* Encoding: windows-1252.
* Project  : Evaluation of a Diarrheal Prevention Program Among Internally Displaced
*            Persons at Marwi Camps, Sudan, 2025 - A Quasi-Experimental Study
* Script   : Post-Intervention Statistical Analysis and Pre-Post Comparison
* Author   : Abdulrahman Sirelkhatim
* Date     : May 2026
*
* NOTE: Update the FILE paths below before running.
* The one-sample t-tests compare post-intervention means against pre-intervention
* means as reference values (independent samples quasi-experimental design).
* Encoding: UTF-8.

GET DATA
  /TYPE=XLSX
  /FILE='C:\path\to\1_data\cleaned\cleaned_post.xlsx'
  /SHEET=name 'Sheet1'
  /READNAMES=ON.
CACHE.
EXECUTE.

VARIABLE LABELS
  knowledge_score 'Knowledge Scale Total Score (0-13)'
  knowledge_cat 'Knowledge Category (Poor/Medium/Good)'
  attitude_score 'Attitude Scale Total Score (0-14)'
  attitude_cat 'Attitude Category (Positive/Negative)'
  practice_score 'Practice Scale Total Score (0-27)'
  practice_cat 'Practice Category (Low/Moderate/High)'
  kap_score 'Composite KAP Score (0-100)'
  p_hh_diarrhea_r 'Household Reported Diarrhea Episode (1=Yes, 0=No)'.
EXECUTE.

* Descriptive statistics: post-intervention scores.
DESCRIPTIVES VARIABLES=knowledge_score attitude_score practice_score kap_score
  /STATISTICS=MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES=knowledge_cat attitude_cat practice_cat p_hh_diarrhea_r
  /STATISTICS=MODE /BARCHART PERCENT.

FREQUENCIES VARIABLES=k_diarrhea_def k_r_contam_water k_r_unwashed_hands k_r_hwash_toilet
  k_r_water_alone k_r_boil_treat k_r_feces_source k_r_flies k_r_transmit
  k_r_hwash_latrine k_r_latrine_struct k_r_ors_prepare k_r_water_methods
  /STATISTICS=MEAN.

FREQUENCIES VARIABLES=p_hwash_outdoor_r p_hwash_toilet_r p_hwash_food_prep_r
  p_hwash_before_eat_r p_use_safe_water_r p_store_water_r p_see_doctor_r p_use_ors_r
  obs_hwash_r obs_waste_r obs_latrine_r obs_lat_clean_r obs_child_f_r obs_nails_r obs_hh_waste_r
  /STATISTICS=MEAN MODE.

* One-sample t-tests: compare post-intervention means against pre-intervention means
* as fixed reference values (pre means from pre_analysis output).
* Pre-intervention means: Knowledge=9.61, Attitude=10.49, Practice=18.51, KAP=72.48.
T-TEST
  /TESTVAL=9.61
  /MISSING=ANALYSIS
  /VARIABLES=knowledge_score
  /CRITERIA=CI(.95).

T-TEST
  /TESTVAL=10.49
  /MISSING=ANALYSIS
  /VARIABLES=attitude_score
  /CRITERIA=CI(.95).

T-TEST
  /TESTVAL=18.51
  /MISSING=ANALYSIS
  /VARIABLES=practice_score
  /CRITERIA=CI(.95).

T-TEST
  /TESTVAL=72.48
  /MISSING=ANALYSIS
  /VARIABLES=kap_score
  /CRITERIA=CI(.95).

* Post-intervention regression: does education still predict KAP after the program?.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT kap_score
  /METHOD=ENTER age gender_r edu_r fam_size_r income_r occupation_r.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT knowledge_score
  /METHOD=ENTER age gender_r edu_r fam_size_r income_r occupation_r.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT practice_score
  /METHOD=ENTER age gender_r edu_r fam_size_r income_r occupation_r.

* NOTE: Update the OUTFILE path below before saving.
SAVE OUTFILE='C:\path\to\1_data\cleaned\cleaned_post.sav' /COMPRESSED.
EXECUTE.
