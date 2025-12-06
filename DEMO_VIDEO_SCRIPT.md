# 🎬 Pulse AI - Demo Video Script

> **Duration Target**: 3-5 minutes | **Format**: HD Screen Recording with Narration

---

## 📝 Script Outline

### 1️⃣ Introduction (0:00 - 0:30)

**[Show: Dashboard homepage]**

> "Hi, I'm Evelyn, and this is Pulse AI - an autonomous intelligence agent built with LangGraph that revolutionizes how we consume AI and machine learning news.

> The AI field moves incredibly fast. Every day there are new papers on ArXiv, trending repos on GitHub, blog posts from OpenAI, Anthropic, and more. Keeping up is nearly impossible.

> Pulse solves this by automatically scraping, summarizing, and publishing the most important AI news across multiple platforms."

---

### 2️⃣ LangGraph Architecture (0:30 - 1:30)

**[Show: agent.py file in code editor]**

> "Let me show you the core of Pulse - the LangGraph StateGraph.

> Here's where the magic happens. I'm using LangGraph's StateGraph to create a typed state machine. Each node in the graph handles a specific task:

> - **Scrape** pulls news from ArXiv, GitHub, RSS feeds, and tech blogs
> - **Dedupe** removes duplicates using embedding-based similarity
> - **Summarize** generates LLM-powered summaries using Groq's Llama 3.3
> - **Publish** posts to X, Medium, and other platforms
> - **Finalize** logs results and completes the pipeline

> What makes this powerful is the typed state management. I'm using TypedDict to define the AgentState, which tracks everything from raw items to summaries to errors.

> The state flows through each node, accumulating results. And notice the error handling pattern - errors are accumulated rather than breaking the pipeline."

**[Scroll to show the edge definitions]**

> "The edges define how nodes connect - creating a clean, linear flow from scrape to finalize."

---

### 3️⃣ Live Demo (1:30 - 3:30)

**[Switch to browser - Dashboard]**

> "Now let's see Pulse in action. This is the dashboard, built with Next.js 14 and Tailwind CSS."

**[Click "Fetch News" button]**

> "When I click 'Fetch News', the LangGraph agent kicks off. Watch the terminal..."

**[Show terminal with LangGraph node logs]**

> "You can see each node executing:
> - Scrape node fetching from multiple sources
> - Dedupe node filtering duplicates
> - Summarize node generating AI summaries"

**[Return to dashboard showing summaries]**

> "And now we have fresh AI news summaries, each with:
> - A 3-sentence summary for quick understanding
> - A social hook ready for Twitter
> - Auto-generated tags for categorization"

**[Click on Podcast player]**

> "What's really cool is the AI podcast feature. Pulse uses Edge TTS - which is completely free - to generate a podcast-style audio summary."

**[Play a few seconds of podcast]**

> "Professional quality narration, all generated automatically."

**[Click "Publish to Dev.to"]**

> "I can also publish directly to platforms. Let me post to Dev.to..."

**[Show success message]**

> "And it's live! The agent handled everything - formatting, tagging, and posting."

---

### 4️⃣ Technical Highlights (3:30 - 4:15)

**[Show code snippets or architecture diagram]**

> "A few technical highlights:

> - **Groq API** for blazing fast LLM inference - Llama 3.3 70B generates summaries in under a second
> - **Edge TTS** for free, high-quality text-to-speech
> - **SQLite** for persistence - all news items and summaries are stored
> - **Mock mode** for testing without burning API credits
> - **6 publishing platforms** - X, Medium, Bluesky, LinkedIn, Dev.to, and Mastodon"

---

### 5️⃣ Conclusion (4:15 - 4:45)

**[Return to dashboard]**

> "Pulse AI saves hours of manual curation. Instead of scrolling through dozens of sources, you get curated, summarized, and published content automatically.

> The LangGraph architecture makes it incredibly extensible - adding a new source or platform is just adding a new node.

> Thanks for watching! Check out the GitHub repo for the full code.

> This is Pulse AI - autonomous intelligence for staying ahead of the AI curve."

---

## 📋 Recording Checklist

Before recording:
- [ ] Clear browser history/tabs
- [ ] Set terminal font size to large (readable)
- [ ] Enable dark mode in code editor
- [ ] Have backend running (`python main.py`)
- [ ] Have frontend running (`npm run dev`)
- [ ] Test microphone levels
- [ ] Record in HD (1080p minimum)

Key moments to capture:
- [ ] Dashboard with gradient design
- [ ] LangGraph code in agent.py
- [ ] Terminal showing node execution logs
- [ ] Summary cards with tags
- [ ] Podcast player in action
- [ ] Successful publish notification

---

## 🎙️ Tips for Recording

1. **Speak clearly and at a moderate pace** - You have 5 minutes, don't rush
2. **Highlight the LangGraph integration** - This is the hackathon theme
3. **Show real functionality** - Live demos are more compelling than slides
4. **End with impact** - What problem does this solve?
