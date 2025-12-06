# Contributing to Pulse AI

Thank you for your interest in contributing to Pulse AI! 🎉

## How to Contribute

### Reporting Bugs
1. Check if the issue already exists in [Issues](https://github.com/tejiri-code/pulse-ai/issues)
2. Use the bug report template when creating a new issue
3. Include steps to reproduce, expected vs actual behavior

### Suggesting Features
1. Open a feature request issue using the template
2. Describe the problem you're solving
3. Explain your proposed solution

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes with clear commit messages
4. Run tests: `pytest` (backend) and `npm test` (frontend)
5. Submit a PR with a clear description

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Max line length: 100 characters

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow ESLint configuration
- Use functional components with hooks

## Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

## Questions?

Open a discussion or reach out to the maintainers!
