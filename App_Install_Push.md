# App Install Push (Initiative 1)

**Objective:** Drive app downloads and initial logins. Since onboarding happens exclusively in the app, these users have likely signed up via web but failed to install the mobile app.

## 1. Why This Makes Sense (Data Rationale)
- **Massive Churn:** 59.5% of all signups (99,743 users) drop off before completing onboarding. Because onboarding is app-only, this represents a massive gap between web signups and app installs.
- **The Reachability Reality (Email vs. Push Notifications):** At this specific stage in the funnel, the user has signed up via the web but has *not* completed onboarding (which is app-exclusive). This means they likely have not downloaded the app, making their mobile Push Notification (PN) reachability essentially 0%. We cannot send them an in-app message or a push notification to download the app they haven't installed yet. However, because their email was captured during the initial web registration step, we have valid `is_email_reachable` addresses for 58,087 of these abandoned users. Email is the *only* viable, owned channel to bridge the gap between web-signup and app-installation. Once activated and onboarded, we can request PN permissions and transition them to push notifications for downstream retention, but for this initial activation push, email is structurally mandatory.
- **Fresh Leads:** Over 24,000 of these unonboarded, reachable users signed up in just the last 6 weeks (Jan-Feb 2026), meaning the brand is still fresh in their minds. Recovering just 5% of this segment could yield ~£464,000 in early GMV.

## 2. Data Scope & Audience
- **Target Audience:** Users with `onboarding_completed = false` AND `is_email_reachable = true`.
- **Audience Size:** ~58,000 users.
- **Personalization Data:** 
  - `country` (if available, ~60k have this) for localization (e.g., French/German translations).
  - `signup_date` to segment by freshness (prioritize the ~24k users from the last 6 weeks).
  - `product_recommendations` based on purchases by similar users (segment users based on their `user_intent`, `reselling_platform`, `has_existing_store`, `region`).

## 3. Content & Channels
- **Primary Channel:** Email (since they are verified `is_email_reachable`).

### Message Framework
- **Subject Lines:** "Download the Fleek app to start sourcing", "Your wholesale vintage access is waiting."
- **Body Content:** 
  - Remind them of the value proposition (access to wholesale vintage).
  - **Core CTA:** A prominent, direct link to the App Store / Google Play Store to download the app.
  - *Localized Variants:* For FR/DE, assure them about local shipping or translate the email to native languages. For the US, emphasize the ease of exploring the catalog.

## 4. Monitoring Outcomes
- **Primary KPI:** Onboarding Completion Rate (aiming to increase the baseline 40%).
- **Secondary KPIs:** Email Open Rate, Click-Through Rate, and Cost per Reactivation.
- **Company Metric Linkage:** 
  - **CAC Efficiency:** By reactivating users who have already been acquired (marketing spend is already sunk), any converted user dramatically lowers the blended Customer Acquisition Cost (CAC).
  - **Pipeline GMV:** Moving users out of the "ghost" phase directly expands the addressable audience for future revenue.

---

## 5. Execution Plan & A/B Testing
To rigorously measure the impact of dynamic personalization versus a straightforward incentive (£20 off first app order), we will divide the ~58,000 target users into four distinct cohorts.

### Cohort Split & Email Delivery
- **Standard Timing:** For new signups, a single email will be triggered exactly **+24 Hours** after web registration.
- **Fresh Leads Catch-up:** For the ~24k existing fresh leads, the email will be sent on the first available date. The specific delivery time will be dynamically assigned based on the median ordering time of similar converting customers.

The content varies by cohort:

1. **Global Control (10% - Holdout):** Does not receive this CRM push. This establishes the baseline organic app download and onboarding completion rate.
2. **Active Control - Value Prop Only (30%):** 
   - **Content:** Standard reminder to download the app to access wholesale vintage. 
   - **Details:** NO mention of a discount, NO product imagery. Just the core value proposition and app store links.
3. **Group A - Incentive + Product Recs (30%):** 
   - **Content:** Core incentive (£20 off first app order) *plus* a random assortment of active product recommendations.
   - **Details:** Highlights the £20 offer prominently, followed by a randomized visual catalog of 4 active products to showcase inventory breadth without complex targeting.
4. **Group B - Incentive Only (30%):** 
   - **Content:** Core incentive (£20 off first app order) without any specific product imagery.
   - **Details:** Text/banner heavily focused on the £20 off offer and the App Store CTA. NO catalogue distractions.

### Experiment Hypothesis
We expect both Group A and Group B to significantly outperform the Active Control in Click-Through-to-Install rates due to the financial incentive. The core questions this test seeks to answer are:
1. **Baseline Uplift:** How much does an active email push (Active Control) lift install rates over doing nothing (Global Control)?
2. **Incentive Impact:** How much does the £20 discount (Groups A & B) lift conversion over a standard reminder (Active Control)?
3. **Catalogue vs. Focused Offer (Group A vs Group B):** Does visualizing the actual vintage inventory alongside the discount bridge the intent gap, or is the user overwhelmed/distracted by the catalogue being present at this early stage?

### Statistical Rigor & Test Duration
To ensure our findings are robust and not subject to random variance, the experiment is governed by strict statistical parameters:
*   **Sample Size & MDE:** With a baseline organic install rate of ~5.2%, detecting a 15% relative uplift with 80% statistical power and a 95% confidence interval requires approximately **14,500 users per cohort**. Across our 4 cohorts, this means we must accumulate and send roughly **58,000 total emails** before we can declare a statistically significant winner. We will not halt the test prematurely until this sample threshold is met.
*   **Test Duration:** Given our daily signup volume and the required sample size per cohort, we estimate it will take exactly 14 to 21 days of continuous cohort accumulation to reach statistical significance. The test will run strictly for this pre-calculated duration to avoid the "peeking problem."
*   **Confidence Intervals:** When reporting final results to leadership (e.g., "+ £3.85 Incremental GMV / User"), all core metrics will be presented alongside 95% Confidence Intervals (e.g., +£3.85 ± £0.42). This accurately reflects the margin of error and the certainty of the financial uplift before we permanently alter the default Web-to-App onboarding flow.

## 6. Technical Architecture (Cron & Data Pipeline)
To fully automate this campaign, we will implement a daily CRON job that orchestrates the segmentation, assignment, and tracking lifecycle.

### Daily Processing (Every Morning)
1. **Target Isolation:** The script isolates users who signed up in the past 24 hours but have not yet installed the app/onboarded.
2. **Cohort Assignment:** These isolated users are randomly assigned to one of the four experimental cohorts (Global Control, Active Control, Group A, Group B).
3. **Product Matching & API Hydration:** Users assigned to receive products are dynamically matched with product IDs using "closest match" logic. The script then immediately hits the internal Fleek Product API (e.g., `GET /api/v1/products?ids=...`) to "hydrate" those raw IDs with live image URLs, product names, and pricing, ensuring no out-of-stock items are pushed.
4. **Dynamic Localization & News Injection:** The script fetches the latest country-specific news headlines regarding fashion, sustainability, vintage clothing, or Vinted selling. An LLM step generates a personalized, dynamic introductory hook and translates the email copy into the user's native language (e.g., French for FR, German for DE).
5. **Template Rendering:** The script injects the hydrated product data and localized LLM copy into the designated HTML template (Group A, Group B, or Active Control) for that user.
6. **Email Delivery via Resend:** As the final outbound step, the script dispatches the fully rendered HTML email payloads via the **Resend API**, scheduling the delivery to perfectly match the user's initial signup time (e.g., a 2:00 PM signup receives the email exactly at 2:00 PM the following day).
7. **State Logging:** The script pushes the user details, cohort assignment, product IDs, and generated email content payloads into a dedicated tracking table in BigQuery.

## 7. Monitoring & Tracking Success Metrics

To rigorously evaluate the success of the CRM Activation Initiative, the daily CRON job loops back over users who have previously received the campaign and updates their BigQuery records with downstream conversion events. This creates a closed-loop data pipeline that automatically tracks our A/B test results and monitors GMV and CAC efficiency in near real-time.

### Key Performance Indicators (KPIs)

*   **Primary Metric (Activation):** The percentage of targeted users who successfully initiate and complete the in-app onboarding flow (transitioning from web-signup to fully active app user).
*   **Secondary Metric (Time to First Purchase):** The average or median duration (in hours/days) between the email delivery timestamp and the user completing their first order. Shorter times indicate higher intent capture.
*   **Tertiary Metric (Marginal Revenue Per User):** The incremental Gross Merchandise Value (GMV) generated per user in the experimental cohort minus the baseline GMV of the Global Control, factored against the cost of the £20 promo code liability.
### Guardrails & Counter Metrics
To ensure this activation strategy doesn't negatively impact long-term brand equity or audience health, we will closely monitor:
*   **Unsubscribe & Complaint Rate:** Tracking if the £20 incentive or the rapid 24-hour cadence causes a statistically significant spike in spam complaints or opt-outs compared to the Active Control.
*   **Email Fatigue (Frequency Impact):** Monitoring whether receiving this early activation push cannibalizes the open and click rates of downstream, organic marketing emails (e.g., measuring 30-day email engagement post-activation).
*   **Long-Term Retention Degradation:** Tracking the 90-day active purchasing behavior of users activated via the £20 incentive. If Group A and B users churn immediately after exhausting the promotional credit (indicating low LTV), the initial MRPU gains are illusory, and the incentive strategy must be re-evaluated.

### Tracking Schema: `crm_activation_log`
Every time the daily pipeline runs, it inserts a record into the tracking table for the user. Subsequent CRON runs update the downstream columns (`app_installed`, `first_order_placed`, etc.) when the events occur.

| `user_id` | `assigned_cohort` | `locale` | `sent_at` | `email_opened_at` | `link_clicked_at` | `app_installed` | `first_order_placed` | `gmv_first_order` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `1288` | `group_a` | `FR` | `2024-05-15 14:00:00` | `2024-05-15 14:15:22` | `2024-05-15 14:18:05` | `TRUE` | `TRUE` | `£125.00` |
| `1492` | `group_b` | `EN` | `2024-05-15 16:30:00` | `2024-05-15 18:45:10` | `NULL` | `FALSE` | `FALSE` | `£0.00` |
| `9881` | `active_control` | `DE` | `2024-05-16 09:15:00` | `NULL` | `NULL` | `FALSE` | `FALSE` | `£0.00` |
| `1021` | `global_control` | `EN` | `NULL` | `NULL` | `NULL` | `TRUE` | `FALSE` | `£0.00` |

### Initiative Reporting: Cohort Evaluation
Success is measured by comparing the cumulative performance of each cohort against the `global_control` (baseline organic behavior) and the `active_control` (baseline email behavior).

| Cohort | Targeted Users | Install Rate | 7-Day Order Rate | Unsubscribe Rate | Incremental GMV / User |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Global Control** (No Email) | 10,000 | 5.2% | 1.8% | N/A | baseline |
| **Active Control** (Value Prop) | 10,000 | 8.5% | 2.5% | 0.8% | + £1.20 |
| **Group A** (Incentive + Recs) | 10,000 | **14.2%** | **4.9%** | 1.1% | **+ £3.85** |
| **Group B** (Incentive Only) | 10,000 | 12.8% | 3.2% | 0.9% | + £2.50 |

**Evaluation Criteria:** If Group A or Group B yields a statistically significant uplift in Incremental GMV / User that offsets the cost of the £20 incentive, the winning variant will be promoted to the default onboarding flow for all new Web-Signup users.

### Addressing Correlation vs. Causation
In CRM and lifecycle marketing, it is notoriously easy to confuse correlation (e.g., "users who open emails tend to buy more") with causation ("the email *caused* them to buy more"). This tracking architecture explicitly solves for causal inference through strict Randomized Controlled Trial (RCT) principles:

1. **Isolating Organic Behavior (The Global Control):** By deliberately holding out 10% of the target audience to receive absolutely nothing, we establish the baseline organic activation rate. Many users who sign up on the web will eventually download the app naturally. Subtracting this baseline from our treatment groups ensures we only report *truly incremental*, causal lift, rather than taking credit for organic intent.
2. **Isolating the Incentive Effect (The Active Control):** Simply sending *any* email will cause a spike in activity due to brand recall. By comparing Groups A & B against the Active Control (which receives a generic reminder email), we isolate the exact causal impact of the £20 incentive and product recommendations. This proves whether sacrificing margin is actually necessary, or if a simple reminder would have achieved the same result.
3. **Randomized Assignment:** Because users are randomly assigned to these cohorts at the exact time of isolation, all confounding variables (e.g., innate high-intent vs. low-intent users, demographics, weekend vs. weekday signups) are distributed equally across all four groups. Therefore, any statistically significant variance in MRPU between the cohorts is mathematically proven to be *caused* by the specific email variant they received.


