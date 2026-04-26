# BigQuery Database Context for Fleek

Use this context to write standard SQL queries for Google BigQuery. 

## Tables and Relationships

### 1. User Activation Dataset
**Table:** `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset`
**Description:** Contains user signup, onboarding, and high-level order summary data (167k users over the last 6 months).
**Primary Key:** `user_id`

**Key Fields:**
- `user_id` (string): Unique identifier. Joins with `customer_id` in `growth_model`.
- `country` (string): User's country.
- `signup_date` (date/timestamp): Date of signup.
- `buyer_persona` (string): E.g., Reseller, Retailer.
- `is_email_reachable`, `is_push_reachable` (boolean)
- `onboarding_completed` (boolean)
- `user_intent` (string): E.g., TO_EARN_EXTRA_MONEY, TO_GROW.
- `reselling_platform`, `has_existing_store` (string/boolean)
- `first_order_date`, `second_order_date` (date/timestamp)
- `total_orders` (int), `total_gmv` (numeric): Spend in GBP.

---

### 2. Growth Model (Order History)
**Table:** `dogwood-baton-345622.fleek_analytics.growth_model`
**Description:** Contains line-item level purchase history.
**Foreign Keys:** 
- `customer_id` joins to `user_id` in `case_study_activation_dataset`
- `product_id` joins to `product_id` in `product_details_v2`

**Key Fields:**
- `order_line_id` (string): Unique identifier for the line item.
- `order_id`, `order_number` (string): Identifiers for the order.
- `customer_id` (string): Buyer identifier.
- `ordered_date` (date/timestamp): Order placement date.
- `order_type` (string): E.g., first order, repeat.
- `product_id` (string): Product identifier.
- `quantity` (int): Units purchased on this line.
- `total_amount_prediscount`, `total_discount` (numeric): Revenue in GBP.
- `financial_status`, `fulfillment_status`, `account_status` (string)
- `buyer_persona` (string)

---

### 3. Product Details
**Table:** `dogwood-baton-345622.fleek_analytics.product_details_v2`
**Description:** Product and inventory catalog.
**Primary Key:** `product_id`

**Key Fields:**
- `product_id` (string): Unique product identifier.
- `title`, `vendor` (string)
- `product_type`, `l1`, `l2`, `l3` (string): Category hierarchy.
- `grade`, `gender`, `style`, `brand` (string)
- `is_active`, `approved_status` (boolean/string)
- `per_unit_price`, `vendor_base_price` (numeric): GBP.
- `available_quantity` (int)
- `vintage_inspired_flag`, `upcycled_flag` (boolean)

## Join Snippets
When joining tables, use these standard patterns:

```sql
-- Join Users to their Orders
SELECT *
FROM `dogwood-baton-345622.fleek_marketing.case_study_activation_dataset` users
LEFT JOIN `dogwood-baton-345622.fleek_analytics.growth_model` orders
  ON users.user_id = orders.customer_id

-- Join Orders to Product Details
SELECT *
FROM `dogwood-baton-345622.fleek_analytics.growth_model` orders
LEFT JOIN `dogwood-baton-345622.fleek_analytics.product_details_v2` products
  ON orders.product_id = products.product_id
```

## Best Practices & Assumptions for Queries
- **SQL Dialect:** Always use standard BigQuery SQL syntax.
- **Nulls & Blanks:** Nulls and blanks are realistic and not errors (e.g., users who haven't ordered will have a null `first_order_date`). Make sure to handle `NULL` values correctly in WHERE clauses.
- **Currency:** All financial values (`total_gmv`, `total_amount_prediscount`, etc.) are consistently in GBP.
- **Granularity:** 
  - `case_study_activation_dataset` is at the **user** level.
  - `growth_model` is at the **order line item** level. If you need order-level metrics, be sure to `GROUP BY order_id`.
  - `product_details_v2` is at the **product** level.
