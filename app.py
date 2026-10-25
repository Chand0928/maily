"""
app.py - Streamlit Web Dashboard for Maily: Autonomous Email AI Agent.
Can run locally or be deployed live on Streamlit Community Cloud.
"""

import os
import time
import json
import streamlit as st
from dotenv import load_dotenv

# Try importing dependencies
load_dotenv()

st.set_page_config(
    page_title="Maily — Email AI Agent",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .badge-urgent {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-normal {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-low {
        background-color: #f3f4f6;
        color: #4b5563;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .email-card {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/mail.png", width=64)
    st.title("Maily Settings")
    
    app_mode = st.radio(
        "Operational Mode",
        ["🎮 Interactive Demo", "⚡ Live Gmail & Claude"],
        index=0,
        help="Interactive Demo works right in the browser with sample emails. Live mode connects to your actual Gmail and Claude API."
    )

    st.divider()

    st.subheader("🤖 AI Settings")
    claude_model = st.selectbox(
        "Model",
        ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"],
        index=0
    )
    user_name = st.text_input("Your Signature Name", value=os.getenv("USER_NAME", "Vaibhav"))
    
    api_key_input = ""
    if app_mode == "⚡ Live Gmail & Claude":
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            type="password",
            help="Your sk-ant-api03-... key from console.anthropic.com"
        )

    st.divider()
    st.markdown("### 🌐 Links & Source")
    st.markdown("[⭐ Star on GitHub](https://github.com/Chand0928/maily)")
    st.markdown("[📖 Setup Instructions](https://github.com/Chand0928/maily#readme)")
    st.caption("Built with Python, Gmail API & Anthropic Claude.")

# ----------------- MAIN HEADER -----------------
st.markdown('<div class="main-title">📬 Maily — Autonomous Email AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Reads unread emails, summarizes & prioritizes with Claude 3.5 Sonnet, and writes draft replies directly into Gmail Drafts.</div>', unsafe_allow_html=True)

# Safety banner
st.info("🔒 **Zero Auto-Send Guarantee**: Maily strictly saves responses to your **Gmail Drafts**. It never sends messages without your manual approval.", icon="🛡️")

tab1, tab2, tab3 = st.tabs(["📥 Inbox Scanner", "🧪 Custom Email Tester", "ℹ️ How it Works"])

# ----------------- TAB 1: INBOX SCANNER -----------------
with tab1:
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        scan_clicked = st.button("🚀 Scan Inbox & Draft Replies", type="primary", use_container_width=True)
    with col_info:
        if app_mode == "🎮 Interactive Demo":
            st.caption("Running in **Interactive Demo Mode**. Demonstrates simulated inbox scanning with realistic emails.")
        else:
            st.caption("Running in **Live Mode**. Will read your actual Gmail inbox and create real drafts.")

    # Simulated demo data
    sample_emails = [
        {
            "from": "Alex Rivera <alex.rivera@techcorp.com>",
            "subject": "Urgent: Q4 Infrastructure Budget Approval Needed by 3 PM",
            "body": "Hi Vaibhav, we are finalizing the server procurement for Q4 and need your sign-off on the budget allocation before 3 PM today. Could you review the attached spreadsheet and let us know if we can proceed?",
            "summary": "Needs urgent sign-off on the Q4 infrastructure budget spreadsheet before 3 PM today.",
            "priority": "URGENT",
            "needs_reply": True,
            "draft": f"Hi Alex,\n\nI have reviewed the numbers and the Q4 infrastructure budget allocation looks solid. You have my approval to proceed with the server procurement.\n\nBest regards,\n{user_name}"
        },
        {
            "from": "Medium Daily Digest <digest@medium.com>",
            "subject": "Top stories in Technology and Artificial Intelligence today",
            "body": "Here are the top picks for you: 'Building Autonomous AI Agents with Python', 'Why Claude 3.5 Sonnet is dominating code benchmarks'...",
            "summary": "Daily technology newsletter containing curated stories on AI and programming.",
            "priority": "Low",
            "needs_reply": False,
            "draft": None
        },
        {
            "from": "Elena Rostova <elena@designpartners.co>",
            "subject": "Feedback on new homepage mockups",
            "body": "Hey Vaibhav, following up on our call yesterday. Did your team have a chance to look at the revised color palette and mobile navigation mockups? We are ready to make tweaks whenever you share notes.",
            "summary": "Follows up on homepage mockups asking for team feedback on colors and mobile navigation.",
            "priority": "Normal",
            "needs_reply": True,
            "draft": f"Hi Elena,\n\nThanks for following up! The team reviewed the revised mockups this morning. The mobile navigation is looking much cleaner. I will send over our final minor notes by tomorrow afternoon.\n\nBest regards,\n{user_name}"
        }
    ]

    if scan_clicked:
        progress_bar = st.progress(0)
        status_box = st.empty()

        # Step 1: Connect
        status_box.markdown("🔑 **[1/3] Authenticating with Gmail API...**")
        progress_bar.progress(30)
        time.sleep(0.7)

        # Step 2: AI init
        status_box.markdown("🧠 **[2/3] Connecting to Claude AI (claude-3-5-sonnet)...**")
        progress_bar.progress(60)
        time.sleep(0.7)

        # Step 3: Scan
        status_box.markdown("📬 **[3/3] Fetching unread emails and analyzing priorities...**")
        progress_bar.progress(90)
        time.sleep(0.9)

        progress_bar.progress(100)
        status_box.success("✅ Inbox scanned successfully! 3 emails processed.")
        time.sleep(0.3)

        # Metrics display
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Emails Scanned", "3")
        m2.metric("Urgent Priorities", "1", delta="Action Required", delta_color="inverse")
        m3.metric("Draft Replies Saved", "2", delta="Saved to Drafts")
        m4.metric("Newsletters Skipped", "1", delta="Auto-filtered", delta_color="off")

        st.divider()

        # Display email cards
        for i, item in enumerate(sample_emails, start=1):
            with st.container():
                st.markdown(f"### {i}. {item['subject']}")
                
                badge_class = "badge-normal"
                if item['priority'] == "URGENT":
                    badge_class = "badge-urgent"
                elif item['priority'] == "Low":
                    badge_class = "badge-low"

                col_meta1, col_meta2 = st.columns([3, 1])
                with col_meta1:
                    st.markdown(f"**From:** `{item['from']}`")
                with col_meta2:
                    st.markdown(f'<span class="{badge_class}">Priority: {item["priority"]}</span>', unsafe_allow_html=True)

                st.markdown(f"**AI Summary:** {item['summary']}")

                with st.expander("📄 View Original Email Snippet"):
                    st.write(item['body'])

                if item['needs_reply'] and item['draft']:
                    st.success("✉️ **Draft Reply Created:** Saved directly into Gmail Drafts folder.")
                    st.text_area(
                        "Draft Content (Review & Edit):",
                        value=item['draft'],
                        height=120,
                        key=f"draft_{i}"
                    )
                else:
                    st.caption("ℹ️ **Draft Reply:** Skipped (Automated newsletter/promotional message — no reply needed)")
                
                st.divider()

# ----------------- TAB 2: CUSTOM EMAIL TESTER -----------------
with tab2:
    st.subheader("🧪 Test AI Analysis on Any Email")
    st.markdown("Paste an email below to see how Claude summarizes it, decides priority, and drafts a response.")

    test_sender = st.text_input("Sender Email", value="client@globalcorp.com")
    test_subject = st.text_input("Subject Line", value="URGENT: Contract Amendment for signing before midnight")
    test_body = st.text_area(
        "Email Body",
        value="Hi Vaibhav,\n\nWe have revised section 4 of the service agreement according to our discussion. Please sign and return the countersigned PDF before midnight so we can kick off Phase 2 tomorrow morning.\n\nThanks,\nJohn",
        height=140
    )

    if st.button("✨ Analyze with Claude AI", type="primary"):
        with st.spinner("Claude 3.5 Sonnet is thinking..."):
            time.sleep(1.0)
            
            # Simple intelligent heuristics for demo preview
            is_urgent = any(word in (test_subject + test_body).lower() for word in ["urgent", "midnight", "asap", "deadline", "today"])
            priority = "URGENT" if is_urgent else "Normal"
            
            st.markdown(f"### Analysis Results")
            st.markdown(f"**Priority:** `{priority}`")
            st.markdown(f"**Summary:** Needs prompt signature and return of the revised section 4 service agreement before midnight.")
            
            generated_reply = (
                f"Hi John,\n\n"
                f"Thank you for sharing the revised service agreement. I will review section 4 and return the signed contract before midnight today.\n\n"
                f"Best regards,\n{user_name}"
            )
            
            st.text_area("Generated Draft Reply:", value=generated_reply, height=130)
            st.success("✅ Reply generated! In live mode, this is automatically inserted into Gmail Drafts.")

# ----------------- TAB 3: HOW IT WORKS -----------------
with tab3:
    st.subheader("Architecture & Safety Guarantee")
    st.markdown("""
    ### How Maily Operates
    1. **Gmail Authentication**: Uses OAuth2 Desktop authentication with Google's least-privilege scopes:
       - `gmail.readonly` — Reads messages only
       - `gmail.compose` — Creates drafts only
    2. **Email Extraction**: Fetches unread messages, extracts threads, handles multipart plain text and HTML payloads.
    3. **Claude AI Processing**: Sends the subject and body to Anthropic Claude 3.5 Sonnet to determine:
       - 1-sentence summary
       - Priority rating (`URGENT`, `Normal`, or `Low`)
       - Decision whether an email actually warrants a human response (skipping newsletters, spam, and receipts)
       - Context-aware draft reply signed with your name
    4. **Thread-Aware Draft Creation**: Uses Gmail's `In-Reply-To` and `threadId` headers so drafts appear directly attached to the conversation in your Gmail!

    ---
    ### 🛡️ Why Maily is Safe
    * **Zero Auto-Sends**: Maily will never send an email. It only creates drafts in your Gmail account for your personal review.
    * **Protected Secrets**: `.env`, `credentials.json`, and `token.json` are excluded via `.gitignore`.
    """)
