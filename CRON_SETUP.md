# 🕐 Daily Email Cron Job Setup

## Quick Start

### 1. Set Recipient Email
```bash
# Add to backend/.env
DAILY_EMAIL_RECIPIENT=your.email@example.com
```

### 2. Run Cron Scheduler
```bash
cd backend
python cron_scheduler.py
```

You'll see:
```
🚀 Cron scheduler started!
📅 Daily email scheduled for 9:00 AM
⏰ Current time: 2025-12-03 09:05:00
```

---

## How It Works

1. **Automated Daily Emails** at 9:00 AM
2. **Fetches today's summaries** from database
3. **Sends beautiful HTML email** to configured recipient
4. **Logs every action** for tracking

---

## Configuration

### Change Email Time
Edit `cron_scheduler.py`:
```python
# Change "09:00" to your preferred time (24-hour format)
schedule.every().day.at("09:00").do(run_async_job, send_daily_email_job)
```

###  Multiple Recipients
Edit `.env`:
```bash
DAILY_EMAIL_RECIPIENT=person1@example.com,person2@example.com
```

---

## Run as Background Service

### Mac/Linux:
```bash
nohup python cron_scheduler.py > cron.log 2>&1 &
```

### Check if running:
```bash
ps aux | grep cron_scheduler
```

### Stop:
```bash
pkill -f cron_scheduler
```

---

## Logs

Watch live logs:
```bash
tail -f cron.log
```

You'll see:
```
🕐 2025-12-03 09:00:00 - Running daily email job...
📧 Sending daily report to your.email@example.com...
✅ Daily email sent successfully!
```

---

##  Production Deployment

For production, use a proper scheduler like **cron** (Linux/Mac) or **Task Scheduler** (Windows):

### Linux Cron:
```bash
# Edit crontab
crontab -e

# Add this line (runs at 9 AM daily)
0 9 * * * cd /path/to/backend && /usr/bin/python3 cron_scheduler.py
```

---

## Features

✅ **Automatic daily emails**
✅ **No manual intervention needed**
✅ **Configurable time**  
✅ **Error handling & logging**
✅ **Background operation**

**Your users get fresh AI news every morning!** ☕
