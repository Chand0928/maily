"""
agent.py - AI logic powered by Anthropic Claude to summarize, prioritize, and draft email replies.
"""

import os
import json
import re
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def get_ai_client():
    """Initializes and returns the Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key.strip() in ("", "your_anthropic_api_key_here"):
        raise ValueError(
            "ANTHROPIC_API_KEY is not set in .env!\n"
            "Please add your Anthropic API key to the .env file."
        )
    return Anthropic(api_key=api_key)


def analyze_email(email: dict, client: Anthropic = None, model: str = None, user_name: str = None) -> dict:
    """
    Analyzes an email to generate:
    - summary: 1-2 sentence overview
    - priority: URGENT, Normal, or Low
    - needs_reply: bool (False for newsletters, spam, automated receipts, etc.)
    - reply_draft: suggested reply text (or None if skipped)
    """
    if client is None:
        client = get_ai_client()

    if not model:
        model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

    if not user_name:
        user_name = os.getenv("USER_NAME", "Me")

    sender = email.get("from", "Unknown")
    subject = email.get("subject", "No Subject")
    body = email.get("body", "")

    # Truncate body if excessively long (e.g. over 8000 characters) to save tokens
    truncated_body = body[:8000] if body else "(Empty Body)"

    prompt = f"""You are an executive email assistant. Your job is to process incoming emails intelligently.

Here is an incoming email:
----------------------------------------
From: {sender}
Subject: {subject}
Body:
{truncated_body}
----------------------------------------

User's Name: {user_name}

Tasks:
1. Summarize: Provide a 1-sentence concise summary of what this email is about and any requested action.
2. Prioritize: Determine the priority level:
   - "URGENT": Direct requests with imminent deadlines, emergencies, critical boss/client communications.
   - "Normal": Legitimate human emails asking questions or sharing updates that should be answered.
   - "Low": Marketing promos, newsletters, automated receipts, system alerts, social media notifications.
3. Decision on Reply:
   - Set `needs_reply` to false for automated newsletters, promotional offers, notifications, receipts, no-reply emails, or pure FYIs.
   - Set `needs_reply` to true only if a human response is genuinely required or expected.
4. Draft Reply:
   - If `needs_reply` is true, write a polite, professional, and clear reply addressing the specific points. Sign off with:
     Best regards,
     {user_name}
   - If `needs_reply` is false, set `reply_draft` to null.

You must respond ONLY with a valid JSON object matching this schema:
{{
  "summary": "Concise 1-sentence summary",
  "priority": "URGENT" | "Normal" | "Low",
  "needs_reply": true | false,
  "reply_draft": "Draft text here or null"
}}
"""

    response = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = response.content[0].text.strip()

    # Clean markdown json codeblock if present
    cleaned_json = response_text
    if "```json" in cleaned_json:
        cleaned_json = cleaned_json.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in cleaned_json:
        cleaned_json = cleaned_json.split("```", 1)[1].split("```", 1)[0].strip()

    try:
        data = json.loads(cleaned_json)
    except json.JSONDecodeError:
        # Regex extraction fallback if LLM included conversational wrapper
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
        else:
            # Fallback safe response
            data = {
                "summary": "Could not parse AI summary.",
                "priority": "Normal",
                "needs_reply": False,
                "reply_draft": None
            }

    # Normalize fields
    priority = data.get("priority", "Normal").upper()
    if "URGENT" in priority:
        data["priority"] = "URGENT"
    elif "LOW" in priority:
        data["priority"] = "Low"
    else:
        data["priority"] = "Normal"

    return data
