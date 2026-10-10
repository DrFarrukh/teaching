# Lecture 5 — Methods practice

Eight short after-class problems. Use clear pseudocode or pandas. No computer is required. All numbers are synthetic. Show the operation, relevant key or policy, and a check where requested.

## 1. Select and assign

| Source row | category | value |
|---:|---|---:|
| 1 | FOOD | 120 |
| 2 | FOOD | missing |
| 3 | TRANSPORT | 0 |
| 4 | TRANSPORT | -3 |

Write a mask selecting observed, nonnegative TRANSPORT values. Which source row qualifies? Assign `review_flag=True` to that row without changing its value.

## 2. Parse without hiding failures

The text tokens are `" 1,250 "`, `""`, `"bad"`, `"0"`, and `"-2"`. The source defines commas as thousands separators, blank as missing, and valid values as nonnegative.

Describe the parsing steps and give the final typed value and reason for each token. What original information should remain available?

## 3. Handle an unresolved key

The table should have one record per `(category, month)`. Two records claim FOOD, 2024-04, with values 100 and 101. Their source-row IDs differ.

Does `drop_duplicates('source_row')` address the repeated observation key? Explain how to detect the conflict and what to do while the source is being checked.

## 4. Validate a lookup merge

A primary table has three A records, two B records, and one C record. A lookup has two A rows with different labels, one B row, and no C row.

Predict the row count for an unchecked left merge. Which validation setting should reject the lookup? After resolving A to one accepted lookup row, how many primary records are unmatched?

## 5. Aggregate or transform

Group A contains `[4, missing, 8]`; Group B contains `[2, missing]`.

For each group, give `size`, `count`, mean, and valid-value fraction. How many rows does the group summary have? How many values does a group-mean `transform` return? Give those transformed values in input order.

## 6. Melt and pivot

| product | 2024-01 | 2024-02 |
|---|---:|---:|
| A | 10 | 12 |
| B | 20 | missing |

Show the long table with columns `product`, `month`, and `value`. Give its key. Can it pivot back without aggregation? What changes if a second A, 2024-01 record with value 11 is added?

## 7. Choose the complete merge key

Two tables each contain exactly four records: products A and B for both 2024-01 and 2024-02. Each `(product, month)` key is unique and present in both tables.

How many rows does a merge on `month` alone produce? Write the corrected left merge and its validation setting. Give a match-coverage pass condition.

## 8. Check keys and reproducibility

The expected output key set is `{(A, Jan), (A, Feb), (B, Jan)}`. The output has three records with keys `(A, Jan), (A, Jan), (A, Feb)`.

Does equal row count prove success? State two key checks and their pass conditions. Explain how you would check that the same frozen inputs and configuration reproduce the output after restarting the environment.
