"""
main.py - Entry point for Email AI Agent.
Runs the complete workflow:
1. Connects to Gmail and reads unread emails
2. Uses Claude AI to summarize, prioritize, and generate draft replies
3. Saves draft replies directly in Gmail Drafts (never sends automatically)

Supports --demo mode to test/preview without API keys.
"""

import os
import sys
import time
from dotenv import load_dotenv

from gmail_tools import authenticate_gmail, get_unread_emails, create_draft_reply
from agent import get_ai_client, analyze_email

# Load environment configuration
load_dotenv()


def check_prerequisites():
    """Verify that credentials and API keys are present before starting."""
    missing = []
    
    if not os.path.exists("credentials.json"):
        missing.append("- credentials.json (Download from Google Cloud Console)")
        
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key or api_key in ("your_anthropic_api_key_here", "sk-ant-api03-YourRealKeyHere12345", "sk-ant-api03-your_actual_key"):
        missing.append("- ANTHROPIC_API_KEY in .env (Get your real key from https://console.anthropic.com/)")

    if missing:
        print("\n=======================================================")
        print("⚠️  Setup required before running Email AI Agent:")
        print("=======================================================")
        for item in missing:
            print(f" {item}")
        print("\nPlease follow the setup guide in README.md to configure them.")
        print("\n💡 Want to preview Maily in action right now without API keys?")
        print("   👉 Run: python main.py --demo")
        print("=======================================================\n")
        return False
    return True


def run_demo_mode():
    """Simulates the agent with realistic emails for demonstration and recording."""
    print("=" * 60)
    print("🤖  Maily - Email AI Agent (DEMO PREVIEW)")
    print("=" * 60)
    print("\n[1/3] 🔑 Authenticating with Gmail API...")
    time.sleep(0.6)
    print("  ✓ Gmail authenticated successfully. (Demo)")

    print("\n[2/3] 🧠 Connecting to Claude AI...")
    time.sleep(0.6)
    print("  ✓ Claude AI initialized (Model: claude-3-5-sonnet). (Demo)")

    print("\n[3/3] 📬 Fetching up to 3 unread emails...")
    time.sleep(0.8)
    print("  ✓ Found 2 unread email(s). Processing...\n")
    print("-" * 60)

    demo_emails = [
        {
            "from": "boss@company.com",
            "summary": "Wants the quarterly budget report finalized by Friday.",
            "priority": "URGENT",
            "draft": "saved in Gmail Drafts"
        },
        {
            "from": "newsletter@shop.com",
            "summary": "Discount offer on apparel this weekend.",
            "priority": "Low",
            "draft": "skipped"
        }
    ]

    for i, item in enumerate(demo_emails, start=1):
        time.sleep(0.7)
        print(f"{i}. From: {item['from']}")
        print(f"   Summary: {item['summary']}")
        print(f"   Priority: {item['priority']}")
        print(f"   Draft reply: {item['draft']}\n")

    print("-" * 60)
    print("Done! Processed 2 email(s):")
    print("• 1 draft reply(s) saved in Gmail Drafts")
    print("• 1 email(s) skipped (newsletters/promos or FYI)")
    print("\n🔒 Safety reminder: Nothing was sent. All drafts are waiting for your review in Gmail.")
    print("=" * 60)


def main():
    if "--demo" in sys.argv:
        run_demo_mode()
        return

    print("=" * 60)
    print("🤖  Maily - Email AI Agent")
    print("=" * 60)

    if not check_prerequisites():
        sys.exit(1)

    max_emails = int(os.getenv("MAX_EMAILS", 5))
    user_name = os.getenv("USER_NAME", "Vaibhav")

    # Step 1: Connect to Gmail
    print("\n[1/3] 🔑 Authenticating with Gmail API...")
    try:
        service = authenticate_gmail()
        print("  ✓ Gmail authenticated successfully.")
    except Exception as e:
        print(f"  ✗ Failed to connect to Gmail: {e}")
        sys.exit(1)

    # Step 2: Initialize Anthropic AI
    print("\n[2/3] 🧠 Connecting to Claude AI...")
    try:
        ai_client = get_ai_client()
        print("  ✓ Claude AI initialized.")
    except Exception as e:
        print(f"  ✗ Failed to initialize AI: {e}")
        sys.exit(1)

    # Step 3: Fetch unread emails
    print(f"\n[3/3] 📬 Fetching up to {max_emails} unread emails...")
    try:
        unread_emails = get_unread_emails(service, max_results=max_emails)
    except Exception as e:
        print(f"  ✗ Failed to fetch emails: {e}")
        sys.exit(1)

    if not unread_emails:
        print("\n✨ You're all caught up! No unread emails found in your inbox.\n")
        return

    print(f"  ✓ Found {len(unread_emails)} unread email(s). Processing...\n")
    print("-" * 60)

    drafts_created = 0
    drafts_skipped = 0

    for i, email in enumerate(unread_emails, start=1):
        try:
            # AI Analysis
            analysis = analyze_email(
                email=email,
                client=ai_client,
                user_name=user_name
            )

            summary = analysis.get("summary", "No summary provided.")
            priority = analysis.get("priority", "Normal")
            needs_reply = analysis.get("needs_reply", False)
            reply_draft = analysis.get("reply_draft")

            draft_status = "skipped"
            if needs_reply and reply_draft:
                try:
                    create_draft_reply(service, email, reply_draft)
                    draft_status = "saved in Gmail Drafts"
                    drafts_created += 1
                except Exception as draft_err:
                    draft_status = f"error creating draft ({draft_err})"
                    drafts_skipped += 1
            else:
                drafts_skipped += 1

            # Format terminal output exactly as requested
            print(f"{i}. From: {email['from']}")
            print(f"   Summary: {summary}")
            print(f"   Priority: {priority}")
            print(f"   Draft reply: {draft_status}\n")

        except Exception as err:
            print(f"{i}. From: {email.get('from', 'Unknown')}")
            print(f"   Error processing email: {err}\n")

    print("-" * 60)
    print(f"Done! Processed {len(unread_emails)} email(s):")
    print(f"• {drafts_created} draft reply(s) saved in Gmail Drafts")
    print(f"• {drafts_skipped} email(s) skipped (newsletters/promos or FYI)")
    print("\n🔒 Safety reminder: Nothing was sent. All drafts are waiting for your review in Gmail.")
    print("=" * 60)


if __name__ == "__main__":
    main()
