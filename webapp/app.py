import os
import resend
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Configure Resend API Key from environment variables
api_key = os.environ.get("RESEND_API_KEY")
if api_key:
    resend.api_key = api_key
else:
    print("Warning: RESEND_API_KEY environment variable not set.")

TEST_EMAILS_DIR = os.environ.get("TEST_EMAILS_DIR", "../test_emails")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
