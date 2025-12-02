# Pulse AI Agent - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.11+
- Node.js 18+
- Terminal

### 1. Clone or Download
\`\`\`bash
# If you have the project locally, just navigate to it
cd pulse-ai-agent
\`\`\`

### 2. Backend Setup (2 minutes)

\`\`\`bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Keep USE_MOCK_MODE=True for testing
\`\`\`

### 3. Frontend Setup (2 minutes)

\`\`\`bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
\`\`\`

### 4. Run Everything (1 minute)

**Terminal 1 - Backend:**
\`\`\`bash
cd backend
source venv/bin/activate
python main.py
\`\`\`

**Terminal 2 - Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

**Terminal 3 - Test Agent (Optional):**
\`\`\`bash
cd backend
source venv/bin/activate
python tasks.py
\`\`\`

### 5. Open Browser

Visit: **http://localhost:3000**

## 🎯 First Actions

1. Click **"Fetch Latest News"** to scrape and process
2. View summaries on the dashboard
3. Click **"Publish to X"** to see mock Twitter posts
4. Explore **History**, **Daily Reports**, and **Weekly Reports**
5. Check **Settings** to configure sources

## 📝 Common Issues

**Port already in use?**
\`\`\`bash
# Backend
uvicorn main:app --port 8001

# Frontend
npm run dev -- -p 3001
\`\`\`

**Dependencies not installing?**
\`\`\`bash
# Python
pip install --upgrade pip
pip install -r requirements.txt

# Node.js
rm -rf node_modules package-lock.json
npm install
\`\`\`

## 🔧 Configuration

### Use Real APIs (Production Mode)

Edit \`backend/.env\`:
\`\`\`env
USE_MOCK_MODE=False
OPENAI_API_KEY=sk-...
TWITTER_BEARER_TOKEN=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_SECRET=...
MEDIUM_INTEGRATION_TOKEN=...
\`\`\`

### Change Backend URL

Edit \`frontend/.env.local\`:
\`\`\`env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
\`\`\`

## 🎬 Demo Mode

Perfect for presentations:
1. Keep \`USE_MOCK_MODE=True\`
2. Run \`python tasks.py\` to populate database
3. Refresh frontend to see data
4. Click publish buttons to see mock outputs

## 📚 Learn More

- [README.md](README.md) - Full documentation
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - Presentation guide
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File overview

---

**Questions?** Check the README or raise an issue!
