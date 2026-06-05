"""
Project  : Evaluation of a Diarrheal Prevention Program Among Internally Displaced
           Persons at Marwi Camps, Sudan, 2025 – A Quasi-Experimental Study
Script   : Data Cleaning & Recoding (Pre- and Post-Intervention)
Author   : Abdulrahman Sirelkhatim
Date     : May 2026
Input    : 1_data/raw/pre_raw.xlsx, 1_data/raw/post_raw.xlsx
Output   : 1_data/cleaned/cleaned_pre.xlsx, 1_data/cleaned/cleaned_post.xlsx
"""

import numpy as np
import pandas as pd

PRE_RAW = "1_data/raw/pre_raw.xlsx"
POST_RAW = "1_data/raw/post_raw.xlsx"
PRE_OUT = "1_data/cleaned/cleaned_pre.xlsx"
POST_OUT = "1_data/cleaned/cleaned_post.xlsx"

FREQ_MAP = {"Always": 3, "Some time": 2, "Sometimes": 2, "Rare": 1, "Never": 0}

BINARY_K_CORRECT = {
    12: "Yes",
    13: "Yes",
    14: "Yes",
    15: "Yes",
    16: "Yes",
    17: "Yes",
    18: "Yes",
    19: "Yes",
    20: "No",
    21: "No",
    22: "Yes",
}

ATTITUDE_POSITIVE = [23, 24, 25, 26, 27, 28, 29, 30, 35, 36]
ATTITUDE_NEGATIVE = [31, 32, 33, 34]


def col(df, idx):
    return df.iloc[:, idx]


def recode_gender(val):
    v = str(val).strip()
    if v == "Male":
        return 1
    if v == "Female":
        return 2
    return np.nan


def recode_edu(val):
    v = str(val).strip().lower()
    mapping = {
        "literate": 1,
        "primary": 2,
        "secondary": 3,
        "university": 4,
        "postgraduate": 5,
    }
    return mapping.get(v, np.nan)


def recode_fam_size(val):
    v = str(val).strip()
    if v == "3 or less":
        return 1
    if v == "4 to 7":
        return 2
    if v == "More than 7":
        return 3
    return np.nan


def recode_income(val):
    v = str(val).strip()
    if v == "<100000":
        return 1
    if v == "100000-250000":
        return 2
    if v == ">250000":
        return 3
    return np.nan


def recode_occupation(val):
    v = str(val).strip().lower().rstrip()
    mapping = {
        "unemployed": 1,
        "farmer": 2,
        "trader": 3,
        "teacher": 4,
        "employee": 5,
        "free worker": 6,
        "free work": 6,
        "student": 7,
        "doctor": 8,
        "other": 8,
    }
    return mapping.get(v, np.nan)


def recode_water_source(val):
    v = str(val).strip().lower()
    if v == "pipe":
        return 1
    if v == "river":
        return 2
    if v == "pump":
        return 3
    if v in ("weel", "well"):
        return 4
    return 5


def score_binary_k(df, col_idx, correct_answer):
    raw = col(df, col_idx).astype(str).str.strip()
    return (raw == correct_answer).astype(int)


def score_attitude_positive(series):
    v = series.astype(str).str.strip().str.lower()
    return v.isin(["agree", "strongly agree"]).astype(int)


def score_attitude_negative(series):
    v = series.astype(str).str.strip().str.lower()
    return v.isin(["disagree", "strongly disagree"]).astype(int)


def score_k_diarrhea_def(series):
    """Correct Answer: mentions loose/watery stool 3+ times per day."""
    v = series.astype(str).str.lower()
    correct = v.str.contains("loose", na=False) | v.str.contains("watery", na=False)
    return correct.astype(int)


def score_k_transmission(series):
    """Correct Answer: mentions contaminated water AND/OR dirty hands."""
    v = series.astype(str).str.lower()
    return (v.str.contains("dirty", na=False) | v.str.contains("bad", na=False)).astype(
        int
    )


def score_k_water_treat(series):
    """Correct Answer: mentions boiling or chlorination."""
    v = series.astype(str).str.lower()
    return (
        v.str.contains("boil", na=False) | v.str.contains("chlorin", na=False)
    ).astype(int)


def score_k_hwash_times(series):
    """Correct Answer: mentions after toilet use AND before eating."""
    v = series.astype(str).str.lower()
    after_toilet = v.str.contains("toilet", na=False)
    before_eating = v.str.contains("before eating", na=False)
    return (after_toilet & before_eating).astype(int)


def score_p_hwash_before_eat(series):
    """How often wash hands before eating: By water and soap = 2, by water = 1, Not wash = 0."""
    v = series.astype(str).str.strip().str.lower()
    result = pd.Series(np.nan, index=series.index)
    result[v == "by water and soap"] = 2
    result[v == "by water"] = 1
    result[v == "not wash"] = 0
    return result


def expand_diarrhea_actions(series):
    """Expand multi-select diarrhea actions into binary dummies."""
    v = series.astype(str).str.lower()
    return pd.DataFrame(
        {
            "p_act_health_center": v.str.contains("health center", na=False).astype(
                int
            ),
            "p_act_ors": v.str.contains("ors", na=False).astype(int),
            "p_act_home_treat": v.str.contains("home treatment", na=False).astype(int),
            "p_act_stop_feeding": v.str.contains("stop feeding", na=False).astype(int),
        }
    )


def process(raw_path, out_path):
    df = pd.read_excel(raw_path)

    out = pd.DataFrame()

    out["prev_info"] = (col(df, 0).astype(str).str.strip() == "Yes").astype(int)
    out["age"] = pd.to_numeric(col(df, 1), errors="coerce").astype("Int64")
    out["gender"] = col(df, 2).apply(recode_gender).astype("Int64")
    out["occupation"] = col(df, 3).apply(recode_occupation).astype("Int64")
    out["edu_level"] = col(df, 4).apply(recode_edu).astype("Int64")
    out["fam_size"] = col(df, 5).apply(recode_fam_size).astype("Int64")
    out["income"] = col(df, 6).apply(recode_income).astype("Int64")

    out["k_diarrhea_def"] = score_k_diarrhea_def(col(df, 7))
    out["k_transmission"] = score_k_transmission(col(df, 8))
    out["k_water_methods_yn"] = (col(df, 9).astype(str).str.strip() == "Yes").astype(
        int
    )
    out["k_water_treat"] = score_k_water_treat(col(df, 10))
    out["k_hwash_times"] = score_k_hwash_times(col(df, 11))

    for col_idx, name in [
        (12, "k_contam_water"),
        (13, "k_unwashed_hands"),
        (14, "k_hwash_toilet"),
        (15, "k_water_alone"),
        (16, "k_boil_treat"),
        (17, "k_feces_source"),
        (18, "k_flies"),
        (19, "k_transmit"),
    ]:
        out[name] = score_binary_k(df, col_idx, "Yes")

    out["k_hwash_latrine"] = score_binary_k(df, 20, "No")
    out["k_latrine_struct"] = score_binary_k(df, 21, "No")
    out["k_ors_prepare"] = score_binary_k(df, 22, "Yes")

    k_cols = [
        "k_diarrhea_def",
        "k_transmission",
        "k_water_treat",
        "k_hwash_times",
        "k_contam_water",
        "k_unwashed_hands",
        "k_hwash_toilet",
        "k_water_alone",
        "k_boil_treat",
        "k_feces_source",
        "k_flies",
        "k_transmit",
        "k_hwash_latrine",
        "k_latrine_struct",
        "k_ors_prepare",
    ]
    out["knowledge_score"] = out[k_cols].sum(axis=1)

    def knowledge_cat(score):
        if pd.isna(score):
            return np.nan
        if score >= 12:
            return 3
        if score >= 9:
            return 2
        return 1

    out["knowledge_cat"] = out["knowledge_score"].apply(knowledge_cat).astype("Int64")

    for col_idx, name in zip(
        ATTITUDE_POSITIVE,
        [
            "a_serious_issue",
            "a_confident_prev",
            "a_family_water",
            "a_treat_water",
            "a_handwash_expose",
            "a_soap_effective",
            "a_water_container",
            "a_hygiene_cause",
            "a_defect_water",
            "a_waste_flies",
        ],
    ):
        out[name] = score_attitude_positive(col(df, col_idx))

    for col_idx, name in zip(
        ATTITUDE_NEGATIVE,
        [
            "a_latrine_privacy",
            "a_latrine_night",
            "a_latrine_struct2",
            "a_neighbor_latrine",
        ],
    ):
        out[name] = score_attitude_negative(col(df, col_idx))

    a_cols = [
        "a_serious_issue",
        "a_confident_prev",
        "a_family_water",
        "a_treat_water",
        "a_handwash_expose",
        "a_soap_effective",
        "a_water_container",
        "a_hygiene_cause",
        "a_latrine_privacy",
        "a_latrine_night",
        "a_latrine_struct2",
        "a_neighbor_latrine",
        "a_defect_water",
        "a_waste_flies",
    ]
    out["attitude_score"] = out[a_cols].sum(axis=1)
    out["attitude_cat"] = (out["attitude_score"] >= 9).astype(int)

    out["diarrhea_hh_yn"] = (col(df, 37).astype(str).str.strip() == "Yes").astype(int)
    out["diarrhea_hh_count"] = pd.to_numeric(col(df, 38), errors="coerce").astype(
        "Int64"
    )

    actions = expand_diarrhea_actions(col(df, 39))
    for c in actions.columns:
        out[c] = actions[c]

    out["p_hwash_before_eat"] = score_p_hwash_before_eat(col(df, 40))

    for col_idx, name in zip(
        range(41, 49),
        [
            "p_hwash_outdoor",
            "p_hwash_toilet",
            "p_hwash_food_prep",
            "p_hwash_soap",
            "p_use_safe_water",
            "p_store_water",
            "p_see_doctor",
            "p_use_ors",
        ],
    ):
        out[name] = col(df, col_idx).map(FREQ_MAP)

    p_cols = [
        "p_hwash_outdoor",
        "p_hwash_toilet",
        "p_hwash_food_prep",
        "p_hwash_soap",
        "p_use_safe_water",
        "p_store_water",
        "p_see_doctor",
        "p_use_ors",
    ]
    out["practice_score"] = out[p_cols].sum(axis=1, skipna=True)

    def practice_cat(score):
        if pd.isna(score):
            return np.nan
        if score >= 19:
            return 3
        if score >= 10:
            return 2
        return 1

    out["practice_cat"] = out["practice_score"].apply(practice_cat).astype("Int64")

    out["water_source"] = col(df, 49).apply(recode_water_source).astype("Int64")
    out["obs_hwash_critical"] = (col(df, 50).astype(str).str.strip() == "Yes").astype(
        int
    )
    out["obs_waste_disposal"] = (
        col(df, 51).astype(str).str.strip() == "Appropriate"
    ).astype(int)
    # 99 = Not applicable for households without latrines, but we keep it separate from NaN for analysis purposes
    out["obs_latrine_use"] = col(df, 52).map(
        {"Properly": 1, "Improperly": 0, "Not applicable": 99}
    )
    out["obs_latrine_clean"] = col(df, 53).map(
        {"Yes": 1, "No": 0, "Not applicable": 99}
    )
    out["obs_child_feces"] = (col(df, 54).astype(str).str.strip() == "Yes").astype(int)
    out["obs_nails"] = (col(df, 55).astype(str).str.strip() == "Yes").astype(int)
    out["obs_hh_waste"] = (
        col(df, 56)
        .map({"In community dustbins": 1, "Burn": 2, "Open": 3})
        .astype("Int64")
    )

    obs_cols = [
        "obs_hwash_critical",
        "obs_waste_disposal",
        "obs_latrine_use",
        "obs_latrine_clean",
        "obs_child_feces",
        "obs_nails",
    ]
    out["obs_score"] = out[obs_cols].sum(axis=1, skipna=True)

    k_max, a_max, p_max = 15, 14, 24
    out["kap_score"] = (
        (out["knowledge_score"] / k_max * 100 * 0.33)
        + (out["attitude_score"] / a_max * 100 * 0.33)
        + (out["practice_score"] / p_max * 100 * 0.34)
    ).round(2)

    out.insert(0, "ID", range(1, len(out) + 1))
    out.to_excel(out_path, index=False)
    print(f"Saved: {out_path} — {out.shape[0]} rows x {out.shape[1]} columns")
    return out


pre_df = process(PRE_RAW, PRE_OUT)
post_df = process(POST_RAW, POST_OUT)

print(
    f"\nPre  — Knowledge: {pre_df['knowledge_score'].mean():.2f}  "
    f"Attitude: {pre_df['attitude_score'].mean():.2f}  "
    f"Practice: {pre_df['practice_score'].mean():.2f}  "
    f"KAP: {pre_df['kap_score'].mean():.2f}"
)
print(
    f"Post — Knowledge: {post_df['knowledge_score'].mean():.2f}  "
    f"Attitude: {post_df['attitude_score'].mean():.2f}  "
    f"Practice: {post_df['practice_score'].mean():.2f}  "
    f"KAP: {post_df['kap_score'].mean():.2f}"
)
