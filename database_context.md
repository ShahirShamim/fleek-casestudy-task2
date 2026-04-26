**The data:**

You will be given BigQuery access to a dataset containing real, anonymised Fleek user data. The table is in `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`.

| Field | Description |
| --- | --- |
| `user_id` | Anonymised unique identifier |
| `country` | User's country (may be null) |
| `signup_date` | Date the user signed up |
| `buyer_persona` | User type where known (e.g. Reseller, Retailer) |
| `is_email_reachable` | Whether we can reach them via email |
| `is_push_reachable` | Whether we can reach them via push notification |
| `onboarding_completed` | Whether the user completed in-app onboarding |
| `user_intent` | Self-reported intent during onboarding (e.g. TO_EARN_EXTRA_MONEY, TO_GROW, TO_EXPLORE) |
| `reselling_platform` | Platform they resell on, where known (e.g. VINTED, DEPOP) |
| `has_existing_store` | Whether they had an existing reselling presence at signup |
| `num_selected_categories` | Number of product categories selected during onboarding |
| `first_order_date` | Date of first purchase (null if never ordered) |
| `first_order_value` | Value of first order in GBP |
| `second_order_date` | Date of second purchase (null if no repeat order) |
| `total_orders` | Total number of orders placed |
| `total_gmv` | Total spend in GBP |

The data covers the last 6 months of signups (167k users). Blanks and nulls are realistic, not errors. If anything in the data is unclear or surprising, that may be intentional - document your assumptions.

**Leadership has asked you to own buyer activation from a CRM.** Your job is to figure out where in the funnel the biggest opportunities are - from landing on the site through to repeat purchase - and propose what you'd focus your CRM efforts on in your first 90 days.

**Additional data tables:**

**`dogwood-baton-345622.fleek_analytics.growth_model`** — Buyer order/purchase history (last 6 months)

| Field | Description |
| --- | --- |
| `order_line_id` | Unique identifier for each line item within an order |
| `order_id` | Unique identifier for the order |
| `order_number` | Human-readable order number |
| `customer_id` | Anonymised buyer identifier (joins to `user_id` in the activation dataset) |
| `ordered_date` | Date the order was placed |
| `order_week` | Week the order was placed |
| `order_month` | Month the order was placed |
| `order_quarter` | Quarter the order was placed |
| `first_order_date` | Date of the buyer's first ever order |
| `order_sort` | The sequence number of this order for the buyer (1 = first order, 2 = second, etc.) |
| `order_type` | Type of order (e.g. first order, repeat) |
| `product_id` | Product identifier (joins to `product_details_v2`) |
| `product_name` | Product title |
| `vendor` | Supplier/wholesaler who listed the product |
| `quantity` | Units purchased on this line |
| `total_amount_prediscount` | Line item revenue before discounts (GBP) |
| `total_discount` | Total discount applied to the line (GBP) |
| `discountValue` | Discount value applied |
| `financial_status` | Payment status (e.g. paid, refunded, voided) |
| `fulfillment_status` | Order fulfilment status |
| `cancel_reason` | Reason the order was cancelled, if applicable |
| `checkout_platform` | Platform used at checkout (iOS, Android, Web) |
| `shipping_address_country` | Destination country of the order |
| `customer_country_region` | Buyer's country/region |
| `buyer_persona` | Buyer type where known (e.g. Reseller, Retailer) |
| `account_status` | Status of the buyer's account |
| `Account_Owner` | Internal owner — `Self Serve` or the name of the Account Manager |

**`dogwood-baton-345622.fleek_analytics.product_details_v2`** — Product and inventory catalogue

| Field | Description |
| --- | --- |
| `product_id` | Unique product identifier (joins to `growth_model`) |
| `title` | Product title |
| `product_handle` | URL handle for the product |
| `vendor` | Supplier/wholesaler who listed the product |
| `product_type` | High-level product type |
| `product_status` | Current product status |
| `is_active` | Whether the product is currently active/live on the marketplace |
| `approved_status` | Approval status of the product listing |
| `approved_status_date` | Date the approval status was set |
| `product_uploaded_date` | Date the product was first uploaded |
| `published_date` | Date the product went live |
| `grade` | Condition grade of the secondhand item (e.g. A, B, C) |
| `gender` | Target gender (e.g. Mens, Womens, Unisex) |
| `l1` | Top-level category |
| `l1_details` | Top-level category details |
| `l2` | Sub-category |
| `l2_details` | Sub-category details |
| `l3` | Sub-sub-category |
| `l3_details` | Sub-sub-category details |
| `style` | Product style tag |
| `style_details` | Additional style detail |
| `brand` | Brand classification (e.g. branded, unbranded, specific brand) |
| `brand_details` | Additional brand details |
| `vintage_inspired_flag` | Flag for vintage-inspired items |
| `upcycled_flag` | Flag for upcycled items |
| `rework_vi_tag` | Rework / vintage-inspired tag |
| `bundle_size` | Bundle size for the listing |
| `total_bundles` | Total number of bundles listed |
| `moq` | Minimum order quantity |
| `available_quantity` | Current available inventory quantity |
| `bundles_sold` | Number of bundles sold to date |
| `str` | Sell-through rate |
| `per_unit_price` | Listed price per unit (GBP) |
| `vendor_base_price` | Vendor's base price per unit (GBP) |
| `shipping_gb_per_unit_price` | Shipping cost per unit to GB |
| `shipping_eu_per_unit_price` | Shipping cost per unit to EU |
| `shipping_us_per_unit_price` | Shipping cost per unit to US |
| `shipping_row_per_unit_price` | Shipping cost per unit to rest of world |
| `is_shipping_inclusive` | Whether the listed price includes shipping |
| `is_fleek_sort` | Whether this product has been graded/sorted by Fleek |
