# 🔑 API Keys Setup Guide

## Quick Setup (5 minutes)

Your Pulse AI Agent now supports **user-specific API keys** for publishing to Twitter/X and Medium!

### How It Works

1. **Navigate to Settings**: Click "Settings" in the sidebar
2. **Enter API Keys**: Paste your Twitter and Medium credentials
3. **Save**: Keys are stored in your browser (localStorage)
4. **Publish**: Your personal accounts will be used when publishing

---

## Getting Twitter/X API Keys

### Step 1: Developer Account
1. Go to https://developer.twitter.com/en/portal/dashboard  
2. Create a developer account (if you don't have one)
3. Create a new "Project" and "App"

### Step 2: Get Credentials
1. In your app settings, go to "Keys and tokens"
2. Copy these 4 values:
   - **Consumer Key** (API Key)
   - **Consumer Secret** (API Secret)
   - **Access Token**
   - **Access Token Secret**

### Step 3: Set Permissions
- Make sure your app has **Read and Write** permissions
- You may need to apply for "Elevated" access for API v1.1

### Step 4: Paste in Settings
- Go to Settings page in Pulse AI Agent
- Paste all 4 values
- Click "Save Settings"

---

## Getting Medium Integration Token

### Step 1: Medium Settings
1. Log in to Medium
2. Go to https://medium.com/me/settings/security
3. Scroll to "Integration tokens"

### Step 2: Generate Token
1. Click "Get integration token"
2. Give it a description (e.g., "Pulse AI Agent")
3. Copy the generated token

### Step 3: Paste in Settings
- Go to Settings page in Pulse AI Agent
- Paste token in "Medium Integration Token"
- Click "Save Settings"

---

## ✅ You're Ready!

Now when you click:
- **"Publish to X"** → Uses YOUR Twitter account
- **"Publish to Medium"** → Uses YOUR Medium account

### Privacy Note
- API keys stored **locally** in your browser
- Never sent to our servers
- Only used when YOU click publish
- Clear with "Clear All" button anytime

---

## Troubleshooting

**"Mock mode" response?**
- Backend doesn't have credentials set
- Check that you saved settings
- Make sure API keys are valid

**429 Rate Limit Error?**
- Twitter free tier: 50 tweets/day
- Wait and try again later
- Consider Twitter API Pro plan

**401 Unauthorized?**
- Check API key permissions
- Regenerate tokens if needed
- Verify "Read and Write" access
