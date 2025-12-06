# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] - 2024-12-06

### Added
- **LangGraph StateGraph pipeline** with 6 typed nodes
- **Multi-source scraping**: ArXiv, GitHub Trending, RSS feeds, tech blogs
- **Embedding-based deduplication** with novelty scoring
- **LLM-powered summarization** via Groq (Llama 3.3 70B)
- **AI podcast generation** using Edge TTS (free!)
- **Publishing to 6 platforms**: X, Medium, Bluesky, LinkedIn, Dev.to, Mastodon
- **Next.js 14 dashboard** with real-time summaries
- **Daily & weekly report** generation
- **Mock mode** for testing without API credentials
- **SQLite database** for persistence

### Technical Highlights
- Async execution with `ainvoke`
- Error accumulation pattern for robust pipelines
- TypedDict state management
- Full CORS support

### Initial Contributors
- [@tejiri-code](https://github.com/tejiri-code) (Evelyn) - Project creator

---

## Commit History Highlights

| Date | Commit | Description |
|------|--------|-------------|
| 2024-12-06 | `v1.0.0` | Initial open source release |
| 2024-12-05 | `feat/podcast` | Added AI podcast generation with Edge TTS |
| 2024-12-04 | `feat/publishers` | Multi-platform publishing support |
| 2024-12-03 | `feat/dashboard` | Next.js 14 dashboard implementation |
| 2024-12-02 | `feat/langgraph` | LangGraph StateGraph integration |
| 2024-12-01 | `feat/scraping` | Multi-source news scraping |
| 2024-11-30 | `init` | Project initialization |
