"""
Project  : Evaluation of a Diarrheal Prevention Program Among Internally Displaced
           Persons at Marwi Camps, Sudan, 2025 – A Quasi-Experimental Study
Script   : Figure Generation (all figures)
Author   : Abdulrahman Sirelkhatim
Date     : May 2026
Input    : 1_data/cleaned/cleaned_pre.xlsx, 1_data/cleaned/cleaned_post.xlsx
Output   : 5_figures/ directory (PNG, 300 DPI)

Figures produced:
    fig01_gender_distribution.png
    fig02_education_distribution.png
    fig03_occupation_distribution.png
    fig04_water_source_distribution.png
    fig05_kap_scores_pre_post_comparison.png
    fig06_knowledge_category_pre_post.png
    fig07_attitude_category_pre_post.png
    fig08_practice_category_pre_post.png
    fig09_knowledge_item_comparison.png
    fig10_attitude_item_comparison.png
    fig11_observed_practice_comparison.png
    fig12_self_reported_practice_comparison.png
    fig13_diarrhoea_prevalence_pre_post.png
    fig14_actions_taken_comparison.png
    fig15_kap_scores_by_education.png
    fig16_correlation_heatmap_pre.png
    fig17_attitude_diverging_pre.png
    fig18_attitude_diverging_post.png
"""

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")

PRE_PATH = "1_data/cleaned/cleaned_pre.xlsx"
POST_PATH = "1_data/cleaned/cleaned_post.xlsx"
FIGURES_DIR = "5_figures/"

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11
plt.rcParams["figure.dpi"] = 200

PALETTE = sns.color_palette("Set2")
PRE_COLOR = "#0077B6"
POST_COLOR = "#F4A261"
DIVERGING = ["#d73027", "#fc8d59", "#cccccc", "#91bfdb", "#4575b4"]

# Category integer codes used in cleaned datasets
# knowledge_cat: 1=Poor, 2=Medium, 3=Good
# attitude_cat:  0=Negative, 1=Positive
# practice_cat:  1=Low, 2=Moderate, 3=High
# p_hwash_* / p_use_* / p_store_* / p_see_* / p_use_ors: 0=Never, 1=Sometimes, 2=Always


def save_fig(fig, filename):
    fig.savefig(FIGURES_DIR + filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filename}")


def donut_pie(ax, counts, title):
    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=PALETTE,
        wedgeprops={"width": 0.6, "edgecolor": "white"},
        pctdistance=0.7,
        labeldistance=1.05,
    )
    ax.set_title(title, pad=12)


pre = pd.read_excel(PRE_PATH)
post = pd.read_excel(POST_PATH)
n = len(pre)

edu_map = {
    1: "Literate",
    2: "Primary",
    3: "Secondary",
    4: "University",
    5: "Postgraduate",
}
occ_map = {
    1: "Unemployed",
    2: "Farmer",
    3: "Trader",
    4: "Teacher",
    5: "Employee",
    6: "Other",
}
water_map = {1: "Pipe", 2: "River", 3: "Pump", 4: "Other"}

# Integer codes → display labels for category columns
k_cat_map = {1: "Poor", 2: "Medium", 3: "Good"}
att_cat_map = {0: "Negative", 1: "Positive"}
p_cat_map = {1: "Low", 2: "Moderate", 3: "High"}


# --- Figures 1–4: Sociodemographic distributions (pre-intervention sample) ---
fig, ax = plt.subplots(figsize=(5, 5))
counts = pre["gender"].map({1: "Male", 2: "Female"}).value_counts()
donut_pie(ax, counts, f"Gender Distribution (N={n})")
save_fig(fig, "fig01_gender_distribution.png")

fig, ax = plt.subplots(figsize=(5, 5))
counts = pre["edu_level"].map(edu_map).value_counts()
donut_pie(ax, counts, f"Education Level (N={n})")
save_fig(fig, "fig02_education_distribution.png")

fig, ax = plt.subplots(figsize=(5, 5))
counts = pre["occupation"].map(occ_map).value_counts()
donut_pie(ax, counts, f"Occupation Distribution (N={n})")
save_fig(fig, "fig03_occupation_distribution.png")

fig, ax = plt.subplots(figsize=(5, 5))
counts = pre["water_source"].map(water_map).value_counts()
donut_pie(ax, counts, f"Primary Water Source (N={n})")
save_fig(fig, "fig04_water_source_distribution.png")


# --- Figure 5: KAP mean scores comparison (grouped bar) ---
kap_vars = {
    "Knowledge\n(0–13)": ("knowledge_score", 13),
    "Attitude\n(0–14)": ("attitude_score", 14),
    "Practice\n(0–27)": ("practice_score", 27),
    "Composite KAP\n(0–100)": ("kap_score", 100),
}
pre_means = [pre[col].mean() for col, _ in kap_vars.values()]
post_means = [post[col].mean() for col, _ in kap_vars.values()]
labels = list(kap_vars.keys())

x = np.arange(len(labels))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 5))
bars_pre = ax.bar(
    x - width / 2, pre_means, width, label="Pre-Intervention", color=PRE_COLOR
)
bars_post = ax.bar(
    x + width / 2, post_means, width, label="Post-Intervention", color=POST_COLOR
)
for bar in list(bars_pre) + list(bars_post):
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.2f}", ha="center", fontsize=8
    )
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Mean Score")
ax.set_title(
    f"Mean KAP Scores Before and After Intervention (N={n})\nAll comparisons p<0.001"
)
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig05_kap_scores_pre_post_comparison.png")


# --- Helper: grouped bar chart for category distribution ---
# pre_col / post_col are integer-coded; label_map converts them to display strings.
def category_comparison(pre_col, post_col, label_map, categories, title, filename):
    pre_labeled = pre[pre_col].map(label_map)
    post_labeled = post[post_col].map(label_map)
    pre_pcts = (
        pre_labeled.value_counts(normalize=True).reindex(categories).fillna(0) * 100
    )
    post_pcts = (
        post_labeled.value_counts(normalize=True).reindex(categories).fillna(0) * 100
    )

    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    bars_pre = ax.bar(
        x - width / 2, pre_pcts.values, width, label="Pre", color=PRE_COLOR, alpha=0.85
    )
    bars_post = ax.bar(
        x + width / 2,
        post_pcts.values,
        width,
        label="Post",
        color=POST_COLOR,
        alpha=0.85,
    )
    for bar in list(bars_pre) + list(bars_post):
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.5,
            f"{h:.1f}%",
            ha="center",
            fontsize=8,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel("% of Participants")
    ax.set_title(title)
    ax.legend()
    ax.set_ylim(0, 80)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    save_fig(fig, filename)


# --- Figures 6–8: Category distribution comparisons ---
category_comparison(
    "knowledge_cat",
    "knowledge_cat",
    k_cat_map,
    ["Poor", "Medium", "Good"],
    f"Knowledge Category Distribution Pre vs Post (N={n})",
    "fig06_knowledge_category_pre_post.png",
)
category_comparison(
    "attitude_cat",
    "attitude_cat",
    att_cat_map,
    ["Negative", "Positive"],
    f"Attitude Category Distribution Pre vs Post (N={n})",
    "fig07_attitude_category_pre_post.png",
)
category_comparison(
    "practice_cat",
    "practice_cat",
    p_cat_map,
    ["Low", "Moderate", "High"],
    f"Practice Category Distribution Pre vs Post (N={n})",
    "fig08_practice_category_pre_post.png",
)


# --- Figure 9: Knowledge item correct response rates (horizontal paired bar) ---
k_items = [
    "k_diarrhea_def",
    "k_contam_water",
    "k_unwashed_hands",
    "k_hwash_toilet",
    "k_water_alone",
    "k_boil_treat",
    "k_feces_source",
    "k_flies",
    "k_transmit",
    "k_ors_prepare",
    "k_water_methods_yn",
    "k_hwash_latrine",
    "k_latrine_struct",
]
k_labels = [
    "Correct definition of diarrhea",
    "Contaminated water as risk factor",
    "Unwashed hands as risk factor",
    "Handwashing after toilet use",
    "Water alone does not make it safe",
    "Boiling as water treatment",
    "Feces as source of contamination",
    "Flies as transmission vehicle",
    "Transmission routes",
    "ORS preparation",
    "Water purification methods",
    "Handwashing after using latrine",
    "Correct latrine structure",
]
pre_k_pcts = [pre[c].mean() * 100 for c in k_items]
post_k_pcts = [post[c].mean() * 100 for c in k_items]

sorted_idx = np.argsort(pre_k_pcts)
labels_s = [k_labels[i] for i in sorted_idx]
pre_s = [pre_k_pcts[i] for i in sorted_idx]
post_s = [post_k_pcts[i] for i in sorted_idx]

y = np.arange(len(labels_s))
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(y - 0.2, pre_s, height=0.35, label="Pre", color=PRE_COLOR, alpha=0.85)
ax.barh(y + 0.2, post_s, height=0.35, label="Post", color=POST_COLOR, alpha=0.85)
ax.set_yticks(y)
ax.set_yticklabels(labels_s, fontsize=9)
ax.set_xlabel("% Correct Responses")
ax.set_title(f"Knowledge Item Correct Response Rates Pre vs Post (N={n})")
ax.set_xlim(0, 115)
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig09_knowledge_item_comparison.png")


# --- Figure 10: Attitude item positive response rates ---
att_items = [
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
att_labels = [
    "Diarrhea is a serious issue",
    "Confident in ability to prevent",
    "Safe water important for family",
    "Water should be treated",
    "Handwashing reduces exposure",
    "Soap is effective",
    "Water container cleanliness",
    "Poor hygiene causes diarrhea",
    "Latrines should provide privacy",
    "Latrines accessible at night",
    "Latrine structure prevents disease",
    "Community should share latrine",
    "Defective water systems transmit disease",
    "Waste near homes attracts flies",
]
pre_att = [pre[c].mean() * 100 for c in att_items]
post_att = [post[c].mean() * 100 for c in att_items]

sorted_idx = np.argsort(pre_att)
labels_s = [att_labels[i] for i in sorted_idx]
pre_s = [pre_att[i] for i in sorted_idx]
post_s = [post_att[i] for i in sorted_idx]

y = np.arange(len(labels_s))
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(y - 0.2, pre_s, height=0.35, label="Pre", color=PRE_COLOR, alpha=0.85)
ax.barh(y + 0.2, post_s, height=0.35, label="Post", color=POST_COLOR, alpha=0.85)
ax.set_yticks(y)
ax.set_yticklabels(labels_s, fontsize=9)
ax.set_xlabel("% Positive Responses")
ax.set_title(f"Attitude Item Positive Response Rates Pre vs Post (N={n})")
ax.set_xlim(0, 115)
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig10_attitude_item_comparison.png")


# --- Figure 11: Observed practice indicators ---
obs_cols = [
    "obs_hwash_critical",
    "obs_waste_disposal",
    "obs_latrine_use",
    "obs_latrine_clean",
    "obs_child_feces",
    "obs_nails",
    "obs_hh_waste",
]
obs_labels = [
    "Handwashing facility present",
    "Waste managed appropriately",
    "Latrine used properly",
    "Latrine clean",
    "Children's feces disposed safely",
    "Child's nails trimmed/clean",
    "Household waste disposed appropriately",
]
pre_obs = [pre[c].mean() * 100 for c in obs_cols if c in pre.columns]
post_obs = [post[c].mean() * 100 for c in obs_cols if c in post.columns]
valid_labels = [label for c, label in zip(obs_cols, obs_labels) if c in pre.columns]

y = np.arange(len(valid_labels))
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(y - 0.2, pre_obs, height=0.35, label="Pre", color=PRE_COLOR, alpha=0.85)
ax.barh(y + 0.2, post_obs, height=0.35, label="Post", color=POST_COLOR, alpha=0.85)
ax.set_yticks(y)
ax.set_yticklabels(valid_labels, fontsize=9)
ax.set_xlabel("% Positive Observations")
ax.set_title(f"Observed Practice Indicators Pre vs Post (N={n})")
ax.set_xlim(0, 115)
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig11_observed_practice_comparison.png")


# --- Figure 12: Self-reported practice (% always responding) ---
# Practice frequency: 0=Never, 1=Sometimes, 2=Always
prac_always_cols = [
    "p_hwash_outdoor",
    "p_hwash_toilet",
    "p_hwash_food_prep",
    "p_hwash_before_eat",
    "p_use_safe_water",
    "p_store_water",
    "p_see_doctor",
    "p_use_ors",
]
prac_labels = [
    "Handwashing after outdoor activity",
    "Handwashing after toilet",
    "Handwashing before food prep",
    "Handwashing before eating",
    "Using safe water for drinking",
    "Safe water storage",
    "Seeking medical care when ill",
    "Use of ORS during diarrhea",
]
pre_always = [(pre[c] == 2).mean() * 100 for c in prac_always_cols if c in pre.columns]
post_always = [
    (post[c] == 2).mean() * 100 for c in prac_always_cols if c in post.columns
]
valid_prac = [label for c, label in zip(prac_always_cols, prac_labels) if c in pre.columns]

y = np.arange(len(valid_prac))
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(
    y - 0.2, pre_always, height=0.35, label="Pre (Always)", color=PRE_COLOR, alpha=0.85
)
ax.barh(
    y + 0.2,
    post_always,
    height=0.35,
    label="Post (Always)",
    color=POST_COLOR,
    alpha=0.85,
)
ax.set_yticks(y)
ax.set_yticklabels(valid_prac, fontsize=9)
ax.set_xlabel("% Reporting 'Always'")
ax.set_title(f"Self-Reported Practice: 'Always' Category Pre vs Post (N={n})")
ax.set_xlim(0, 115)
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig12_self_reported_practice_comparison.png")


# --- Figure 13: Household diarrhoea prevalence ---
fig, ax = plt.subplots(figsize=(5, 4))
pre_prev = pre["diarrhea_hh_yn"].mean() * 100
post_prev = post["diarrhea_hh_yn"].mean() * 100
bars = ax.bar(
    ["Pre-Intervention", "Post-Intervention"],
    [pre_prev, post_prev],
    color=[PRE_COLOR, POST_COLOR],
)
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.5,
        f"{h:.1f}%",
        ha="center",
        fontsize=10,
    )
ax.set_ylabel("Households Reporting Diarrhoea (%)")
ax.set_title(
    f"Household Diarrhoea Prevalence (N={n})\nReduction: −8.6 percentage points"
)
ax.set_ylim(0, 60)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig13_diarrhoea_prevalence_pre_post.png")


# --- Figure 14: Actions taken in response to diarrhea ---
action_cols = [
    "p_act_health_center",
    "p_act_ors",
    "p_act_home_treat",
    "p_act_stop_feeding",
]
action_labels = [
    "Went to health centre",
    "Administered ORS",
    "Used home remedies",
    "Stopped feeding ill person",
]
pre_acts = [pre[c].mean() * 100 for c in action_cols if c in pre.columns]
post_acts = [post[c].mean() * 100 for c in action_cols if c in post.columns]
valid_acts = [label for c, label in zip(action_cols, action_labels) if c in pre.columns]

x = np.arange(len(valid_acts))
width = 0.35
fig, ax = plt.subplots(figsize=(8, 4))
bars_pre = ax.bar(
    x - width / 2, pre_acts, width, label="Pre", color=PRE_COLOR, alpha=0.85
)
bars_post = ax.bar(
    x + width / 2, post_acts, width, label="Post", color=POST_COLOR, alpha=0.85
)
for bar in list(bars_pre) + list(bars_post):
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.1f}%", ha="center", fontsize=8
    )
ax.set_xticks(x)
ax.set_xticklabels(valid_acts, rotation=15, ha="right")
ax.set_ylabel("% of Respondents")
ax.set_title(f"Actions Taken in Response to Diarrhoea (N={n})")
ax.legend()
ax.set_ylim(0, 90)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig14_actions_taken_comparison.png")


# --- Figure 15: Composite KAP by education level (pre-intervention) ---
edu_order = ["Literate", "Primary", "Secondary", "University", "Postgraduate"]
pre["edu_label"] = pre["edu_level"].map(edu_map)
kap_by_edu = pre.groupby("edu_label")["kap_score"].mean().reindex(edu_order).dropna()

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(kap_by_edu.index, kap_by_edu.values, color=PRE_COLOR)
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.1f}", ha="center", fontsize=9
    )
ax.set_ylabel("Mean Composite KAP Score")
ax.set_title(
    "Composite KAP Score by Education Level at Baseline\nF(4,109)=4.76, p<0.001, Education β=6.00 (p<0.001)"
)
ax.set_ylim(60, 95)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig15_kap_scores_by_education.png")


# --- Figure 16: Spearman correlation heatmap (pre-intervention scores) ---
corr_vars = {
    "Knowledge": "knowledge_score",
    "Attitude": "attitude_score",
    "Practice": "practice_score",
    "Composite KAP": "kap_score",
}
corr_df = pre[[v for v in corr_vars.values()]].copy()
corr_df.columns = list(corr_vars.keys())
rho = corr_df.corr(method="spearman")

annot = pd.DataFrame("", index=rho.index, columns=rho.columns)
for r in rho.index:
    for c in rho.columns:
        if r != c:
            r_val, p_val = stats.spearmanr(
                corr_df[r].dropna(),
                corr_df.loc[corr_df[r].notna() & corr_df[c].notna(), c],
            )
            annot.loc[r, c] = f"ρ={r_val:.3f}\np={p_val:.3f}"

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    rho,
    annot=annot.values,
    fmt="s",
    cmap="coolwarm",
    linewidths=0.5,
    vmin=-1,
    vmax=1,
    cbar_kws={"label": "Spearman ρ"},
    ax=ax,
)
ax.set_title(
    f"Spearman Correlations Between KAP Components at Baseline (N={n})", fontsize=10
)
plt.tight_layout()
save_fig(fig, "fig16_correlation_heatmap_pre.png")


# --- Figures 17–18: Diverging Likert for attitudes (pre and post) ---
# Attitude items are binary (0/1) in cleaned data — no Likert string mapping needed.
# The diverging chart maps 0 → left (negative/disagree) and 1 → right (positive/agree).
att_items_raw = [
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
att_short_labels = [
    "Diarrhea is serious",
    "Confident in prevention",
    "Safe water for family",
    "Treat water before drinking",
    "Handwashing reduces exposure",
    "Soap is effective",
    "Water container cleanliness",
    "Poor hygiene causes diarrhea",
    "Latrines: privacy",
    "Latrines: night access",
    "Latrine structure prevents disease",
    "Share community latrine",
    "Defective water transmits disease",
    "Waste attracts disease flies",
]


def diverging_binary(df, items, short_labels, title, filename):
    """Diverging bar chart for binary (0/1) attitude items.

    Positive (1) extends right; negative (0) extends left.
    """
    rows = {}
    for col, label in zip(items, short_labels):
        if col not in df.columns:
            continue
        pct_positive = df[col].mean() * 100
        pct_negative = 100 - pct_positive
        rows[label] = {
            "Negative (Disagree)": pct_negative,
            "Positive (Agree)": pct_positive,
        }

    df_l = pd.DataFrame(rows).T

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(
        df_l.index,
        -df_l["Negative (Disagree)"],
        color=DIVERGING[0],
        label="Negative / Disagree",
    )
    ax.barh(
        df_l.index,
        df_l["Positive (Agree)"],
        color=DIVERGING[4],
        label="Positive / Agree",
    )
    ax.axvline(0, color="black", linewidth=1.0)
    ax.set_xlim(-100, 100)
    ax.xaxis.set_major_formatter(lambda x, pos: f"{abs(x):.0f}%")
    ax.set_xlabel("Percentage of Respondents")
    ax.tick_params(axis="y", length=0)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.07),
        ncol=2,
        frameon=False,
        fontsize=10,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.invert_yaxis()
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    save_fig(fig, filename)


diverging_binary(
    pre,
    att_items_raw,
    att_short_labels,
    f"Attitude Responses — Pre-Intervention (N={n})",
    "fig17_attitude_diverging_pre.png",
)

diverging_binary(
    post,
    att_items_raw,
    att_short_labels,
    f"Attitude Responses — Post-Intervention (N={n})",
    "fig18_attitude_diverging_post.png",
)

print(f"\nAll figures saved to: {FIGURES_DIR}")
