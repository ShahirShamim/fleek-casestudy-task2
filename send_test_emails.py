import os
import sys
import time
import resend
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Resend API Key from environment variables
api_key = os.environ.get("RESEND_API_KEY")
if not api_key:
    print("Error: Please set the RESEND_API_KEY environment variable before running this script.")
    sys.exit(1)
    
resend.api_key = api_key

TEST_EMAILS_DIR = "test_emails"
FROM_EMAIL = "hireme@shahir.work"

def format_subject(filename):
    """
    Parses the filename (e.g. 'group_a_EN_user_1288.html') 
    and returns a clean subject line (e.g. '[TEST] Group A - EN')
    """
    name_without_ext = os.path.splitext(filename)[0]
    # Replace underscores with spaces and title case it
    # e.g. active_control_EN_user_1288 -> Active Control En User 1288
    # We can clean it up slightly
    parts = name_without_ext.split('_')
    
    # Extract the core parts (Cohort and Lang)
    if len(parts) >= 3:
        if parts[0] == "active":
            cohort = "Active Control"
            lang = parts[2]
        else:
            cohort = f"Group {parts[1].upper()}"
            lang = parts[2]
            
        return f"[TEST] {cohort} - {lang.upper()}"
    else:
        return f"[TEST] {name_without_ext.replace('_', ' ').title()}"

def main():
    if not os.path.exists(TEST_EMAILS_DIR):
        print(f"Error: Directory '{TEST_EMAILS_DIR}' not found.")
        return

    recipient_email = input("Enter the email address to send the test emails to: ").strip()
    
    if not recipient_email:
        print("Error: No email address provided.")
        return

    # List all HTML files in the test_emails directory
    files = [f for f in os.listdir(TEST_EMAILS_DIR) if f.endswith('.html')]
    
    if not files:
        print(f"No HTML files found in '{TEST_EMAILS_DIR}'.")
        return

    print(f"\nSending {len(files)} emails to {recipient_email} from {FROM_EMAIL}...")

    success_count = 0
    for filename in files:
        filepath = os.path.join(TEST_EMAILS_DIR, filename)
        subject = format_subject(filename)
        
        # Read the fully rendered HTML payload
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()

        try:
            r = resend.Emails.send({
                "from": FROM_EMAIL,
                "to": recipient_email,
                "subject": subject,
                "html": html_content
            })
            print(f"✅ Sent: {subject} (ID: {r.get('id', 'unknown')})")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to send {filename}: {e}")

    print(f"\nFinished sending. Successfully dispatched {success_count}/{len(files)} test emails.")

    print("\n" + "="*40)
    print("🎬 CRON PIPELINE 🎬")
    print("="*40)
    
    steps = [
        "Fetching Random User",
        "Retrieving Localisation Context",
        "Prompting Gemma4 to create copy",
        "Populating email templates with JSON",
        "Wrapping things up",
        "Sending emails"
    ]
    
    for step in steps:
        sys.stdout.write(f"\r\033[K⏳ {step}...")
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f"\r\033[K✅ {step} [DONE]\n")
        sys.stdout.flush()
        
    time.sleep(0.5)
    print("🚀 Emails Sent!\n")

if __name__ == "__main__":
    main()
