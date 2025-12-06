# 🏆 AI Demos Hackathon Submission - Pulse AI

## Project Information

### Project Title
**Pulse AI** - Autonomous AI Intelligence Agent

### Brief Description (Copy-paste ready for submission form)

> **Pulse AI** is an autonomous AI intelligence agent built with **LangGraph** that revolutionizes how we consume AI/ML news. It scrapes multiple sources (ArXiv, GitHub, RSS feeds, blogs), uses embedding-based deduplication to surface novel content, generates LLM-powered summaries via Groq (Llama 3.3 70B), and auto-publishes to 6 platforms (X, Medium, Bluesky, LinkedIn, Dev.to, Mastodon). 
>
> The LangGraph **StateGraph** orchestrates a typed 6-node pipeline: `scrape → dedupe → summarize → publish_x → publish_medium → finalize`. Each node handles a specific task with async execution and error accumulation. It even generates **AI podcasts** using Edge TTS (free!).
>
> **Real-world problem solved**: Information overload for AI researchers and enthusiasts. What takes hours of manual curation now happens automatically with intelligent filtering and multi-platform distribution.

---

## Links

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/tejiri-code/pulse-ai |
| **Demo Video** | *[Add Google Drive link after recording]* |
| **Screenshots/Artifacts** | *[Add Google Drive folder link]* |
| **Hosted Backend** | https://pulse-ai-nbje.onrender.com|
| **Hosted Frontend** | https://pulse-ai-liard.vercel.app/ |

---

## LangGraph Integration Details

### Core Framework Usage

Pulse uses **LangGraph** as the core agent framework:

```python
from langgraph.graph import StateGraph, END

# Define typed state
class AgentState(TypedDict):
    raw_items: List[Dict]
    unique_items: List[Dict]
    summaries: List[Dict]
    errors: Annotated[List[str], operator.add]
    step: str
    publish_to_x: bool
    publish_to_medium: bool

# Build the state graph
workflow = StateGraph(AgentState)
workflow.add_node("scrape", scrape_node)
workflow.add_node("dedupe", dedupe_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("publish_x", publish_x_node)
workflow.add_node("publish_medium", publish_medium_node)
workflow.add_node("finalize", finalize_node)

# Connect the nodes
workflow.add_edge("scrape", "dedupe")
workflow.add_edge("dedupe", "summarize")
# ... etc
```

### Key LangGraph Features

| Feature | Implementation |
|---------|---------------|
| StateGraph | 6-node typed pipeline |
| TypedDict State | `AgentState` with typed fields |
| Async Execution | `ainvoke` for non-blocking workflow |
| Error Handling | Accumulating pattern with `operator.add` |
| Conditional Logic | Publish flags in state control behavior |

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | **LangGraph** |
| LLM | Groq API (Llama 3.3 70B) |
| Backend | FastAPI + Python 3.11 |
| Frontend | Next.js 14 + Tailwind CSS |
| Database | SQLite |
| TTS | Edge TTS (FREE) |
| Platforms | X, Medium, Bluesky, LinkedIn, Dev.to, Mastodon |

---

## Demo Video Highlights

The 3-5 minute demo covers:

1. **Introduction** - The problem of AI information overload
2. **LangGraph Architecture** - Code walkthrough of StateGraph
3. **Live Demo** - Fetching news, viewing summaries, playing podcast
4. **Publishing** - Auto-posting to Dev.to/Mastodon
5. **Conclusion** - Real-world impact and extensibility

---

## Why Pulse Matters

### Problem
The AI/ML field moves incredibly fast. Researchers, engineers, and enthusiasts struggle to keep up with the constant stream of papers, GitHub repos, blog posts, and announcements.

### Solution
Pulse is an **autonomous agent** that acts as your personal AI news curator. It doesn't just aggregate—it **understands**, **filters**, **summarizes**, and **distributes** content across multiple platforms.

### Impact
- ⏱️ **Time Savings**: Hours of manual curation → automatic
- 🎯 **Quality Filtering**: Novelty scoring surfaces important content
- 📡 **Multi-Platform**: Reach audiences everywhere automatically
- 🎙️ **Accessibility**: Listen to AI news as a podcast
- 🔧 **Extensibility**: Easy to add new sources/platforms
