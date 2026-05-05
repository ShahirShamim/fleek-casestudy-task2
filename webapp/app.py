import os
import resend
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)

# Configure Resend API Key from environment variables
api_key = os.environ.get("RESEND_API_KEY")
if api_key:
    resend.api_key = api_key
else:
    print("Warning: RESEND_API_KEY environment variable not set.")

TEST_EMAILS_DIR = os.environ.get("TEST_EMAILS_DIR", os.path.join(BASE_DIR, "test_emails"))
FROM_EMAIL = "hireme@shahir.work"

def format_subject(cohort, region):
    # Format the cohort name (e.g., active_control -> Active Control, group_a -> Group A)
    if cohort == "active_control":
        cohort_display = "Active Control"
    else:
        parts = cohort.split('_')
        cohort_display = f"Group {parts[1].upper()}" if len(parts) > 1 else cohort.title()
        
    return f"[TEST] {cohort_display} - {region.upper()}"

@app.route('/')
def index():
    # Parse available cohorts and regions from the files in TEST_EMAILS_DIR
    cohorts = set()
    regions = set()
    
    if os.path.exists(TEST_EMAILS_DIR):
        for f in os.listdir(TEST_EMAILS_DIR):
            if f.endswith('.html'):
                # e.g. group_a_EN.html
                name_without_ext = os.path.splitext(f)[0]
                parts = name_without_ext.split('_')
                if len(parts) >= 3:
                    if parts[0] == "active" and parts[1] == "control":
                        cohorts.add("active_control")
                        regions.add(parts[2].upper())
                    elif parts[0] == "group":
                        cohorts.add(f"group_{parts[1]}")
                        regions.add(parts[2].upper())
                elif len(parts) == 2:
                    cohorts.add(parts[0])
                    regions.add(parts[1].upper())
    
    return render_template('index.html', 
                           cohorts=sorted(list(cohorts)), 
                           regions=sorted(list(regions)))

@app.route('/send', methods=['POST'])
def send_email():
    data = request.json
    email = data.get('email')
    cohort = data.get('cohort')
    region = data.get('region')
    
    if not email or not cohort or not region:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
        
    filename = f"{cohort}_{region}.html"
    filepath = os.path.join(TEST_EMAILS_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"success": False, "message": f"Template not found for {cohort} and {region}"}), 404
        
    subject = format_subject(cohort, region)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        r = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": email,
            "subject": subject,
            "html": html_content
        })
        
        return jsonify({
            "success": True, 
            "message": f"Successfully sent to {email}",
            "id": r.get('id', 'unknown')
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/simulate', methods=['POST'])
def simulate_pipeline():
    data = request.json or {}
    email = data.get('email', 'user@example.fr')
    cohort = data.get('cohort', 'group_a')
    region = data.get('region', 'FR').upper()
    user_id = 1288
    
    steps = [
        {
            "id": "step-1",
            "title": "1. Target Isolation (BigQuery)",
            "description": "Isolating users who signed up in the past 24 hours but have not yet installed the app.",
            "request": "SELECT \n  user_id, email, country, \n  signup_date, reselling_platform, user_intent\nFROM `fleek.core.users`\nWHERE onboarding_completed = false\n  AND is_email_reachable = true\n  AND signup_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR);",
            "response": "[\n  {\n    \"user_id\": " + str(user_id) + ", \n    \"email\": \"" + email + "\", \n    \"country\": \"" + region + "\", \n    \"reselling_platform\": \"vinted\", \n    \"user_intent\": \"sourcing\"\n  }\n]"
        },
        {
            "id": "step-2",
            "title": "2. Cohort Assignment",
            "description": "Randomly assigning isolated users to one of the four experimental cohorts.",
            "request": "POST /internal/assign_cohorts HTTP/1.1\nContent-Type: application/json\n\n{\n  \"users\": [" + str(user_id) + "],\n  \"distribution\": {\n    \"global_control\": 0.1, \n    \"active_control\": 0.3, \n    \"group_a\": 0.3, \n    \"group_b\": 0.3\n  }\n}",
            "response": "{\n  \"assignments\": {\n    \"" + str(user_id) + "\": \"" + cohort + "\"\n  }\n}"
        },
        {
            "id": "step-3",
            "title": "3. Product Matching & API Hydration",
            "description": "Fetching relevant products using nearest-neighbor similarity.",
            "request": "GET /api/v1/products?ids=992,104 HTTP/1.1\nAuthorization: Bearer internal_token_xyz",
            "response": "{\n  \"data\": [\n    {\n      \"id\": 992, \n      \"name\": \"Vintage Levi's 501\", \n      \"price\": \"£25.00\", \n      \"in_stock\": true\n    },\n    {\n      \"id\": 104, \n      \"name\": \"Nike Spellout Sweatshirt\", \n      \"price\": \"£35.00\", \n      \"in_stock\": true\n    }\n  ]\n}"
        },
        {
            "id": "step-4",
            "title": "4. Dynamic Localization & News Injection",
            "description": f"LLM generation for localized hooks based on region ({region}).",
            "request": "POST /v1/chat/completions HTTP/1.1\nHost: api.openai.com\nContent-Type: application/json\n\n{\n  \"model\": \"gpt-4-turbo\",\n  \"messages\": [\n    {\n      \"role\": \"system\", \n      \"content\": \"Generate a brief vintage fashion hook for " + region + ".\"\n    }\n  ]\n}",
            "response": "{\n  \"choices\": [\n    {\n      \"message\": {\n        \"content\": \"Découvrez les dernières pépites vintage sur Fleek!\"\n      }\n    }\n  ]\n}"
        },
        {
            "id": "step-5",
            "title": "5. Email Delivery via Resend",
            "description": "Dispatching the rendered HTML payload to the isolated user.",
            "request": "POST /emails HTTP/1.1\nHost: api.resend.com\nContent-Type: application/json\n\n{\n  \"from\": \"hireme@shahir.work\",\n  \"to\": \"" + email + "\",\n  \"subject\": \"" + format_subject(cohort, region) + "\",\n  \"html\": \"<html>...</html>\"\n}",
            "response": "{\n  \"id\": \"re_123456789\",\n  \"status\": \"queued\"\n}"
        },
        {
            "id": "step-6",
            "title": "6. State Logging (BigQuery)",
            "description": "Pushing user details and cohort assignment to crm_activation_log.",
            "request": "INSERT INTO `fleek.marketing.crm_activation_log` \n  (user_id, assigned_cohort, locale, sent_at)\nVALUES \n  (" + str(user_id) + ", '" + cohort + "', '" + region + "', CURRENT_TIMESTAMP());",
            "response": "{\n  \"status\": \"success\",\n  \"rows_inserted\": 1\n}"
        }
    ]
    return jsonify(steps)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
