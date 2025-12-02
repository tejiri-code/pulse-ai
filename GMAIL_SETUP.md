# 📧 Gmail SMTP Setup Guide (5 minutes)

## Step 1: Enable 2-Factor Authentication

1. Go to your **Google Account**: https://myaccount.google.com/
2. Click **Security** in the left sidebar
3. Under "Signing in to Google", enable **2-Step Verification**
4. Follow the prompts to set it up (you'll need your phone)

## Step 2: Generate App Password

1. Still in **Security** settings, scroll down to "Signing in to Google"
2. Click **App passwords** (this option only appears if 2FA is enabled)
3. Click **Select app** → Choose **Mail**
4. Click **Select device** → Choose **Other (Custom name)**
5. Type: `Pulse AI Agent`
6. Click **Generate**
7. **Copy the 16-character password** (shown as: xxxx xxxx xxxx xxxx)

## Step 3: Configure Backend

Update your `backend/.env` file:

```bash
# Gmail SMTP Configuration
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx  # 16-character password (no spaces)
RECIPIENT_EMAIL=your.email@gmail.com  # Can be same or different email
```

## Step 4: Test It!

Restart your backend and test:

```bash
cd backend
python main.py
```

Then in another terminal:
```bash
curl -X POST http://localhost:8000/email/test
```

Or click the **"Send Daily Email"** button in your dashboard!

## ✅ Done!

You'll now receive beautiful HTML emails with:
- 📊 Daily AI news summaries
- 🏷️ Tags for each article
- 💅 Professional formatting
- 📧 Sent directly from your Gmail

---

**Troubleshooting:**
- Make sure you don't have spaces in the App Password
- Use the exact Gmail address that has 2FA enabled
- The App Password is different from your Gmail password!
