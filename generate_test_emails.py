import os
import sys
import csv
import json
import ast

# Paths
USERS_FILE = 'user_products.csv'
LOCALIZED_JSON = 'localized_content_samples.json'
TEMPLATE_DIR = 'email_templates'
OUTPUT_DIR = 'test_emails'

# Cohort definitions
COHORTS = ['active_control', 'group_a', 'group_b']
LANGUAGES = ['EN', 'DE', 'FR']

def load_templates():
    templates = {}
    for cohort in COHORTS:
        path = os.path.join(TEMPLATE_DIR, f'template_{cohort}.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                templates[cohort] = f.read()
    return templates

def get_user_products(user_id):
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if str(row['user_id']) == str(user_id):
                try:
                    return ast.literal_eval(row['recommended_product_ids'])
                except:
                    return []
    return None

def fetch_product_metadata(product_ids):
    """
    Mocks an API hydration step. In production, this would make an HTTP GET request
    to Fleek's internal backend (e.g. requests.get('https://api.joinfleek.com/v1/products', params={'ids': ','.join(map(str, product_ids))}))
    """
    print(f"Hydrating {len(product_ids)} products via API...")
    mock_catalog = [
        {"name": "Y2K Bootcut Jeans", "image_url": "https://d314e77m1bz5zy.cloudfront.net/bee/Images/bmsx/wfjybjh5/ngk/d5v/c0p/394_15.png"},
        {"name": "Vintage Carhartt Jacket", "image_url": "https://d314e77m1bz5zy.cloudfront.net/bee/Images/bmsx/wfjybjh5/6lh/nca/8tz/395_12.png"},
        {"name": "90s Graphic Sweatshirt", "image_url": "https://d314e77m1bz5zy.cloudfront.net/bee/Images/bmsx/wfjybjh5/q0s/9wn/4uq/396_12.png"},
        {"name": "Upcycled Denim Skirt", "image_url": "https://d314e77m1bz5zy.cloudfront.net/bee/Images/bmsx/wfjybjh5/maz/s6f/xtg/397_11.png"},
        {"name": "Retro Harley Davidson Tee", "image_url": "https://d314e77m1bz5zy.cloudfront.net/bee/Images/bmsx/wfjybjh5/ngk/d5v/c0p/394_15.png"},
        {"name": "Oversized Flannel Shirt", "image_url": "https://d314e77m1bz5zy.cloudfront.net/bee/Images/bmsx/wfjybjh5/6lh/nca/8tz/395_12.png"}
    ]
    
    hydrated_products = []
    for pid in product_ids:
        # Use modulo math to assign a deterministic mock product to each ID
        catalog_item = mock_catalog[int(pid) % len(mock_catalog)]
        hydrated_products.append({
            "id": pid,
            "name": catalog_item["name"],
            "image_url": catalog_item["image_url"]
        })
        
    return hydrated_products

def main():
    if len(sys.argv) > 1:
        target_user_id = sys.argv[1]
    else:
        target_user_id = input("Enter the user_id to generate test emails for: ").strip()

    product_ids = get_user_products(target_user_id)
    
    if product_ids is None:
        print(f"Error: user_id '{target_user_id}' not found in {USERS_FILE}.")
        sys.exit(1)
        
    print(f"Found user {target_user_id} with recommended products: {product_ids}")
    
    # Hydrate products via mock API
    hydrated_products = fetch_product_metadata(product_ids)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    templates = load_templates()
    
    with open(LOCALIZED_JSON, 'r', encoding='utf-8') as f:
        localized_content = json.load(f)
        
    for cohort, template_html in templates.items():
        for lang in LANGUAGES:
            content = localized_content.get(lang, {})
            html = template_html
            
            # 1. Replace Localized Strings
            for key, value in content.items():
                html = html.replace(f"{{{{{key}}}}}", str(value))
                
            # 2. Replace Generic Links
            html = html.replace("{{APP_STORE_LINK}}", "https://apps.apple.com/app/fleek")
            html = html.replace("{{UNSUBSCRIBE_LINK}}", "https://www.joinfleek.com/unsubscribe")
            
            # 3. Replace Product Data (Group A only)
            if cohort == 'group_a' and len(hydrated_products) >= 4:
                for i in range(1, 5):
                    prod = hydrated_products[i-1]
                    html = html.replace(f"{{{{PRODUCT_{i}_ID}}}}", str(prod["id"]))
                    html = html.replace(f"{{{{PRODUCT_{i}_NAME}}}}", prod["name"])
                    html = html.replace(f"{{{{PRODUCT_{i}_IMAGE_URL}}}}", prod["image_url"])
                    
            # 4. Save to test_emails/ folder
            output_file = os.path.join(OUTPUT_DIR, f"{cohort}_{lang}_user_{target_user_id}.html")
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(html)
                
            print(f"Generated: {output_file}")
            
    print(f"\nAll 9 test variations for user {target_user_id} have been successfully generated in the '{OUTPUT_DIR}' directory.")

if __name__ == '__main__':
    main()
