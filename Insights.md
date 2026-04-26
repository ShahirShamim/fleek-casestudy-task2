# Activation Insights

Based on the high-level summary of the `case_study_activation_dataset` (167,554 total users), here are the initial insights:

## The 3 Biggest Funnel Leakages (Quantified)

### Leak 1: The Onboarding Drop-off (Top of Funnel)
- **The Leak:** 99,743 users sign up but never finish onboarding.
- **The Quantification:** This represents a massive **59.5% churn rate** before a user even sees the core product. Of these, 58,087 are email reachable. If we recovered just a conservative 5% of these reachable users (2,904 users) and they spent the average first-order value (£160), that is **~£464,000 in uncaptured early GMV**.

### Leak 2: The "Window Shoppers" (First Purchase Drop-off)
- **The Leak:** 55,657 users complete onboarding but never make a purchase.
- **The Quantification:** Out of 67,811 users who successfully finish setting up their accounts, only 12,154 go on to buy. This is an **82% drop-off rate for onboarded users**. The app is acquiring high-intent users, but failing to convert them to paying customers within the first crucial days.

### Leak 3: Activation Failure (The "One-and-Done" Buyers)
- **The Leak:** 7,079 buyers make their first purchase but never return for a second (which is our definition of a fully "Activated" user).
- **The Quantification:** Out of 12,154 first-time buyers, only 5,075 (41.7%) make a repeat purchase and become fully Activated. That means **58.3% of acquired buyers churn before reaching Activation**. Since the average first order value is ~£160, getting these 7,079 one-and-done users to make just *one* more average-sized purchase represents **over £1.13 Million in lost potential GMV**.

---

## 1. The Onboarding Drop-off is Massive
- **99,743 users (60%)** have `onboarding_completed` = false.
- **67,811 users (40%)** have completed onboarding.
- **Insight:** The biggest immediate bottleneck in the funnel is getting users through the onboarding flow. If they don't onboard, they likely aren't browsing or buying. 

## 2. Order Conversion is Low, and True Activation is Even Harder
- Only **12,154 users (7.2%)** make a first order.
- Of those who buy once, only **5,075 users (41.7%)** go on to make a second order (True Activation).
- **Insight:** Getting the first purchase is difficult, but the real challenge is driving them to the second order. The CRM strategy must focus not just on the first purchase, but heavily on the post-purchase nurture to drive that critical second sale.

## 3. Communication Channels
- **Email is strong:** 120,244 users (72%) are email reachable.
- **Push is weak:** Only 46,002 users (27%) are push reachable.
- **Insight:** Early activation campaigns must heavily rely on Email. Push notifications can be a secondary channel for the subset that opted in.

## 4. User Demographics & Intent
- **Top Countries:** UK (~45k), France (~17.8k), US (~12.4k), Germany (~9.5k), Italy (~7.4k). However, ~44.8k users have a blank country.
- **Motivation:** Where known, "TO_EARN_EXTRA_MONEY" (24.3k) and "TO_EXPLORE" (10.8k) are the main drivers.
- **Platforms:** Vinted dominates the known reselling platforms (22.7k), followed by Depop (2.5k).

## 5. A Data Quirk to Investigate
- Exactly 12,154 users have a `buyer_persona` filled out, which is the *exact same number* of users who have a `first_order_date`. 
- **Assumption:** It seems `buyer_persona` might only be assigned once a user actually places an order, meaning we can't use it to predict behavior for new signups.

## 6. Deep Dive: Unonboarded Users
- **Massive CRM Win-back Opportunity:** Out of the 99,743 unonboarded users, **58,087 are email reachable**. This is a huge, untapped pool of users to re-engage.
- **Where they drop off:** 60,014 of the unonboarded users *do* have country data, but only 5,260 have intent data. This pinpoints the exact UX bottleneck: users are churning **between the country selection screen and the intent selection screen**. 

## 7. Deep Dive: Geographic Nuances
- **The USA anomaly (High Intent, Low Conversion):** US users have the highest onboarding completion rate (57.56%) but the **lowest conversion rate (2.86%)**. However, when a US user *does* convert, they are extremely valuable, spending an average of **£650 GMV** (the highest of any top country).
- **Germany is highly efficient:** German users have the lowest onboarding rate (43.76%) among top countries, but they have the **highest conversion rate (13.17%)**. 
- **UK & France form the reliable core:** Both convert steadily at ~10%. France is particularly lucrative, with buyers spending an average of £482 GMV compared to the UK's £356.

---

## 8. Deep Dive: The US Anomaly
- **Why do they onboard but not buy?** The #1 intent for US users is `TO_EXPLORE` (2,517 users), and they have a near-zero conversion rate (0.6%). The US cohort is heavily skewed towards "window shoppers" rather than serious resellers. 

## 9. Deep Dive: Time-to-Value (TTV)
- **Speed is everything:** Out of the 12k total conversions, **4,782 (39%) happen on Day 0**. By Day 3, over **62%** of all conversions have occurred.
- **Insight:** The CRM onboarding sequence must be front-loaded. If a user doesn't buy within the first 72 hours, their likelihood of converting drops off a cliff.

## 10. Deep Dive: The Unonboarded Backlog
- **Fresh Leads:** The 58k email-reachable unonboarded users are not just old, stale leads. Over **24,000** of them signed up in January and February 2026. 
- **France & Germany Drop-offs:** Unonboarded users in FR and DE drop off earlier in the flow than US/UK users (only ~6% even reach the intent screen). However, they are highly email reachable (~85-90%). A localized translation of the onboarding flow or CRM emails is an easy win.

---

### Conclusion & Moving to Strategy
We now have a complete picture of the funnel:
1. **The Leak:** 60% drop off during onboarding.
2. **The Window:** We have ~3 days to convert them once they do onboard.
3. **The Goldmine:** 58k highly reachable, relatively fresh leads sitting in the unonboarded bucket.
4. **The Nuance:** The US has high intent to explore but low intent to buy; FR/DE have friction in onboarding but convert well once through.
