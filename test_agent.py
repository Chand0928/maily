"""
test_agent.py - Unit test suite for Email AI Agent.
Tests email parsing, payload extraction, MIME draft creation, and AI response parsing.
"""

import unittest
import base64
from unittest.mock import MagicMock
from agent import analyze_email
from gmail_tools import _extract_body_from_payload, create_draft_reply


class TestEmailAgent(unittest.TestCase):

    def test_extract_plain_text_payload(self):
        sample_text = "Hello, please send the weekly report by Friday."
        encoded_data = base64.urlsafe_b64encode(sample_text.encode('utf-8')).decode('utf-8')
        payload = {
            'mimeType': 'text/plain',
            'body': {'data': encoded_data}
        }
        extracted = _extract_body_from_payload(payload)
        self.assertEqual(extracted, sample_text)

    def test_extract_multipart_payload(self):
        plain_text = "Meeting at 3 PM today."
        encoded_data = base64.urlsafe_b64encode(plain_text.encode('utf-8')).decode('utf-8')
        payload = {
            'mimeType': 'multipart/alternative',
            'parts': [
                {
                    'mimeType': 'text/plain',
                    'body': {'data': encoded_data}
                }
            ]
        }
        extracted = _extract_body_from_payload(payload)
        self.assertEqual(extracted, plain_text)

    def test_analyze_email_urgent_mock(self):
        mock_client = MagicMock()
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text='''
        ```json
        {
          "summary": "Urgent deadline for financial audit by 5 PM.",
          "priority": "URGENT",
          "needs_reply": true,
          "reply_draft": "Hi Boss,\\n\\nI am finalizing the audit documents right now and will send them before 5 PM.\\n\\nBest regards,\\nVaibhav"
        }
        ```
        ''')]
        mock_client.messages.create.return_value = mock_msg

        fake_email = {
            'from': 'boss@company.com',
            'subject': 'Urgent: Audit files needed',
            'body': 'Need the audit files by 5 PM today without delay.'
        }

        result = analyze_email(fake_email, client=mock_client, user_name="Vaibhav")
        self.assertEqual(result['priority'], 'URGENT')
        self.assertTrue(result['needs_reply'])
        self.assertIn("audit", result['summary'].lower())
        self.assertIn("Vaibhav", result['reply_draft'])

    def test_analyze_email_newsletter_mock(self):
        mock_client = MagicMock()
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text='''
        {
          "summary": "Weekly 30% off tech accessories sale.",
          "priority": "Low",
          "needs_reply": false,
          "reply_draft": null
        }
        ''')]
        mock_client.messages.create.return_value = mock_msg

        fake_email = {
            'from': 'newsletter@store.com',
            'subject': 'Weekly Deals: 30% Off',
            'body': 'Check out our massive discounts on electronics this weekend.'
        }

        result = analyze_email(fake_email, client=mock_client, user_name="Vaibhav")
        self.assertEqual(result['priority'], 'Low')
        self.assertFalse(result['needs_reply'])
        self.assertIsNone(result['reply_draft'])

    def test_create_draft_reply_structure(self):
        mock_service = MagicMock()
        mock_drafts = MagicMock()
        mock_service.users.return_value.drafts.return_value = mock_drafts
        mock_drafts.create.return_value.execute.return_value = {'id': 'draft_123'}

        fake_email = {
            'id': 'msg_001',
            'threadId': 'thread_001',
            'from': 'colleague@company.com',
            'subject': 'Project timeline review',
            'message_id': '<12345@company.com>'
        }
        reply_text = "Thanks! The timeline looks good to me."

        draft = create_draft_reply(mock_service, fake_email, reply_text)
        self.assertEqual(draft['id'], 'draft_123')
        
        # Verify call arguments
        call_kwargs = mock_drafts.create.call_args[1]
        self.assertEqual(call_kwargs['userId'], 'me')
        self.assertEqual(call_kwargs['body']['message']['threadId'], 'thread_001')


if __name__ == '__main__':
    unittest.main()
