# Pulse AI Agent - Project Structure

\`\`\`
pulse-ai-agent/
│
├── README.md                 # Main documentation
├── LICENSE                   # MIT License
├── DEMO_SCRIPT.md           # 3-5 minute demo guide
│
├── backend/                  # Python FastAPI Backend
│   ├── main.py              # FastAPI application & REST endpoints
│   ├── agent.py             # LangGraph autonomous agent
│   ├── scraper.py           # Multi-source news scraping
│   ├── dedupe.py            # Embedding-based deduplication
│   ├── summaries.py         # LLM-powered summarization
│   ├── publisher_x.py       # Twitter/X API v2 integration
│   ├── publisher_medium.py  # Medium API integration
│   ├── db.py                # SQLite database models & helpers
│   ├── models.py            # Pydantic data models
│   ├── tasks.py             # Scheduled task runner
│   ├── test_data.py         # Demo test data
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variable template
│   └── pulse.db             # SQLite database (created at runtime)
│
└── frontend/                # Next.js 14 Frontend
    ├── app/
    │   ├── layout.tsx       # Root layout with dark theme
    │   ├── page.tsx         # Dashboard (main page)
    │   ├── history/
    │   │   └── page.tsx     # News archive with filters
    │   ├── reports/
    │   │   ├── daily/
    │   │   │   └── page.tsx # Daily report viewer
    │   │   └── weekly/
    │   │       └── page.tsx # Weekly report viewer
    │   └── settings/
    │       └── page.tsx     # Settings & configuration
    │
    ├── components/
    │   ├── Navbar.tsx       # Navigation bar
    │   ├── SummaryCard.tsx  # News summary card
    │   └── TagChip.tsx      # Tag filter chip
    │
    ├── lib/
    │   └── api.ts           # API client wrapper
    │
    ├── types/
    │   └── index.ts         # TypeScript type definitions
    │
    ├── package.json         # Node.js dependencies
    ├── tsconfig.json        # TypeScript configuration
    ├── next.config.js       # Next.js configuration
    └── tailwind.config.js   # Tailwind CSS configuration
\`\`\`

## File Descriptions

### Backend Core Files

- **main.py**: FastAPI REST API with endpoints for fetching, summarizing, and publishing
- **agent.py**: LangGraph state machine orchestrating the complete pipeline
- **scraper.py**: Async scrapers for ArXiv, GitHub, RSS, and blogs
- **dedupe.py**: Sentence transformer embeddings + cosine similarity for deduplication
- **summaries.py**: OpenAI GPT integration for summaries, hooks, and tags
- **publisher_x.py**: Twitter API v2 client with mock mode
- **publisher_medium.py**: Medium API client with draft posting
- **db.py**: SQLAlchemy models and database helpers
- **tasks.py**: Cron-style scheduler for daily/weekly automation

### Frontend Core Files

- **page.tsx**: Dashboard with real-time summaries and action buttons
- **history/page.tsx**: Filterable archive of all summaries
- **reports/daily/page.tsx**: Daily email-format brief
- **reports/weekly/page.tsx**: Long-form Medium article preview
- **settings/page.tsx**: Configuration UI for sources, schedules, and publishing

### Configuration Files

- **.env.example**: Template for API keys and settings
- **requirements.txt**: Python package dependencies
- **package.json**: Node.js package dependencies

## Key Technologies

### Backend Stack
- **FastAPI** - Modern async Python web framework
- **LangChain** - LLM orchestration and chains
- **LangGraph** - Stateful agent workflows
- **SQLAlchemy** - ORM for database operations
- **Sentence Transformers** - Embedding generation
- **httpx** - Async HTTP client
- **BeautifulSoup** - HTML parsing

### Frontend Stack
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Hooks** - State management

### APIs & Services
- **Twitter API v2** - Social media posting
- **Medium API** - Blog article publishing
- **OpenAI API** - LLM summarization
- **ArXiv API** - Research paper access
- **GitHub** - Trending repository scraping

## Environment Variables

### Backend (.env)
\`\`\`env
OPENAI_API_KEY=your_key
TWITTER_BEARER_TOKEN=your_token
MEDIUM_INTEGRATION_TOKEN=your_token
USE_MOCK_MODE=True
\`\`\`

### Frontend (.env.local)
\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

## Running the Project

1. **Backend**: \`cd backend && python main.py\`
2. **Frontend**: \`cd frontend && npm run dev\`
3. **Visit**: http://localhost:3000

Enjoy! 🚀
