"""Explained transformation methods for CS-808 Lecture 5.

The small prices table is synthetic. No source value is silently corrected.
"""

from __future__ import annotations

import pandas as pd


def prepare_prices(raw: pd.DataFrame, confirmed_copies: tuple[int, ...] = ()):
    """Return clean rows, a decision log, and quarantined rows.

    Policy: a confirmed repeated row can be removed; invalid dates and unresolved
    key conflicts are quarantined; unknown or invalid values remain missing.
    Every key-conflict row is quarantined, including its apparently valid partner.
    """
    required = {'source_row', 'category_text', 'date_text', 'value_text'}
    if not required.issubset(raw.columns):
        raise ValueError(f'Missing columns: {sorted(required - set(raw.columns))}')
    if raw['source_row'].isna().any() or raw['source_row'].duplicated().any():
        raise ValueError('Source-row identifiers must be present and unique')
    work = raw.copy(deep=True)
    work['category'] = work['category_text'].astype('string').str.strip().str.upper()
    if work['category'].isna().any() or work['category'].eq('').any():
        raise ValueError('A category identifier is required')
    work['date_normalized'] = work['date_text'].astype('string').str.strip()
    work['value_normalized'] = work['value_text'].astype('string').str.strip()
    work['date'] = pd.to_datetime(work['date_normalized'], format='%d/%m/%Y', errors='coerce')
    text = work['value_normalized'].str.replace(',', '', regex=False)
    missing = text.isna() | text.str.upper().isin(['', 'NA', 'NOT REPORTED'])
    work['value'] = pd.to_numeric(text.mask(missing), errors='coerce').astype('Float64')
    failed = ~missing & work['value'].isna()
    negative = work['value'].lt(0).fillna(False)
    work['value_reason'] = 'observed'
    work.loc[missing, 'value_reason'] = 'source_missing'
    work.loc[failed, 'value_reason'] = 'parse_failure'
    work.loc[negative, 'value_reason'] = 'invalid_negative'
    work.loc[negative, 'value'] = pd.NA
    events = []

    def record(mask, issue, action, reason):
        for row_id in work.loc[mask, 'source_row']:
            events.append({'source_row': int(row_id), 'issue': issue,
                           'action': action, 'reason': reason})

    record(missing, 'source_missing', 'retain_missing', 'Documented missing token')
    record(failed, 'parse_failure', 'retain_missing', 'Unparseable value; raw token retained')
    record(negative, 'invalid_negative', 'retain_missing', 'Synthetic exercise requires nonnegative values')

    # Row identifiers are provenance, not measurement fields.
    fields = ['category', 'date_normalized', 'value_normalized']
    repeated = work.duplicated(fields, keep='first')
    confirmed = work['source_row'].isin(confirmed_copies)
    if set(confirmed_copies) - set(work['source_row']):
        raise ValueError('A confirmed copy is not present in this input')
    if (confirmed & ~repeated).any():
        raise ValueError('A confirmed copy does not repeat an earlier record')
    record(confirmed, 'confirmed_copy', 'remove', 'Exercise source note confirms an accidental repeat')
    work = work.loc[~confirmed].copy()

    invalid_date = work['date'].isna()
    record(invalid_date, 'invalid_date', 'quarantine', 'No valid period key can be constructed')
    rejected_dates = work.loc[invalid_date].assign(quarantine_reason='invalid_date')
    work = work.loc[~invalid_date].copy()
    conflicts = work.duplicated(['category', 'date'], keep=False)
    record(conflicts, 'unresolved_key', 'quarantine', 'All repeated-key candidates require source reconciliation')
    rejected_keys = work.loc[conflicts].assign(quarantine_reason='unresolved_key')
    clean = work.loc[~conflicts].sort_values(['category', 'date']).reset_index(drop=True)
    quarantine = pd.concat([rejected_dates, rejected_keys], ignore_index=True)
    issues = pd.DataFrame(events, columns=['source_row', 'issue', 'action', 'reason'])
    issues = issues.sort_values(['source_row', 'issue']).reset_index(drop=True)
    validate_prices(clean)
    return clean, issues, quarantine


def validate_prices(frame: pd.DataFrame) -> pd.DataFrame:
    """Check specific contracts; return the input for a .pipe sequence."""
    if not {'source_row', 'category', 'date', 'value'}.issubset(frame.columns):
        raise ValueError('The cleaned schema is incomplete')
    if frame[['category', 'date']].isna().any().any():
        raise ValueError('Clean keys cannot be missing')
    if frame.duplicated(['category', 'date']).any():
        raise ValueError('Clean category-date keys must be unique')
    if not frame['date'].dt.day.eq(1).all():
        raise ValueError('The exercise uses first-of-month dates for monthly records')
    if frame['value'].dropna().lt(0).any():
        raise ValueError('A negative value violates the exercise contract')
    return frame


def add_period(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.assign(month=frame['date'].dt.to_period('M').astype(str))


def attach_categories(frame: pd.DataFrame, lookup: pd.DataFrame) -> pd.DataFrame:
    if frame['category'].isna().any() or lookup['category'].isna().any():
        raise ValueError('Resolve missing join keys before merging')
    joined = frame.merge(lookup, on='category', how='left',
                         validate='many_to_one', indicator=True)
    if len(joined) != len(frame) or set(joined['source_row']) != set(frame['source_row']):
        raise ValueError('The join changed the primary observation set')
    return joined


def summarize_prices(frame: pd.DataFrame) -> pd.DataFrame:
    summary = frame.groupby('category', dropna=False).agg(
        mean_value=('value', 'mean'),
        valid_values=('value', 'count'),
        records=('value', 'size'),
    ).reset_index()
    return summary.assign(valid_fraction=summary['valid_values'] / summary['records'])
