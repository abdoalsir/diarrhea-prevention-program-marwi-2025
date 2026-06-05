# [Project Title]

## [Institution], Sudan – [Year]

**Study type:** [e.g. Cross-sectional descriptive study]

**Degree level:** MBBS

**Institution:** [Faculty and University]

**Sample size:** N = [X] [population]

**Data analyst:** Abdulrahman Sirelkhatim

---

## Background

[2-3 sentences on the research context and why this study matters]

## Objectives

- [Objective 1]
- [Objective 2]
- [Objective 3]

## Study Design & Methods

| Component | Detail |
|-----------|--------|
| Design | |
| Setting | |
| Population | |
| Sampling | |
| Sample size | |
| Data collection | |

**Technical suite:**

| Tool | Purpose |
|------|---------|
| Python (pandas) | Data cleaning |
| IBM SPSS Statistics v26 | Full statistical analysis |
| Python (matplotlib, seaborn) | Figure generation |
| Jupyter Notebook | Exploratory data analysis |

**Statistical methods:**

- **Descriptive statistics:** Frequencies, percentages, means, standard
deviations
- **Bivariate analysis:** [tests used]
- **Multivariate analysis:** [methods used]

## Dataset

| File | Description |
|------|-------------|
| `1_data/raw/` | Raw survey responses — excluded from version control (privacy) |
| `1_data/cleaned/` | Cleaned and recoded dataset |

## Repository Structure

```text
project-name/
│
├── README.md
├── .gitignore
├── .ls-lint.yml
├── .markdownlint.yml
├── .markdownlintignore
│
├── .github/
│   └── workflows/
│       └── ci-checks.yml
│
├── 1_data/
│   ├── raw/
│   └── cleaned/
│
├── 2_cleaning/
│   └── cleaning.py
│
├── 3_notebooks/
│   └── exploratory_analysis.ipynb
│
├── 4_analysis/
│   ├── analysis.sps
│   └── figures.py
│
├── 5_figures/
│
└── 6_docs/
    └── results_chapter.docx
```

## Key Results

[Summary of main findings — 3 to 5 bullet points]

## Selected Figures

**[Figure title]**
![Figure description](5_figures/fig_name.png)

## Limitations

- [Limitation 1]
- [Limitation 2]

## Files

| Script | Purpose |
|--------|---------|
| `2_cleaning/cleaning.py` | Data cleaning and recoding |
| `3_analysis/figures.py` | Figure generation |
| `3_analysis/analysis.sps` | Full SPSS syntax |
| `4_notebooks/exploratory_analysis.ipynb` | EDA |

---

**Data analyst:** *Abdulrahman Sirelkhatim | Analysis conducted [Month Year]*
