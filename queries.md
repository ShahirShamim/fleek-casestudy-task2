# BigQuery Queries

This document contains a log of all the SQL queries generated for the Fleek Case Study. 
Each query is formatted so you can easily copy and paste it into the BigQuery console.

---

## 1. Summary of case_study_activation_dataset

### A. Data Completeness (Null & Non-Null Counts)
This query gives you a high-level view of how many missing values exist in each column.

```sql
SELECT
  COUNT(*) as total_users,
  COUNT(country) as country_filled,
  COUNT(signup_date) as signup_date_filled,
  COUNT(buyer_persona) as buyer_persona_filled,
  COUNT(is_email_reachable) as email_reachable_filled,
  COUNT(is_push_reachable) as push_reachable_filled,
  COUNT(onboarding_completed) as onboarding_filled,
  COUNT(user_intent) as intent_filled,
  COUNT(reselling_platform) as reselling_platform_filled,
  COUNT(has_existing_store) as existing_store_filled,
  COUNT(num_selected_categories) as selected_categories_filled,
  COUNT(first_order_date) as first_order_date_filled,
  COUNT(first_order_value) as first_order_value_filled,
  COUNT(second_order_date) as second_order_date_filled,
  COUNT(total_orders) as total_orders_filled,
  COUNT(total_gmv) as total_gmv_filled
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`;
```

**Output:**
```text
total_users	country_filled	signup_date_filled	buyer_persona_filled	email_reachable_filled	push_reachable_filled	onboarding_filled	intent_filled	reselling_platform_filled	existing_store_filled	selected_categories_filled	first_order_date_filled	first_order_value_filled	second_order_date_filled	total_orders_filled	total_gmv_filled
167554	122700	167554	12154	167554	167554	167554	42852	32930	77334	73375	12154	12154	5075	167554	167554
```

### B. Unique Value Counts for Categorical Columns
Run these individually to see the breakdown of users across different categorical attributes.

#### 1. Country breakdown
```sql
SELECT country, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY country 
ORDER BY user_count DESC;
```
**Output:**
```text
country	user_count
United Kingdom	45323
	44854
France	17809
United States	12421
Germany	9577
Italy	7428
Portugal	6052
Poland	3158
Netherlands	2310
Belgium	2030
Sweden	1436
Australia	1414
Ireland	1405
Finland	1101
Pakistan	1086
Czech Republic	890
Spain	867
Austria	862
Romania	582
Canada	488
Switzerland	454
Slovakia	446
Denmark	406
Hungary	371
Norway	363
Lithuania	293
Philippines	288
Greece	248
New Zealand	244
Luxembourg	202
Croatia	195
Czechia	190
Chile	190
Latvia	184
India	156
Israel	146
Slovenia	129
Estonia	129
Singapore	124
Mexico	123
Japan	105
South Africa	95
Reunion	74
Argentina	74
Georgia	62
Bulgaria	57
United Arab Emirates	53
Saudi Arabia	51
Peru	50
Malaysia	45
Brazil	44
Morocco	41
Turkey	38
Cyprus	37
Iceland	36
Russia	35
Indonesia	31
Malta	30
Nigeria	27
Thailand	25
Ukraine	24
Algeria	23
Guadeloupe	19
"Korea, Republic of"	18
Colombia	18
China	18
Nepal	17
Kuwait	14
Puerto Rico	14
Jamaica	14
Costa Rica	12
Albania	12
Lebanon	12
Viet Nam	12
Egypt	10
Qatar	9
Uruguay	9
Panama	9
"Taiwan, Province of China"	9
Trinidad and Tobago	9
Kenya	8
Martinique	8
Zambia	8
"Macedonia, The Former Yugoslav Republic of"	7
Hong Kong	7
Jordan	7
Belarus	7
Maldives	7
"Moldova, Republic of"	6
Paraguay	6
Iraq	6
Myanmar	6
Senegal	6
Mongolia	6
Serbia	6
Bosnia and Herzegovina	6
Bahrain	6
Ghana	6
Botswana	6
Armenia	5
Fiji	5
Afghanistan	5
Ecuador	5
Angola	5
French Guiana	5
Tunisia	5
Kazakhstan	4
Cambodia	4
Guatemala	4
Somalia	4
Bangladesh	4
Gabon	4
Dominican Republic	4
El Salvador	4
Oman	4
Haiti	4
Azerbaijan	4
Belize	3
Zimbabwe	3
Honduras	3
Brunei Darussalam	3
Suriname	3
Bolivia	3
Cameroon	3
Uganda	3
Aruba	3
Gibraltar	2
Ethiopia	2
Sri Lanka	2
"Congo, The Democratic Republic of the"	2
Seychelles	2
Madagascar	2
Papua New Guinea	2
Namibia	2
French Polynesia	2
Central African Republic	2
Comoros	2
Sao Tome And Principe	1
Northern Mariana Islands	1
Liechtenstein	1
Guernsey	1
Sierra Leone	1
Mozambique	1
Congo	1
"Tanzania, United Republic of"	1
Mali	1
Macao	1
French Southern Territories	1
Liberia	1
Venezuela	1
Côte d'Ivoire	1
Isle of Man	1
Bahamas	1
Moldova	1
Åland Islands	1
Burkina Faso	1
Uzbekistan	1
Burundi	1
Saint Lucia	1
"Iran, Islamic Republic Of"	1
Vanuatu	1
Guyana	1
Gambia	1
Mauritius	1
Malawi	1
Cote D'Ivoire	1
"Virgin Islands, U.S."	1
Cayman Islands	1
South Korea	1
Cuba	1
New Caledonia	1
Syrian Arab Republic	1
```

#### 2. Buyer Persona breakdown
```sql
SELECT buyer_persona, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY buyer_persona 
ORDER BY user_count DESC;
```
**Output:**
```text
buyer_persona	user_count
	155400
Reseller	12154
```

#### 3. Reachability & Onboarding
```sql
SELECT is_email_reachable, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY is_email_reachable;
```
**Output:**
```text
is_email_reachable	user_count
true	120244
false	47310
```

```sql
SELECT is_push_reachable, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY is_push_reachable;
```
**Output:**
```text
is_push_reachable	user_count
false	121552
true	46002
```

```sql
SELECT onboarding_completed, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY onboarding_completed;
```
**Output:**
```text
onboarding_completed	user_count
false	99743
true	67811
```

#### 4. User Intent
```sql
SELECT user_intent, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY user_intent 
ORDER BY user_count DESC;
```
**Output:**
```text
user_intent	user_count
	124702
TO_EARN_EXTRA_MONEY	24385
TO_EXPLORE	10899
TO_GROW	5797
TO_SHARE_STYLE	1771
```

#### 5. Reselling Platform
```sql
SELECT reselling_platform, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY reselling_platform 
ORDER BY user_count DESC;
```
**Output:**
```text
reselling_platform	user_count
	134624
VINTED	22758
OTHERS	7390
DEPOP	2537
WEBSITE	245
```

#### 6. Existing Store
```sql
SELECT has_existing_store, COUNT(*) as user_count 
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY has_existing_store;
```
**Output:**
```text
has_existing_store	user_count
	90220
false	51794
true	25540
```


### C. Distribution & Summary of Numeric/Date Columns
This query summarizes minimums, maximums, and averages for the continuous variables to understand the spread.

```sql
SELECT
  -- Dates
  MIN(signup_date) as first_signup,
  MAX(signup_date) as last_signup,
  MIN(first_order_date) as first_order_made_on,
  MAX(first_order_date) as last_first_order_made_on,
  
  -- Order Values & GMV
  ROUND(AVG(first_order_value), 2) as avg_first_order_value,
  MAX(first_order_value) as max_first_order_value,
  ROUND(AVG(total_gmv), 2) as avg_total_gmv,
  MAX(total_gmv) as max_total_gmv,
  
  -- Orders & Categories
  ROUND(AVG(total_orders), 2) as avg_total_orders,
  MAX(total_orders) as max_total_orders,
  ROUND(AVG(num_selected_categories), 2) as avg_selected_categories,
  MAX(num_selected_categories) as max_selected_categories
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`;
```

**Output:**
```text
first_signup	last_signup	first_order_made_on	last_first_order_made_on	avg_first_order_value	max_first_order_value	avg_total_gmv	max_total_gmv	avg_total_orders	max_total_orders	avg_selected_categories	max_selected_categories
2025-10-01	2026-02-13	2025-10-01	2026-03-31	160.8	7573.58	27.15	10673.3	0.13	89	3.99	5
```

---

*(Future queries will be added below this line)*

## 2. Deep Dive: Unonboarded Users & Country Differences

### A. What data do we have on Unonboarded vs Onboarded users?
This query checks if we can actually reach the unonboarded users via email, and whether they dropped off before or after giving us info like their country or intent.

```sql
SELECT 
  onboarding_completed,
  COUNT(*) as total_users,
  SUM(CAST(is_email_reachable AS INT64)) as email_reachable_count,
  SUM(CAST(is_push_reachable AS INT64)) as push_reachable_count,
  COUNT(country) as have_country_data,
  COUNT(user_intent) as have_intent_data
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
GROUP BY onboarding_completed;
```

**Output:**
```text
onboarding_completed	total_users	email_reachable_count	push_reachable_count	have_country_data	have_intent_data
false	99743	58087	19754	60014	5260
true	67811	62157	26248	62686	37592
```

### B. Meaningful Differences in Top Countries
Looking at the top 6 most popular countries to see if there are major differences in how likely they are to onboard, convert, or spend. *(Note: avg_gmv_per_buyer uses NULLIF to only average across users who actually spent money)*.

```sql
SELECT 
  country,
  COUNT(*) as total_users,
  ROUND(SUM(CAST(onboarding_completed AS INT64)) / COUNT(*) * 100, 2) as onboarding_rate_pct,
  ROUND(COUNT(first_order_date) / COUNT(*) * 100, 2) as conversion_rate_pct,
  ROUND(AVG(first_order_value), 2) as avg_first_order_value,
  ROUND(AVG(NULLIF(total_gmv, 0)), 2) as avg_gmv_per_buyer
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
WHERE country IN ('United Kingdom', 'France', 'United States', 'Germany', 'Italy', 'Portugal')
GROUP BY country
ORDER BY total_users DESC;
```

**Output:**
```text
country	total_users	onboarding_rate_pct	conversion_rate_pct	avg_first_order_value	avg_gmv_per_buyer
United Kingdom	45323	54.48	10.35	130.36	355.97
France	17809	45.52	10.15	202.62	482.63
United States	12421	57.56	2.86	258.19	650.49
Germany	9577	43.76	13.17	183.86	458.7
Italy	7428	51.49	6.07	177.36	325.19
Portugal	6052	47.72	7.06	189.74	295.12
```

## 3. Deep Dive: The US Segment & Time to Conversion

### A. US Users by Intent
Why are US users onboarding but not buying? Let's check their self-reported intent to see if they are just "exploring".

```sql
SELECT 
  user_intent,
  COUNT(*) as total_us_users,
  ROUND(COUNT(first_order_date) / COUNT(*) * 100, 2) as conversion_rate_pct
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
WHERE country = 'United States' AND onboarding_completed = true
GROUP BY user_intent
ORDER BY total_us_users DESC;
```

**Output:**
```text
user_intent	total_us_users	conversion_rate_pct
TO_EXPLORE	2517	0.6
	2378	5.76
TO_EARN_EXTRA_MONEY	1295	1.39
TO_SHARE_STYLE	515	2.52
TO_GROW	444	3.38
```

### B. Time to First Purchase (Time-to-Value)
For users who actually place an order, how many days does it take them from the moment they sign up? This dictates our CRM sequence timing.

```sql
SELECT 
  DATE_DIFF(DATE(first_order_date), DATE(signup_date), DAY) as days_to_first_order,
  COUNT(*) as number_of_users
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
WHERE first_order_date IS NOT NULL
GROUP BY days_to_first_order
ORDER BY number_of_users DESC
LIMIT 15;
```

**Output:**
```text
days_to_first_order	number_of_users
0	4782
1	1585
2	717
3	489
4	423
5	332
6	277
7	257
8	174
9	155
10	131
12	119
13	109
15	109
11	107
```

### C. When did the "Email Reachable, Unonboarded" users sign up?
Are these 58k users fresh leads or stale leads from months ago? Let's group them by signup month.

```sql
SELECT 
  DATE_TRUNC(DATE(signup_date), MONTH) as signup_month,
  COUNT(*) as unonboarded_reachable_users
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
WHERE onboarding_completed = false AND is_email_reachable = true
GROUP BY signup_month
ORDER BY signup_month DESC;
```

**Output:**
```text
signup_month	unonboarded_reachable_users
2026-02-01	5311
2026-01-01	18899
2025-12-01	8504
2025-11-01	11485
2025-10-01	13888
```

## 4. Deep Dive: France & Germany Onboarding Drop-off

### A. At what step are they dropping out?
By looking at what data is `NULL` for users who *did not* complete onboarding, we can deduce exactly which screen caused them to close the app. We'll compare France and Germany against the UK and US.

```sql
SELECT 
  country,
  COUNT(*) as unonboarded_users,
  ROUND(COUNT(user_intent) / COUNT(*) * 100, 2) as pct_reached_intent_screen,
  ROUND(COUNT(has_existing_store) / COUNT(*) * 100, 2) as pct_reached_store_question,
  ROUND(COUNT(reselling_platform) / COUNT(*) * 100, 2) as pct_reached_platform_question
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
WHERE onboarding_completed = false
  AND country IN ('France', 'Germany', 'United Kingdom', 'United States')
GROUP BY country
ORDER BY unonboarded_users DESC;
```

**Output:**
```text
country	unonboarded_users	pct_reached_intent_screen	pct_reached_store_question	pct_reached_platform_question
United Kingdom	20631	8.95	16.18	5.68
France	9703	6.42	14.35	5.82
Germany	5386	6.15	11.07	3.23
United States	5272	13.75	19.31	4.89
```

### B. Are the Unonboarded FR/DE users reachable?
If we are going to build a localized CRM campaign to win them back, we need to know if they gave us their email before bouncing.

```sql
SELECT 
  country,
  COUNT(*) as unonboarded_users,
  ROUND(SUM(CAST(is_email_reachable AS INT64)) / COUNT(*) * 100, 2) as pct_email_reachable
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
WHERE onboarding_completed = false
  AND country IN ('France', 'Germany', 'United Kingdom', 'United States')
GROUP BY country
ORDER BY unonboarded_users DESC;
```

**Output:**
```text
country	unonboarded_users	pct_email_reachable
United Kingdom	20631	87.46
France	9703	89.81
Germany	5386	85.41
United States	5272	94.65
```
