# Lecture 5 methods reference

For each operation, explain **input → operation → output → check**. Use the data's declared keys, units, and policy. Examples below assume the lecture's synthetic tables.

## 1. Read and inspect

```python
raw = pd.read_csv(path, dtype={'value_text': 'string'}, keep_default_na=False)
raw.shape
raw.dtypes
raw.head()
```

Reading a value column as text preserves visible tokens for inspection. `keep_default_na=False` prevents automatic interpretation of text tokens as missing during this read. Decide their meaning explicitly later. Keep the input file and work on a copy.

## 2. Select

```python
work = raw.copy()
work['category'] = work['category_text'].str.strip().str.upper()
work['value_text']               # Series
work[['value_text']]             # DataFrame
work.loc[mask, ['category', 'value_text']]
work.iloc[:3, :2]                # first three positions, first two columns
```

`.loc` uses labels or a mask; `.iloc` uses positions. A mask must describe the intended records and align with the table. Use `&`, `|`, and `~` for elementwise Boolean operations, with parentheses around component comparisons.

## 3. Assign

```python
mask = work['category'].eq('HOUSING')
work['review_flag'] = False
work.loc[mask, 'review_flag'] = True
```

This explicitly assigns into `work`. A separately copied subset is a different table. Avoid chained assignment through successive bracket selections. [Official indexing and assignment guide](https://pandas.pydata.org/docs/user_guide/indexing.html).

## 4. Parse and audit

```python
work['date'] = pd.to_datetime(work['date_text'], format='%d/%m/%Y', errors='coerce')
text = work['value_text'].str.strip().str.replace(',', '', regex=False)
source_missing = text.str.upper().isin(['', 'NA', 'NOT REPORTED'])
work['value'] = pd.to_numeric(text.mask(source_missing), errors='coerce').astype('Float64')
parse_failure = ~source_missing & work['value'].isna()
```

The comma convention and missing tokens are source-specific. Coercion produces a missing typed value for an unparseable token. Inspect the failure mask and retain the original text. Date parsing requires an explicit convention; invalid dates cannot form usable keys.

## 5. Enforce a stated domain

```python
invalid = work['value'].lt(0).fillna(False)
work.loc[invalid, 'value_reason'] = 'invalid_negative'
work.loc[invalid, 'value'] = pd.NA
```

This exercise requires nonnegative values. Keep missing, invalid, and observed zero distinct. Any imputation needs a stated justification. Do not replace unknown values with zero as a generic cleaning step.

## 6. Detect repeats and keys

```python
work.duplicated(['category', 'date_text', 'value_text'], keep=False)
work.duplicated(['category', 'date'], keep=False)
```

The first asks whether the measurement fields repeat; the second asks whether the analytical key repeats. Source-row IDs are provenance fields. Resolve why a key repeats before choosing a removal or aggregation. Here only a confirmed copy is removed; unresolved key candidates are quarantined together.

## 7. Stack compatible files

```python
assert list(batch_a.columns) == list(batch_b.columns)
stacked = pd.concat([batch_a, batch_b], ignore_index=True)
assert not stacked.duplicated(['category', 'date']).any()
```

`concat` appends compatible records. Resetting the index does not remove duplicated observations. Check compatible column meanings and data types as well as names.

## 8. Attach columns through keys

```python
joined = clean.merge(lookup, on='category', how='left',
                     validate='many_to_one', indicator=True)
unmatched = joined.loc[joined['_merge'].eq('left_only')]
```

Many readings can match one accepted category lookup row. A left join preserves unmatched primary records. Cardinality and match coverage are separate checks. Missing keys require explicit handling because pandas can match null keys. [Official merge reference](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html).

For two tables with one row per category-date:

```python
joined = primary.merge(reference, on=['category', 'date'], how='left',
                       validate='one_to_one', indicator=True)
```

Use the whole key. Compare output key sets and uniqueness, not just the number of rows.

## 9. Group and summarize

```python
summary = clean.groupby('category').agg(
    mean_value=('value', 'mean'),
    valid_values=('value', 'count'),
    records=('value', 'size'),
)
```

`agg` produces group summaries. For this numeric variable, `count` excludes missing values, `size` counts rows, and the mean uses observed values. An all-missing group has no observed mean.

```python
clean['group_mean'] = clean.groupby('category')['value'].transform('mean')
```

`transform` produces values aligned to the input records. An observation-weighted mean of group means can recover the pooled mean when the weights count valid values for the same variable. [Official groupby guide](https://pandas.pydata.org/docs/user_guide/groupby.html).

## 10. Reshape

```python
long = wide.melt(id_vars='category', value_vars=['2024-01', '2024-02'],
                 var_name='month', value_name='value')
wide_again = long.pivot(index='category', columns='month', values='value')
```

Melting two value columns over two records creates four long records, including missing cells. Pivoting requires one record per cell key. `pivot_table` adds an aggregation choice; it cannot establish the correctness of conflicting source records. [Official reshape guide](https://pandas.pydata.org/docs/user_guide/reshaping.html).

## 11. Package and verify

```python
clean, issues, quarantine = prepare_prices(raw, confirmed_copies=(3,))
result = clean.pipe(validate_prices).pipe(add_period)
result.to_csv('outputs/clean_prices.csv', index=False)
```

Functions receive explicit inputs and policies. An issue log identifies the source record, issue, action, and reason. Retain quarantined records for investigation. Compare known expected keys, verify uniqueness and domain rules, preserve input snapshots and versions, and restart/run all. A passed check establishes the stated condition.
