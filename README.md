# 📬 Maily - Autonomous Email AI Agent

[![GitHub Repository](https://img.shields.io/badge/GitHub-Chand0928%2Fmaily-blue?logo=github)](https://github.com/Chand0928/maily)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An autonomous executive assistant that connects to your Gmail, reads your unread emails, uses **Claude 3.5 Sonnet** to summarize and prioritize each one, and drafts high-quality replies directly into your **Gmail Drafts**.

🔗 **Live GitHub Repository:** [https://github.com/Chand0928/maily](https://github.com/Chand0928/maily)  
📥 **Clone Command:**
```bash
git clone https://github.com/Chand0928/maily.git
```

> 🔒 **Safety Guarantee**: This agent **NEVER** sends emails automatically. It only creates drafts in your Gmail account for your personal review and approval.

---

## ⚡ What it Does

When you run `python main.py`, it scans your inbox and outputs:

```text
============================================================
🤖  Maily - Email AI Agent
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
maily/
├── app.py           # Streamlit Web UI: interactive browser dashboard
├── main.py          # CLI runner: connects Gmail & Claude, orchestrates workflow
├── gmail_tools.py   # Gmail API integration: OAuth2 login, message parsing, drafts
├── agent.py         # AI intelligence: Claude prompt, priority classification, draft generation
├── requirements.txt # Python dependencies (including streamlit)
├── .env.example     # Template for environment configuration
├── .env             # Your local secret keys (NEVER commit to Git)
├── .gitignore       # Protects secret keys & auth tokens from being uploaded
└── README.md        # Documentation and setup guide
```

---

## 🚀 How to Use (Quick Setup Guide)

### Step 1: Open the Project & Setup Environment

```bash
# 1. Navigate to the project directory
cd ~/Desktop/maily

# 2. Activate the pre-configured virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. (Optional) If starting fresh, install dependencies:
pip install -r requirements.txt
```

---

### Step 2: Setup Gmail API Access (`credentials.json`)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a project** > **New Project**, name it `Maily`, and click **Create**.
3. In the sidebar, navigate to **APIs & Services** > **Library**.
4. Search for **Gmail API** and click **Enable**.
5. Configure the OAuth Consent Screen:
   - In the sidebar, click **OAuth consent screen**.
   - Select **External** and click **Create**.
   - Fill in **App name** (e.g. `Maily`) and your email under **User support email** and **Developer contact information**.
   - Click **Save and Continue** through the scopes screen.
   - Under **Test users**, click **Add Users** and add your own Gmail address (the one you want the agent to read).
   - Click **Save and Continue**.
6. Generate Credentials:
   - In the sidebar, click **Credentials** > **Create Credentials** > **OAuth client ID**.
   - Application type: **Desktop app**.
   - Name: `Maily Desktop Client`.
   - Click **Create**.
7. Download the credentials:
   - Click the **Download JSON** icon next to the created client ID.
   - Rename the downloaded file to `credentials.json` and place it in the `maily/` directory.

---

### Step 3: Setup Anthropic Claude API Key (`.env`)

1. Sign up or log into [Anthropic Console](https://console.anthropic.com/).
2. Navigate to **API Keys** and click **Create Key**.
3. Copy your API key.
4. Open the `.env` file inside `maily/`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-your_actual_key_here
   CLAUDE_MODEL=claude-3-5-sonnet-20241022
   MAX_EMAILS=5
   USER_NAME=Vaibhav
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

### Step 6: Push Updates to GitHub

```bash
cd ~/Desktop/maily
git add .
git commit -m "Update documentation and live links"
git push -u origin main
```

---

### Step 7: Share on X (Twitter) / LinkedIn

Record a quick 30-second screen capture or screenshot:

> **Suggested Post:**  
> *"I built Maily — an autonomous AI email assistant using Python, Gmail API, and Claude 3.5 Sonnet! 🤖✉️*  
> *It reads unread emails, detects urgency, and drafts replies straight into Gmail Drafts (zero auto-sends).*  
> *Check out the open-source code on GitHub: https://github.com/Chand0928/maily"*

---

## 🛡️ Security & Privacy Checklist

- [x] **No Auto-Sending**: Replies are written strictly to `Drafts`.
- [x] **Least-Privilege Scopes**: The agent requests only `gmail.readonly` and `gmail.compose`. It cannot delete or modify other settings.
- [x] **Git Privacy**: `.env`, `credentials.json`, and `token.json` are listed in `.gitignore` by default.

---

## 📜 License

MIT License. Free to use and customize!
