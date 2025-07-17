# Census Data Explorer

A natural language interface for exploring US Census data with AI-powered insights and visualizations. Ask questions about New York census data in plain English and get answers with interactive charts and data tables.

## Architecture

- **Frontend**: React + TypeScript + React Router 7 + Chart.js
- **Backend**: FastAPI + LangChain + Claude AI
- **Database**: PostgreSQL with census data

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Anthropic API key

### Running with Docker (Recommended)
```bash
# Set environment variables
export ANTHROPIC_API_KEY=your_api_key_here

# Start all services
docker compose up -d

# Bootstrap database with census data
make bootstrap_db
```

Access the application at http://localhost:3000

### Local Development
```bash
# Install dependencies
make install_deps

# Start database only
make run_db

# Start backend (separate terminal)
make run_backend

# Start frontend (separate terminal)
make run_frontend
```

## Configuration

The application uses environment variables for configuration:

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 5432)
- `DB_NAME` - Database name (default: data_agent)
- `DB_USER` - Database user (default: postgres)
- `DB_PASSWORD` - Database password (default: postgres)

## API Documentation

The backend API is built with FastAPI and provides automatic documentation:

- **Swagger UI**: http://localhost:8000/docs
