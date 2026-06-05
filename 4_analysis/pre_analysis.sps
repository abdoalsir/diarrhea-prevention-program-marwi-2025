* Project  : Evaluation of a Diarrheal Prevention Program Among Internally Displaced
*            Persons at Marwi Camps, Sudan, 2025 - A Quasi-Experimental Study
* Script   : Pre-Intervention Statistical Analysis
* Author   : Abdulrahman Sirelkhatim
* Date     : May 2026
*
* NOTE: Update the FILE path in the GET DATA command below before running.
* Encoding: UTF-8.

GET DATA
  /TYPE=XLSX
  /FILE='C:\path\to\1_data\cleaned\cleaned_pre.xlsx'
  /SHEET=name 'Sheet1'
  /READNAMES=ON.
CACHE.
EXECUTE.

VARIABLE LABELS
  age 'Age (years)'
  gender 'Gender (1=Male, 2=Female)'
  edu_level 'Education Level'
  fam_size 'Family Size'
  income 'Monthly Income (SDG)'
  occupation 'Occupation'
  water_source 'Primary Water Source'
  prev_info 'Received Diarrhea Prevention Info Before'
  knowledge_score 'Knowledge Scale Total Score (0-13)'
  knowledge_cat 'Knowledge Category (1=Poor, 2=Medium, 3=Good)'
  attitude_score 'Attitude Scale Total Score (0-14)'
  attitude_cat 'Attitude Category (0=Negative, 1=Positive)'
  practice_score 'Practice Scale Total Score (0-27)'
  practice_cat 'Practice Category (1=Low, 2=Moderate, 3=High)'
  kap_score 'Composite KAP Score (0-100)'
  diarrhea_hh_yn 'Household Reported Diarrhea Episode (1=Yes, 0=No)'.

VALUE LABELS
  gender 1 'Male' 2 'Female'
  /edu_level 1 'Literate' 2 'Primary' 3 'Secondary' 4 'University' 5 'Postgraduate'
  /fam_size 1 '3 or fewer' 2 '4 to 7' 3 'More than 7'
  /income 1 '< 100,000 SDG' 2 '100,000-250,000 SDG' 3 '> 250,000 SDG'
  /water_source 1 'Pipe' 2 'River' 3 'Pump' 4 'Other'
  /prev_info 0 'No' 1 'Yes'
  /knowledge_cat 1 'Poor' 2 'Medium' 3 'Good'
  /attitude_cat 0 'Negative' 1 'Positive'
  /practice_cat 1 'Low' 2 'Moderate' 3 'High'.
EXECUTE.

* Reliability analysis: KAP scales at baseline.
RELIABILITY
  /VARIABLES=k_diarrhea_def k_contam_water k_unwashed_hands k_hwash_toilet
    k_water_alone k_boil_treat k_feces_source k_flies k_transmit
    k_hwash_latrine k_latrine_struct k_ors_prepare k_water_methods_yn
  /SCALE('Knowledge Scale') ALL /MODEL=ALPHA /STATISTICS=DESCRIPTIVE SCALE /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=a_serious_issue a_confident_prev a_family_water a_treat_water
    a_handwash_expose a_soap_effective a_water_container a_hygiene_cause
    a_latrine_privacy a_latrine_night a_latrine_struct2 a_neighbor_latrine
    a_defect_water a_waste_flies
  /SCALE('Attitude Scale') ALL /MODEL=ALPHA /STATISTICS=DESCRIPTIVE SCALE /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=p_hwash_outdoor p_hwash_toilet p_hwash_food_prep
    p_hwash_before_eat p_use_safe_water p_store_water p_see_doctor p_use_ors
  /SCALE('Practice Scale') ALL /MODEL=ALPHA /STATISTICS=DESCRIPTIVE SCALE /SUMMARY=TOTAL.

* Descriptive statistics.
DESCRIPTIVES VARIABLES=age knowledge_score attitude_score practice_score kap_score
  /STATISTICS=MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES=gender edu_level fam_size income occupation water_source
  prev_info knowledge_cat attitude_cat practice_cat diarrhea_hh_yn
  /STATISTICS=MODE /BARCHART PERCENT.

FREQUENCIES VARIABLES=k_diarrhea_def k_contam_water k_unwashed_hands k_hwash_toilet
  k_water_alone k_boil_treat k_feces_source k_flies k_transmit
  k_hwash_latrine k_latrine_struct k_ors_prepare k_water_methods_yn
  /STATISTICS=MEAN.

FREQUENCIES VARIABLES=a_serious_issue a_confident_prev a_family_water a_treat_water
  a_handwash_expose a_soap_effective a_water_container a_hygiene_cause
  a_latrine_privacy a_latrine_night a_latrine_struct2 a_neighbor_latrine
  a_defect_water a_waste_flies
  /STATISTICS=MODE.

FREQUENCIES VARIABLES=p_hwash_outdoor p_hwash_toilet p_hwash_food_prep
  p_hwash_before_eat p_use_safe_water p_store_water p_see_doctor p_use_ors
  obs_hwash_critical obs_waste_disposal obs_latrine_use obs_latrine_clean
  obs_child_feces obs_nails obs_hh_waste
  /STATISTICS=MEAN MODE.

* Spearman correlations between KAP component scores and age.
NONPAR CORR
  /VARIABLES=knowledge_score attitude_score practice_score kap_score age
  /PRINT=SPEARMAN TWOTAIL NOSIG.

* Chi-square: sociodemographic variables vs KAP categories.
CROSSTABS /TABLES=gender BY knowledge_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=edu_level BY knowledge_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=fam_size BY knowledge_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=income BY knowledge_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=occupation BY knowledge_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=gender BY practice_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=edu_level BY practice_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=fam_size BY practice_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=income BY practice_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.
CROSSTABS /TABLES=occupation BY practice_cat /CELLS=COUNT ROW /STATISTICS=CHISQ.

* Multiple linear regression: predictors of composite KAP at baseline.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT kap_score
  /METHOD=ENTER age gender edu_level fam_size income occupation.

* Multiple linear regression: predictors of knowledge score at baseline.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT knowledge_score
  /METHOD=ENTER age gender edu_level fam_size income occupation.

* NOTE: Update the OUTFILE path below before saving.
SAVE OUTFILE='C:\path\to\1_data\cleaned\cleaned_pre.sav' /COMPRESSED.
EXECUTE.
