# 🤖 Pulse - Autonomous AI Intelligence Agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/next.js-14-black.svg)](https://nextjs.org/)

> **Pulse** is an autonomous AI agent that scrapes, processes, summarizes, and auto-publishes AI/ML news to X (Twitter) and Medium. Built for the hackathon with real-world impact in mind.

![Pulse Dashboard](https://via.placeholder.com/800x400/1a1a1a/4ade80?text=Pulse+AI+Dashboard)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Mock Mode](#mock-mode)
- [Judges Pitch](#judges-pitch)
- [License](#license)

## 🎯 Overview

Pulse is a fully autonomous AI intelligence agent that:

1. **Scrapes** AI/ML news from ArXiv, GitHub Trending, RSS feeds, and blogs
2. **Deduplicates** using embedding-based similarity matching
3. **Scores** novelty to surface the most interesting content
4. **Summarizes** each item with 3-sentence summaries + 30-word social hooks
5. **Auto-tags** content using LLM-powered classification
6. **Publishes** daily updates to **X (Twitter)** via API v2
7. **Publishes** weekly long-form deep dives to **Medium** as draft articles
8. **Generates** daily email briefs and weekly reports
9. **Displays** everything in a beautiful real-time dashboard

## ✨ Features

### Backend Features
- **LangGraph StateGraph** - Typed state machine with node-based pipeline (scrape → dedupe → summarize → publish)
- **Multi-source scraping**: ArXiv, GitHub, RSS, blogs
- **Embedding-based deduplication** with novelty scoring
- **LLM-powered summarization** via Groq API (Llama 3.3 70B)
- **Multi-platform publishing**: X, Medium, Bluesky, LinkedIn, Dev.to, Mastodon
- **AI Podcast generation** via ElevenLabs TTS
- **SQLite database** for persistence
- **FastAPI REST API** with full CORS support
- **Mock mode** for testing without API keys

### Frontend Features
- **Next.js 14** with App Router
- **Tailwind CSS** with dark mode
- **Real-time dashboard** showing latest summaries
- **History page** with tag filtering
- **Daily & weekly reports** with formatted display
- **Settings page** for configuration
- **Beautiful gradient designs** with glassmorphism
- **Responsive** and mobile-friendly

## 🏗️ Architecture

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                         PULSE AI AGENT                          │
│                                                                 │
│  ┌───────────────┐      ┌──────────────────┐                  │
│  │   Scrapers    │──────▶│   Embeddings     │                  │
│  │ • ArXiv       │      │ • Deduplication  │                  │
│  │ • GitHub      │      │ • Novelty Score  │                  │
│  │ • RSS         │      └──────────────────┘                  │
│  │ • Blogs       │               │                             │
│  └───────────────┘               │                             │
│                                  ▼                             │
│                      ┌──────────────────┐                      │
│                      │   LangGraph      │                      │
│                      │   Agent Flow     │                      │
│                      │ • Scrape         │                      │
│                      │ • Dedupe         │                      │
│                      │ • Summarize      │                      │
│                      │ • Classify       │                      │
│                      │ • Store          │                      │
│                      │ • Publish        │                      │
│                      └──────────────────┘                      │
│                               │                                │
│                  ┌────────────┴────────────┐                  │
│                  ▼                         ▼                   │
│         ┌────────────────┐        ┌────────────────┐          │
│         │   X (Twitter)  │        │     Medium     │          │
│         │   Daily Posts  │        │  Weekly Drafts │          │
│         └────────────────┘        └────────────────┘          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                  SQLite Database                        │  │
│  │  • News Items  • Summaries  • Reports  • Posts         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                  FastAPI Backend                        │  │
│  │  /fetch  /summaries  /publish/daily  /publish/weekly   │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                   ┌──────────┴──────────┐
                   │   Next.js Frontend  │
                   │ • Dashboard         │
                   │ • History           │
                   │ • Reports           │
                   │ • Settings          │
                   └─────────────────────┘
\`\`\`

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **npm or yarn**

### Backend Setup

1. Navigate to backend directory:
\`\`\`bash
cd backend
\`\`\`

2. Create virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Configure environment:
\`\`\`bash
cp .env.example .env
# Edit .env with your API keys (or leave USE_MOCK_MODE=True)
\`\`\`

### Frontend Setup

1. Navigate to frontend directory:
\`\`\`bash
cd frontend
\`\`\`

2. Install dependencies:
\`\`\`bash
npm install
\`\`\`

3. Configure environment:
\`\`\`bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
\`\`\`

## 🚀 Running Locally

### Start Backend

\`\`\`bash
cd backend
source venv/bin/activate
python main.py
# or
uvicorn main:app --reload
\`\`\`

Backend runs on: **http://localhost:8000**

### Start Frontend

\`\`\`bash
cd frontend
npm run dev
\`\`\`

Frontend runs on: **http://localhost:3000**

### Test the Agent

1. Open http://localhost:3000
2. Click **"Fetch Latest News"** to scrape and process news
3. Click **"Publish to X"** or **"Publish to Medium"** to test publishing
4. Check the terminal for detailed logs

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and API info |
| `/fetch` | POST | Scrape and process new news |
| `/summaries` | GET | Get all summaries |
| `/summaries/generate` | POST | Generate summaries for items |
| `/publish/daily` | POST | Run daily workflow + post to X |
| `/publish/weekly` | POST | Run weekly workflow + post to Medium |
| `/daily_report` | GET | Get daily email report |
| `/weekly_report` | GET | Get weekly deep dive report |

## 🌐 Deployment

### Backend (Render / Fly.io)

**Render.com:**

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env.example`

**Fly.io:**

\`\`\`bash
cd backend
fly launch
fly deploy
\`\`\`

### Frontend (Vercel)

1. Install Vercel CLI:
\`\`\`bash
npm i -g vercel
\`\`\`

2. Deploy:
\`\`\`bash
cd frontend
vercel
\`\`\`

3. Set environment variable: `NEXT_PUBLIC_API_URL=<your-backend-url>`

## 🎭 Mock Mode

Pulse includes a **mock mode** that simulates all API calls without requiring real credentials. Perfect for:

- **Testing** the complete pipeline
- **Demos** without live posting
- **Development** without API rate limits

To enable mock mode, set in `backend/.env`:
\`\`\`
USE_MOCK_MODE=True
\`\`\`

Mock mode will:
- ✅ Generate fake news data
- ✅ Create realistic summaries
- ✅ Log "posts" to console instead of X/Medium
- ✅ Show full workflow execution

## 🏆 Judges Pitch

### Why Pulse Matters

**Problem**: The AI/ML field moves incredibly fast. Researchers, engineers, and enthusiasts struggle to keep up with the constant stream of papers, GitHub repos, blog posts, and announcements.

**Solution**: Pulse is an **autonomous agent** that acts as your personal AI news curator. It doesn't just aggregate—it **understands**, **filters**, **summarizes**, and **distributes** content across multiple platforms.

### Real-World Impact

1. **Time Savings**: What takes hours of manual curation now happens automatically
2. **Quality Filtering**: Novelty scoring surfaces truly important developments
3. **Multi-Platform**: Reaches audiences on X (Twitter) and Medium automatically
4. **Actionable Summaries**: 3-sentence summaries + social hooks = instant understanding
5. **Production-Ready**: Mock mode, error handling, database persistence

### Technical Merit

- **Modern Stack**: LangChain/LangGraph for autonomous agents, Next.js 14 for UI
- **Scalable Architecture**: Modular design, easy to add new sources/publishers
- **Production Features**: Error handling, logging, mock mode, CORS, TypeScript
- **Beautiful UX**: Gradient designs, dark mode, responsive, glassmorphism
- **Full Integration**: Actually uses Twitter API v2 and Medium API (not just mocks)

### Extensibility

Pulse can easily be extended to:
- Add more news sources (Reddit, HackerNews, Discord)
- Support more platforms (LinkedIn, Substack, YouTube)
- Add personalization (user preferences, ML-based filtering)
- Include email notifications via SendGrid/Mailgun
- Add analytics and engagement tracking

---

**Built with** ❤️ **for the hackathon by Evelyn**

License: MIT
