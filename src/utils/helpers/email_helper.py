# import os
# import imaplib
# import email
# import re
# from dotenv import load_dotenv
#
# # Load env vars
# load_dotenv()
#
# GMAIL_USER = os.getenv("GMAIL_USER")
# GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
#
#
# def get_login_details():
#     # Connect to Gmail
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#     mail.select("inbox")
#
#     # Search for unread emails first
#     result, data = mail.search(None, '(UNSEEN)')
#     if not data[0]:
#         # If no unread, get all emails
#         result, data = mail.search(None, "ALL")
#
#     if not data[0]:
#         raise ValueError("No emails found in inbox.")
#
#     # Get the latest email
#     latest_email_id = data[0].split()[-1]
#
#     # (RFC822) Fetch the email content
#     result, msg_data = mail.fetch(latest_email_id, "(RFC822)")
#
#     raw_email = None
#     for response_part in msg_data:
#         if isinstance(response_part, tuple):
#             raw_email = response_part[1]
#             break
#
#     if raw_email is None:
#         raise ValueError("Could not fetch email content.")
#
#     email_message = email.message_from_bytes(raw_email)
#
#     # Extract email body
#     email_body = ""
#     if email_message.is_multipart():
#         for part in email_message.walk():
#             if part.get_content_type() == "text/plain":
#                 email_body = part.get_payload(decode=True).decode(errors="ignore")
#                 break
#     else:
#         email_body = email_message.get_payload(decode=True).decode(errors="ignore")
#
#     # Extract login details using patterns
#     email_match = re.search(r"Email:\s*([^\n\r]+)", email_body, re.IGNORECASE)
#     password_match = re.search(r"Password:\s*([^\n\r]+)", email_body, re.IGNORECASE)
#
#     login_email = email_match.group(1).strip() if email_match else None
#     login_password = password_match.group(1).strip() if password_match else None
#
#     return login_email, login_password
