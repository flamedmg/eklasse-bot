# School Parent Assistant Bot

A Telegram bot that transforms school's schedule and email communication into a clean, organized Telegram experience for parents.

## Features

- 🗓️ Real-time schedule tracking
- 📧 School email notifications
- 📊 Academic performance monitoring
- 🔔 Smart notifications
- 💾 Historical data access

## Technical Stack

### Core Technologies
- Python 3.11+
- SQLite (data storage)
- Docker
- Telethon (Telegram client library)

### Key Libraries
- telethon (Telegram client)
- crawl4ai (web scraping)
- httpx (async HTTP client)
- SQLModel (SQLAlchemy-based ORM)
- Dramatiq (task queue with monitoring UI)
- Redis (message broker for Dramatiq)
- beautifulsoup4 (HTML parsing)
- pydantic (data validation)
- python-dotenv (environment management)

### Development Tools
- uv (package management)
- pytest (testing)
- black (code formatting)
- ruff (linting)

## Project Structure
```
school-parent-bot/
├── .env.example
├── README.md
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── crawlers/
│   │   ├── __init__.py
│   │   ├── schedule.py
│   │   └── email.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── schedule.py
│   │   └── notification.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_crawlers/
│   ├── test_services/
│   └── conftest.py
└── scripts/
    └── init_db.py
```

## Docker Setup

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file: .env
    volumes:
      - ./data:/app/data
    depends_on:
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  dramatiq:
    build: .
    command: python -m dramatiq src.tasks
    env_file: .env
    depends_on:
      - redis

  dramatiq-ui:
    image: ghcr.io/dramatiq/dramatiq-ui:latest
    environment:
      - DRAMATIQ_BROKER_URL=redis://redis:6379/0
    ports:
      - "8080:8080"
    depends_on:
      - redis
```

## Environment Variables

```env
# Telegram
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token

# School
SCHOOL_WEBSITE_URL=school_url
SCHOOL_EMAIL_SERVER=email_server
SCHOOL_EMAIL_USER=email_user
SCHOOL_EMAIL_PASSWORD=email_password

# Database
DATABASE_URL=sqlite:///data/school_bot.db

# Redis
REDIS_URL=redis://redis:6379/0
```

## Setup and Development

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your credentials
3. Run with Docker:
```bash
docker-compose up -d
```

Access Dramatiq UI at http://localhost:8080

## Local Development Setup

1. Install uv: `pip install uv`
2. Create virtual environment: `python -m venv .venv`
3. Activate virtual environment
4. Install dependencies: `uv pip install -r requirements.txt`
5. Run the bot: `python src/main.py`

## Testing

```bash
pytest tests/
```

## License

MIT License
