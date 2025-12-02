# 🎬 Pulse AI Agent - Demo Script (3-5 Minutes)

This script guides you through a complete demonstration of Pulse for judges and stakeholders.

## 🎯 Demo Overview

1. **Introduction** (30 seconds)
2. **Backend Pipeline** (90 seconds)
3. **Frontend Dashboard** (90 seconds)
4. **Publishing to X & Medium** (60 seconds)
5. **Closing** (30 seconds)

---

## 1. Introduction (30 seconds)

> "Hi! I'm excited to show you **Pulse** - an autonomous AI intelligence agent that automatically curates, processes, and publishes AI/ML news to Twitter and Medium.
>
> Pulse solves a real problem: staying up-to-date with AI/ML developments is overwhelming. Pulse does the heavy lifting by scraping multiple sources, filtering for novelty, generating summaries, and auto-publishing across platforms.
>
> Let me show you how it works!"

---

## 2. Backend Pipeline Demo (90 seconds)

### Terminal Window - Backend

\`\`\`bash
cd backend
source venv/bin/activate
python tasks.py
\`\`\`

**Narration:**

> "The backend is powered by a LangGraph agent that runs through a complete pipeline:
>
> 1. **Scraping** - Watch as it pulls from ArXiv, GitHub Trending, RSS feeds, and AI blogs [point to terminal output]
>
> 2. **Deduplication** - Using sentence embeddings, it identifies and removes duplicates. See the novelty scores? Those tell us how unique each article is [point to scores]
>
> 3. **Summarization** - Each article gets a 3-sentence summary PLUS a 30-word social hook optimized for Twitter
>
> 4. **Auto-tagging** - The LLM automatically classifies content with relevant tags
>
> 5. **Storage** - Everything is persisted to a SQLite database
>
> Notice we're in **MOCK MODE** - the agent simulates Twitter and Medium posts without actually publishing. Perfect for this demo!"

**Key things to show in terminal:**
- ✅ Scraping logs
- ✅ Novelty scores
- ✅ Mock Twitter post preview
- ✅ Mock Medium article preview

---

## 3. Frontend Dashboard Demo (90 seconds)

### Browser - http://localhost:3000

**Navigate through pages:**

#### Dashboard Page
> "Here's the main dashboard. This shows today's AI news summaries in real-time.
>
> - **Stat cards** show total summaries, today's count, and average novelty
> - **Action buttons** let you fetch news, publish to Twitter, or publish to Medium
> - Each **summary card** shows the 3-sentence summary, social hook, tags, and novelty score
>
> Let me click 'Fetch Latest News'..." [Click button, show loading, show results]

#### History Page
> "The History page lets you browse all past summaries with **tag filtering**. 
> 
> Click any tag to filter..." [Click a tag like 'AI' or 'GPT']

#### Daily Report
> "Daily reports compile all the day's news into an email-ready format.
>
> You can select different dates..." [Change date selector]

#### Weekly Report
> "Weekly reports are long-form deep dives - perfect for Medium.
>
> This shows the full markdown article that would be posted as a draft." [Scroll through content]

#### Settings
> "Settings let you configure:
> - Auto-publishing schedules
> - Which sources to scrape
> - Daily/weekly timing
> - Mock mode toggle"

---

## 4. Publishing Demo (60 seconds)

### Back to Dashboard

**Narration:**

> "Now let's test the publishing workflow.
>
> Click **'Publish to X'**..." [Click button]
>
> "In mock mode, you see the console output showing exactly what would be posted.
> In production, this uses the Twitter API v2 to actually post tweets.
>
> Now let's try **'Publish to Medium'**..." [Click button]
>
> "Same thing - in production this creates a draft article on Medium using their API.
> The draft status means you can review before publishing - perfect for quality control!"

**Show in terminal:**
- Mock Twitter post with tweet text
- Mock Medium post with title and content preview

---

## 5. Technical Highlights & Closing (30 seconds)

**Narration:**

> "Quick technical highlights:
>
> - **Backend**: Python, FastAPI, LangChain, LangGraph, SQLite
> - **Frontend**: Next.js 14, TypeScript, Tailwind CSS
> - **APIs**: Twitter API v2, Medium API
> - **Features**: Embedding-based deduplication, novelty scoring, LLM summarization
> - **Production-ready**: Error handling, logging, mock mode, CORS, responsive design
>
> Pulse is **extensible** - you can easily add more sources (Reddit, HackerNews), more platforms (LinkedIn, Substack), or personalization features.
>
> Most importantly, Pulse has real-world impact: it saves hours of manual curation and ensures you never miss important AI developments.
>
> Thanks for watching! Questions?"

---

## 📊 Key Metrics to Highlight

- ✅ **5 news sources** (ArXiv, GitHub, RSS, Blogs, configurable)
- ✅ **2 publishing platforms** (X/Twitter, Medium)
- ✅ **3-sentence summaries** for quick reading
- ✅ **30-word social hooks** optimized for engagement
- ✅ **Novelty scoring** to surface important content
- ✅ **Mock mode** for safe testing
- ✅ **100% autonomous** once configured

---

## 🎥 Recording Tips

1. **Screen recording**: Use OBS or QuickTime
2. **Window layout**: Terminal (left) + Browser (right)
3. **Pre-populate**: Run the agent once before recording so there's data
4. **Smooth navigation**: Practice the flow 2-3 times
5. **Voiceover**: Record separately for clarity, or do live
6. **Length**: Aim for 3-4 minutes, max 5 minutes

---

## 🚀 Quick Start Commands

**Terminal 1 - Backend:**
\`\`\`bash
cd backend
source venv/bin/activate
python main.py
\`\`\`

**Terminal 2 - Agent Test:**
\`\`\`bash
cd backend
source venv/bin/activate
python tasks.py
\`\`\`

**Terminal 3 - Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

**Browser:**
\`\`\`
http://localhost:3000
\`\`\`

---

## 📸 Screenshot Checklist

- [ ] Dashboard with summaries loaded
- [ ] History page with tag filters
- [ ] Daily report with date selector
- [ ] Weekly report full article
- [ ] Settings page
- [ ] Terminal showing agent pipeline
- [ ] Mock Twitter post output
- [ ] Mock Medium post output

---

**Good luck with your demo! 🎉**
