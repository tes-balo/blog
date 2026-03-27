# Blog API

A FastAPI-based REST API for managing blog posts with PostgreSQL database support.

## Features

- **Blog Posts Management**: Full CRUD operations for blog posts
- **JWT Authentication**: Secure token-based authentication system
- **Async Database**: PostgreSQL with async SQLAlchemy support
- **Database Migrations**: Alembic for version-controlled schema changes
- **Data Validation**: Pydantic models for request/response validation
- **Security**: Built-in security headers and CORS middleware
- **API Documentation**: Interactive Swagger UI at `/docs`

## Tech Stack

- **Framework**: FastAPI 0.129+
- **Database**: PostgreSQL with SQLAlchemy 2.0+ (async)
- **Migrations**: Alembic
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: pwdlib with argon2
- **Python**: 3.12+

## Project Structure

```
blog/
├── alembic/               # Database migrations
│   └── versions/          # Migration scripts
├── docs/                  # Documentation
│   ├── api.md
│   ├── architecture.md
│   └── authentication.md
├── scripts/               # Utility scripts
│   └── seed_posts.py      # Database seeding
├── src/
│   └── app/
│       ├── api/          # API routes
│       │   └── routes/   # Route handlers (auth, posts, users)
│       ├── core/          # Core configurations
│       │   ├── config.py  # Settings management
│       │   ├── metadata.py # API metadata
│       │   ├── security.py # Auth utilities
│       │   └── middleware/ # CORS, logging, security headers
│       ├── db/            # Database layer
│       │   ├── database.py
│       │   └── tables/    # SQLAlchemy table definitions
│       ├── schemas/       # Pydantic models
│       ├── repositories/  # Data access layer
│       ├── services/      # Business logic
│       └── main.py        # Application entry point
├── pyproject.toml        # Project configuration
└── alembic.ini           # Alembic configuration
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Poetry (optional, for dependency management)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tes-balo/blog.git
   cd blog
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog
   DATABASE_URL_SYNC=postgresql://user:password@localhost:5432/blog
   JWT_SECRET=your-secret-key
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_SECONDS=3600
   DEBUG=true
   ENVIRONMENT=development
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/sign-in` | Sign in and get JWT token |

### Blog Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts` | Get all posts |
| GET | `/posts/{id}` | Get a post by ID |
| POST | `/posts` | Create a new post |
| PATCH | `/posts/{id}` | Update a post |
| DELETE | `/posts/{id}` | Delete a post |

### Request/Response Examples

**Create a Post**
```json
POST /posts
{
  "title": "My First Blog Post",
  "content": "This is the content of my blog post.",
  "published": true
}
```

**Post Response**
```json
{
  "id": "uuid-here",
  "title": "My First Blog Post",
  "content": "This is the content of my blog post.",
  "published": true,
  "created_at": "2026-03-27T08:00:00Z",
  "updated_at": null
}
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project uses:
- **Ruff** for linting and formatting
- **MyPy** for type checking

```bash
# Run linter
ruff check .

# Format code
ruff format .

# Type check
mypy src/
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## License

This project is licensed under the Apache 2.0 License.
