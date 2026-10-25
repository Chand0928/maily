# 📬 Email AI Agent

An autonomous executive assistant that connects to your Gmail, reads your unread emails, uses **Claude AI** to summarize and prioritize each one, and drafts high-quality replies directly into your **Gmail Drafts**.

> 🔒 **Safety Guarantee**: This agent **NEVER** sends emails automatically. It only creates drafts in your Gmail account for your personal review and approval.

---

## ⚡ What it Does

When you run `python main.py`, it scans your inbox and outputs:

```text
============================================================
🤖  Email AI Agent - Inbox Assistant
============================================================

[1/3] 🔑 Authenticating with Gmail API...
  ✓ Gmail authenticated successfully.

[2/3] 🧠 Connecting to Claude AI...
  ✓ Claude AI initialized.

[3/3] 📬 Fetching up to 5 unread emails...
  ✓ Found 2 unread email(s). Processing...

------------------------------------------------------------
1. From: boss@company.com
   Summary: Wants the quarterly budget report finalized by Friday.
   Priority: URGENT
   Draft reply: saved in Gmail Drafts

2. From: newsletter@shop.com
   Summary: 50% discount on summer apparel.
   Priority: Low
   Draft reply: skipped

------------------------------------------------------------
Done! Processed 2 email(s):
• 1 draft reply(s) saved in Gmail Drafts
• 1 email(s) skipped (newsletters/promos or FYI)

🔒 Safety reminder: Nothing was sent. All drafts are waiting for your review in Gmail.
============================================================
```

---

## 🗂️ Project Structure

```text
email-agent/
├── main.py          # Entry point: connects Gmail & Claude, orchestrates workflow
├── gmail_tools.py   # Gmail API integration: OAuth2 login, message parsing, drafts
├── agent.py         # AI intelligence: Claude prompt, priority classification, draft generation
├── requirements.txt # Python dependencies
├── .env.example     # Template for environment configuration
├── .env             # Your local secret keys (NEVER commit to Git)
├── .gitignore       # Protects secret keys & auth tokens from being uploaded
└── README.md        # Documentation and setup guide
```

---

## 🚀 Step-by-Step Setup Guide

### Step 1: Clone & Setup Environment

```bash
# 1. Clone your repository (or navigate to project directory)
cd email-agent

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

### Step 2: Setup Gmail API Access (`credentials.json`)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a project** > **New Project**, name it `Email-AI-Agent`, and click **Create**.
3. In the sidebar, navigate to **APIs & Services** > **Library**.
4. Search for **Gmail API** and click **Enable**.
5. Configure the OAuth Consent Screen:
   - In the sidebar, click **OAuth consent screen**.
   - Select **External** and click **Create**.
   - Fill in **App name** (e.g. `Email Agent`) and your email under **User support email** and **Developer contact information**.
   - Click **Save and Continue** through the scopes screen.
   - Under **Test users**, click **Add Users** and add your own Gmail address (the one you want the agent to read).
   - Click **Save and Continue**.
6. Generate Credentials:
   - In the sidebar, click **Credentials** > **Create Credentials** > **OAuth client ID**.
   - Application type: **Desktop app**.
   - Name: `Email Agent Desktop Client`.
   - Click **Create**.
7. Download the credentials:
   - Click the **Download JSON** icon on the created client ID.
   - Rename the downloaded file to `credentials.json` and place it in the root of this `email-agent/` directory.

---

### Step 3: Setup Anthropic Claude API Key (`.env`)

1. Sign up or log into [Anthropic Console](https://console.anthropic.com/).
2. Navigate to **API Keys** and click **Create Key**.
3. Copy your API key.
4. Duplicate `.env.example` to create `.env`:
   ```bash
   cp .env.example .env
   ```
5. Open `.env` and paste your key:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-...
   CLAUDE_MODEL=claude-3-5-sonnet-20241022
   MAX_EMAILS=5
   USER_NAME=YourName
   ```

---

### Step 4: Run the Agent

Run the main script:

```bash
python main.py
```

* **First run**: A browser window will open asking you to sign into your Google account and grant read & draft access. Click **Allow**.
* A file named `token.json` will be automatically generated locally so you won't need to log in again on future runs.
* The agent reads your unread emails, analyzes them with Claude, prints summaries and priorities, and saves drafts for relevant emails directly in your Gmail!

---

### Step 5: Verify Your Drafts in Gmail

1. Open [Gmail](https://mail.google.com/).
2. Click on the **Drafts** folder.
3. You will see the drafted replies attached directly to the conversation threads.
4. Review, adjust if needed, and hit Send whenever you're ready!

---

### Step 6: Push to GitHub

Ensure sensitive files are never pushed:

```bash
# Check git status (credentials.json, token.json, and .env should NOT appear)
git status

# Initialize repository and commit
git init
git add .
git commit -m "Initial commit: Autonomous Email AI Agent"

# Link to your GitHub repository
git branch -M main
git remote add origin https://github.com/<your-username>/email-agent.git
git push -u origin main
```

---

### Step 7: Share on X (Twitter) / LinkedIn

Record a quick 30-second screen capture or share a screenshot:

> **Suggested Post:**  
> *"I built an autonomous AI email assistant using Python, the Gmail API, and Claude 3.5 Sonnet! 🤖✉️*  
> *It reads unread emails, prioritizes urgent messages, and writes draft replies directly into Gmail Drafts (zero auto-sends).*  
> *Check out the open-source code on GitHub: [link]"*

---

## 🛡️ Security & Privacy Checklist

- [x] **No Auto-Sending**: Replies are written strictly to `Drafts`.
- [x] **Least-Privilege Scopes**: The agent requests only `gmail.readonly` and `gmail.compose`. It cannot delete or modify other settings.
- [x] **Git Privacy**: `.env`, `credentials.json`, and `token.json` are listed in `.gitignore` by default.

---

## 📜 License

MIT License. Free to use and customize!
