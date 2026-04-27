# Case Study: Bridging the Web-to-App Activation Gap

## 1. The Solution: Dynamic, Data-Driven Activation
To re-engage this audience, we developed a personalized email push campaign utilizing a rich dataset.

**Audience Definition:**
Target users are strictly those where `onboarding_completed = false` AND `is_email_reachable = true`.

**Personalization Engine:**
*   **Dynamic Localization:** Utilizing `country` data, we localize the outreach. For users in FR/DE, we translate copy and assure them of local shipping. For the US, we emphasize catalog depth. For users with missing country or metadata, the UK will be used as the default fallback.
*   **LLM Hooks:** A dynamic opening sentence is generated via an LLM, pulling in current regional fashion trends or sustainability news to capture immediate attention.
*   **Intent-Based Recommendations:** Utilizing data points like `user_intent`, `reselling_platform`, and `has_existing_store`, we match users with products purchased by similar cohorts.

**The Message Framework:**
The primary CTA is a direct link to the App Store / Google Play Store. To overcome the high friction of downloading a new mobile app, we are pushing the existing £20 financial incentive on their first app order.

## 2. Rigorous Experimental Design (A/B Testing)
To accurately measure the causal impact of the campaign and the financial viability of the £20 incentive, the 58,000 users will be divided into four distinct experimental cohorts:

1.  **Global Control (10% - Holdout):** Does not receive any CRM push. This establishes the absolute baseline for organic, unprompted app downloads and onboarding.
2.  **Active Control (30% - Value Prop Only):** Receives a standard reminder to download the app to access wholesale vintage. **No mention of a discount, no product imagery.** This isolates the impact of simply sending an email vs doing nothing.
3.  **Group A (30% - Incentive + Product Recs):** Receives the £20 incentive prominently, followed by a randomized visual catalog of 4 active products (hydrated via API) to showcase inventory breadth.
4.  **Group B (30% - Incentive Only):** Receives the £20 incentive with a heavy focus on the App Store CTA. **No catalog distractions.** This tests whether visual inventory aids conversion or distracts the user at this early stage.

**Statistical Rigor:** 
Detecting a 15% relative uplift over a ~5.2% organic baseline with 80% statistical power and a 95% confidence interval requires ~17,400 users per treatment. We will send exactly 52,200 emails over a structured 5-day period, followed by a strict 14-day observation window, before declaring a winner.

## 3. Technical Architecture & Automation Pipeline
The campaign is orchestrated by a fully automated daily CRON job that creates a closed-loop data pipeline:

1.  **Target Isolation & Cohort Assignment:** The script isolates users who signed up in the past 24 hours (who haven't onboarded) and randomly assigns them to one of the four cohorts.
2.  **Product Matching & API Hydration:** For Group A, a BigQuery script matches users with 4 relevant product IDs using a nearest-neighbor similarity score based on reselling preferences. It then hits the internal Fleek Product API (`GET /api/v1/products?ids=...`) to "hydrate" these IDs with live image URLs and pricing, ensuring zero out-of-stock items are promoted.
3.  **Dynamic LLM Injection:** Fetches the latest country-specific fashion news. The LLM generates a brief hook and translates copy. *Crucially, this generation happens at the region level (not per-user) to prevent uncontrolled copy variation from contaminating the A/B test.*
4.  **Delivery via Resend:** The script renders the HTML templates and dispatches the emails via the Resend API, scheduling delivery to exactly +24 Hours from the user's initial signup time.
5.  **State Logging:** Pushes user details, cohort assignments, and sent payloads into a dedicated BigQuery tracking table (`crm_activation_log`).

## 4. Measurement, Guardrails & Causal Inference
The daily CRON job loops back to update BigQuery records with downstream conversion events, creating a real-time feedback loop.

**Core KPIs:**
*   **Primary:** Onboarding Completion Rate.
*   **Secondary:** Time to First Purchase.
*   **Tertiary:** Marginal Revenue Per User (Incremental GMV minus the £20 promo liability).

**Guardrails:**
To protect long-term brand equity, we monitor Counter Metrics including **Unsubscribe Rates**, downstream **Email Fatigue**, and **Long-Term Retention Degradation** (ensuring the £20 incentive doesn't simply attract low-LTV churners).

**Solving for Causal Inference Challenges:**
In CRM, correlation is easily confused with causation. This architecture proactively mitigates several deep measurement challenges:
*   **Isolating the Incentive:** By comparing Groups A & B against the Active Control, we measure the *exact* causal impact of the £20 margin sacrifice, proving if a free reminder would have worked just as well.
*   **Holdout Contamination Risk:** Recognizing that users in the Global Control might still receive paid retargeting ads (Meta/Google), which could artificially inflate the baseline.
*   **Cross-Channel Attribution Conflicts:** Relying on deterministic, server-side tracking (`crm_activation_log` via `user_id`) to bypass probabilistic, device-level "last click" attribution wars in third-party platforms like AppsFlyer.
