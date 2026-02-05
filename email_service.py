import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

# Email configuration - set these in your .env file
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def send_email(to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
    """
    Send an email using SMTP.
    Returns True if successful, False otherwise.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("⚠️ Email not configured. Set SMTP_USER and SMTP_PASSWORD in .env")
        print(f"Would send email to: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        return False
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        
        # Plain text version
        part1 = MIMEText(body, "plain")
        msg.attach(part1)
        
        # HTML version if provided
        if html_body:
            part2 = MIMEText(html_body, "html")
            msg.attach(part2)
        
        # Connect and send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_password_reset_email(to_email: str, reset_token: str, username: str) -> bool:
    """Send password reset email with token."""
    subject = "Password Reset Request"
    
    body = f"""
Hello {username},

You requested a password reset. Use this code to reset your password:

Reset Code: {reset_token}

This code will expire in 15 minutes.

If you didn't request this, please ignore this email.

Best regards,
Auth System
"""
    
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .code {{ background: #f0f0f0; padding: 15px 25px; font-size: 24px; font-weight: bold; 
                 letter-spacing: 3px; text-align: center; border-radius: 8px; margin: 20px 0; }}
        .footer {{ margin-top: 30px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Password Reset Request</h2>
        <p>Hello <strong>{username}</strong>,</p>
        <p>You requested a password reset. Use this code to reset your password:</p>
        <div class="code">{reset_token}</div>
        <p>This code will expire in <strong>15 minutes</strong>.</p>
        <p>If you didn't request this, please ignore this email.</p>
        <div class="footer">
            <p>Best regards,<br>Auth System</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, body, html_body)

# Placeholder functions for WhatsApp and Telegram
def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """
    Send message via WhatsApp Business API.
    Requires WhatsApp Business API credentials.
    """
    print(f"📱 WhatsApp message to {phone_number}: {message}")
    print("⚠️ WhatsApp integration not configured. Set up WhatsApp Business API.")
    return False

def send_telegram_message(telegram_id: str, message: str) -> bool:
    """
    Send message via Telegram Bot.
    Requires TELEGRAM_BOT_TOKEN in .env.
    """
    import os
    import requests
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    if not bot_token:
        print(f"📨 Telegram message to {telegram_id}: {message}")
        print("⚠️ Telegram not configured. Set TELEGRAM_BOT_TOKEN in .env")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = requests.post(url, json={
            "chat_id": telegram_id,
            "text": message
        })
        
        if response.status_code == 200:
            print(f"✅ Telegram message sent to {telegram_id}")
            return True
        else:
            print(f"❌ Telegram error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False
