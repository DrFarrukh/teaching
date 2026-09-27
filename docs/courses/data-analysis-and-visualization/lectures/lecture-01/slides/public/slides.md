# Data Analysis and Visualization

## Lecture 1

Can the data show whether Pakistan's Big Three are losing dominance?

---

# The opening question

Are Suzuki, Toyota, and Honda losing their dominance in Pakistan?

Choose one answer before seeing the data:

- Yes
- No
- Not sure

<!-- Ask for a show of hands. Record the vote on the board. Ask for reasons but do not evaluate them yet. -->

---

# Reasons are not yet evidence

Students may mention:

- Resale value and reliability
- Price and financing
- Features offered by new brands
- Fuel cost and charging access
- Personal experience

Which of these can the workbook measure?

---

# A claim needs a measurable question

```text
Claim
Question
Required measurements
Dataset
Analysis
Evidence
Conclusion and limitation
```

Where can this chain fail?

---

# The population in the claim

The phrase **dominance in Pakistan** could mean:

- All new vehicle sales
- Passenger car sales
- Locally assembled passenger cars
- Sales reported by PAMA members
- Vehicles registered by government agencies

These populations are different.

---

# Unit of observation

Possible observations include:

- One vehicle sale
- One model in one month
- One manufacturer in one fiscal year
- One vehicle category in one month

The unit of observation determines what one row should represent.

---

# Variables needed

For a monthly market share analysis:

| Variable | Example |
|---|---|
| Fiscal month | July 2025 |
| Manufacturer | Toyota |
| Model group | Corolla, Yaris, Corolla Cross |
| Measure | Sales |
| Recorded units | 2,418 |

---

# The source workbook

- 19 fiscal year worksheets
- July 2007 through June 2026
- Monthly production and sales
- Separate vehicle sections
- Changing model labels and column positions
- Formulas, merged cells, subtotals, and totals

<small>Source: Pakistan Automotive Manufacturers Association, https://pama.org.pk/monthly-production-sales-of-vehicles/</small>

---

# Raw data and analysis ready data

Raw worksheet:

| Model | Type | July | August | September |
|---|---|---:|---:|---:|
| Honda Cars | Production | 1,169 | 968 | 1,939 |
|  | Sales | 1,143 | 699 | 1,977 |

Analysis ready table:

| Month | Brand | Model group | Measure | Value |
|---|---|---|---|---:|
| Jul 2025 | Honda | Civic and City | Sales | 1,143 |

---

# Recorded market share

$$
\text{Recorded market share}_{i,t}
=
\frac{\text{Recorded sales}_{i,t}}
{\text{Total recorded sales}_{t}}
$$

Why does the word **recorded** matter?

---

# Big Three concentration

$$
CR_3
=
s_{Suzuki}+s_{Toyota}+s_{Honda}
$$

CR3 describes concentration among the three named groups.

It does not explain why concentration changed.

---

# Four questions before calculation

1. Which vehicle categories belong in the denominator?
2. Which manufacturers does the source cover?
3. Are imports and nonmember firms included?
4. Do model labels mean the same thing each year?

<!-- Pause here. Ask pairs to identify one additional question. -->

---

# Pair task before the break

Redesign the projected raw extract so that one row represents:

> one model group in one fiscal month

Write the column names first.

Then identify one validation check.

---

<!-- _class: lead -->

# Namaz break

After the break: live analysis of the prepared data

---

# Live demonstration

We will ask the computer to show:

- What records exist
- How annual recorded sales changed
- Whether CR3 declined
- What the workbook reports for electric cars

For every code block:

1. Predict the output
2. Run the code
3. Interpret the result

---

# Annual recorded passenger car sales

![bg right:58% contain](public/outputs/annual_total_sales.png)

What does the line establish?

What can it not explain?

---

# Big Three recorded share

![bg right:58% contain](public/outputs/big_three_share.png)

Does the workbook support the claim that the Big Three are losing dominance?

State the denominator in your answer.

---

# Electric cars in the workbook

![bg right:58% contain](public/outputs/recorded_ev_sales.png)

The workbook reports 343 Honri-Ve sales in 2025 to 2026.

Can we call this Pakistan's EV market share?

---

# Evidence workshop

Your group must decide whether this statement is supported:

> New and electric vehicle brands are breaking the dominance of Pakistan's traditional Big Three.

Choose:

- Supported
- Not supported
- Cannot be answered adequately

Give one observation, one limitation, and one additional data source.

---

# A defensible conclusion

The PAMA passenger car records show continued concentration among Suzuki, Toyota, and Honda.

The workbook alone cannot establish their share of the complete Pakistani market.

Coverage determines the conclusion we can defend.

---

# Exit ticket

On any small piece of paper, write:

1. One conclusion supported by today's data
2. One conclusion the data cannot support

Include the relevant population or denominator.

---

# Sources

Pakistan Automotive Manufacturers Association

https://pama.org.pk/monthly-production-sales-of-vehicles/

Ministry of Industries and Production

New Energy Vehicles Policy 2025 to 2030

https://moip.gov.pk/SiteImage/Policy/Draft%20NEV%20Policy%20120625%20(V%201.4).pdf

