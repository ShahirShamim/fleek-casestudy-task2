# CRM Initiatives

This document outlines the three core CRM initiatives to drive buyer activation. Any updates to the scope, content, or monitoring of these initiatives should be recorded here.

## 1. Onboarding Email Reachables (App Install Push)
**Objective:** Drive app downloads and initial logins. Since onboarding happens exclusively in the app, these users have likely signed up via web but failed to install the mobile app.

### Why This Makes Sense (Data Rationale)
- **Massive Churn:** 59.5% of all signups (99,743 users) drop off before completing onboarding. Because onboarding is app-only, this represents a massive gap between web signups and app installs.
- **High Reachability:** We have valid email addresses for 58,087 of these abandoned users, providing a direct and free channel to win them back.
- **Fresh Leads:** Over 24,000 of these unonboarded, reachable users signed up in just the last 6 weeks (Jan-Feb 2026), meaning the brand is still fresh in their minds. Recovering just 5% of this segment could yield ~£464,000 in early GMV.

### Data Scope
- **Target Audience:** Users with `onboarding_completed = false` AND `is_email_reachable = true`.
- **Audience Size:** ~58,000 users.
- **Personalization Data:** 
  - `country` (if available, ~60k have this) for localization (e.g., French/German translations).
  - `signup_date` to segment by freshness (prioritize the ~24k users from the last 6 weeks).
  - `product_recommendations` based on purchases by similar users (segment users based on their `user_intent`, `reselling_platform`, `has_existing_store`, `region`)

### Possible Content
- **Subject Lines:** "Download the Fleek app to start sourcing", "Your wholesale vintage access is waiting."
- **Body:** 
  - Remind them of the value proposition (access to wholesale vintage).
  - **Core CTA:** A prominent, direct link to the App Store / Google Play Store to download the app.
  - *Localized Variants:* For FR/DE, assure them about local shipping or translate the email to native languages. For the US, emphasize the ease of exploring the catalog.

### Content Channels
- **Primary:** Email (since they are verified `is_email_reachable`).
- **Secondary:** Push Notifications (if `is_push_reachable` is true, roughly 19k of this cohort).

### Monitoring Outcomes
- **Primary KPI:** Onboarding Completion Rate (aiming to increase the baseline 40%).
- **Secondary KPIs:** Email Open Rate, Click-Through Rate, and Cost per Reactivation.
- **Company Metric Linkage:** 
  - **CAC Efficiency:** By reactivating users who have already been acquired (marketing spend is already sunk), any converted user dramatically lowers the blended Customer Acquisition Cost (CAC).
  - **Pipeline GMV:** Moving users out of the "ghost" phase directly expands the addressable audience for future revenue.

---

## 2. Frontload TTV (Time-to-Value) Sequences
**Objective:** Compress the welcome sequence to secure the first purchase within the critical 72-hour window.

### Why This Makes Sense (Data Rationale)
- **The "Window Shopper" Problem:** 82% of users who successfully complete onboarding never go on to make a purchase (55,657 users). 
- **The 72-Hour Cliff:** Data shows that when users *do* buy, they buy quickly. 39% of all first conversions happen on Day 0, and 62% happen by Day 3. 
- **Conclusion:** If a user is not converted within the first 72 hours, their likelihood of ever converting drops drastically. We must front-load our best offers and highest-value content immediately.

### Data Scope
- **Target Audience:** Users with `onboarding_completed = true` AND `first_order_date` IS NULL.
- **Audience Size:** ~55,600 users.
- **Personalization Data:**
  - `user_intent` (e.g., "TO_EXPLORE" vs "TO_EARN_EXTRA_MONEY").
  - `reselling_platform` (e.g., Vinted vs Depop) to tailor the "what to buy" recommendations.
  - Hours since signup (triggering at Hour 1, Hour 24, Hour 72).

### Possible Content
- **Day 0 (Welcome):** Focus on ease of use, top-selling beginner products, and perhaps a 10% welcome discount valid for 72 hours.
- **Day 1 (Social Proof):** "How sellers are making £££ on Vinted with Fleek products."
- **Day 2-3 (Urgency):** "Your welcome discount expires tomorrow. Here are our top picks for you."

### Content Channels
- **Primary:** Email.
- **Secondary:** In-App banners/modals emphasizing the 72-hour offer. Push notifications for urgency.

### Monitoring Outcomes
- **Primary KPI:** First Purchase Rate (specifically the Day 0 - Day 3 conversion volume).
- **Secondary KPIs:** Time-to-First-Purchase (reducing the average days) and First Order GMV.
- **Company Metric Linkage:** 
  - **LTV Predictor:** Users who buy within the first 72 hours typically exhibit a much higher 12-month Customer Lifetime Value (LTV) than delayed purchasers.

---

## 3. First order -> Second order push
**Objective:** Drive "True Activation" by ensuring a first-time buyer returns for a second purchase.

### Why This Makes Sense (Data Rationale)
- **The "One-and-Done" Churn:** 58.3% of users who make their first purchase (7,079 users) never return to make a second order.
- **True Activation:** The data indicates that users are not truly "activated" until they build a habit with a second order. 
- **Revenue Impact:** Since the average first order is ~£160, getting these 7,000+ "one-and-done" buyers to make just one more purchase represents over £1.13 Million in lost potential GMV.

### Data Scope
- **Target Audience:** Users with `first_order_date` IS NOT NULL AND `second_order_date` IS NULL.
- **Audience Size:** ~7,000 "one-and-done" users.
- **Personalization Data:**
  - Items purchased in the first order (for cross-pollination recommendations).
  - Delivery date of the first order (to trigger post-purchase nurture at the exact right moment).
  - `first_order_value` (to segment high-rollers from budget testers).

### Possible Content
- **Delivery Day (The Win):** "Your first order has arrived! Here's how to list it for maximum profit." Ask for an unboxing photo or review.
- **Day 7 Post-Delivery (The Bounce-Back):** "Ready for your next haul? Here is a secret 15% off code for your second order."
- **Day 14 Post-Delivery (Cross-Sell):** "Since you bought Vintage Tees, check out these Vintage Denim products."

### Content Channels
- **Primary:** Email + Push notifications (e.g., "Your bounce-back offer is waiting").

### Monitoring Outcomes
- **Primary KPI:** True Activation Rate (increasing the percentage of first-time buyers who make a second purchase from 41.7% to 50%+).
- **Secondary KPIs:** Days between Order 1 and Order 2, and Second Order GMV.
- **Company Metric Linkage:** 
  - **Customer Lifetime Value (LTV):** The second purchase is the single biggest inflection point for LTV. Once a buyer makes order #2, their long-term retention curve flattens out, driving compounding monthly recurring GMV.

---
## What comes first?
If only one initiative can be chosen for the first 90 days, **Initiative 1 (Onboarding Email Reachables)** is the undeniable priority. Here is the rationale:
1. **The Math (Volume & Cascade Effect):** The onboarding drop-off is our single largest leak (60% / 99k users). Any improvement here mathematically cascades down to the rest of the funnel. If we don't widen the top of the funnel, Initiatives 2 and 3 will always be starved for volume.
2. **Instant ROI on Sunk Costs:** The marketing team has already paid to acquire these 58,000 email-reachable users. Activating them requires zero new ad spend, meaning every conversion is pure upside that instantly improves blended Customer Acquisition Cost (CAC).
3. **The Ticking Clock (Lead Decay):** Over 24,000 of these users signed up in just the last 6 weeks. If we wait another quarter to address this, these warm leads will go completely cold and become impossible to reactivate. 
4. **Speed-to-Market:** Launching a "Finish Setup" email drip is a purely CRM-driven intervention. It requires almost zero product or engineering changes, making it the fastest initiative to deploy.

---