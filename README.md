# Tatami E-commerce Capstone Project: Back-end

A robust and scalable e-commerce backend built with Python, Flask, and SQLAlchemy. 
This project implements RESTful API endpoints, secure authentication, and efficient 
database management while maintaining clean architecture principles.

## Project Philosophy

Our backend development focuses on:

- Clean architecture with clear separation of concerns
- RESTful API design principles
- Secure data handling and authentication
- Efficient database operations
- Comprehensive testing

## Tech Stack

- **Backend Programming Language:** Python
- **Web Framework:** Flask
- **Database ORM:** SQLAlchemy
- **API Design:** Flask Blueprint
- **Cross-Origin Resource Sharing:** Flask-CORS
- **Database Migrations:** Alembic
- **Authentication:** AWS Cognito
- **Payment Processing:** Stripe
- **Testing:** pytest

## Project Structure

```
app/
├── models/          # Database models and schemas
├── routes/          # API endpoints and route handlers
├── services/        # Business logic and service layer
│   ├── __init__.py
│   ├── db.py       # Database service
│   └── exceptions.py # Custom exceptions
├── migrations/      # Database migration files
└── tests/          # Test suites

```

## Getting Started

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize database and run migrations:

```bash
flask db upgrade
```

5. Start development server:

```bash
flask run
```

### API Endpoints

Our API provides endpoints for:

- Product management (CRUD operations)
- User authentication and authorization
- Shopping cart operations
- Order processing
- Payment integration

## Key Components

- **Models**: Database schemas and relationships
- **Routes**: API endpoint definitions using Blueprint
- **Services**: Business logic implementation
- **Migrations**: Database version control
- **Tests**: Comprehensive test coverage

### Environment Variables and Configuration

Required environment variables:

1. **Database Configuration**
   - DATABASE_URL
   - DATABASE_TEST_URL

2. **AWS Configuration**
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_REGION
   - COGNITO_USER_POOL_ID
   - COGNITO_APP_CLIENT_ID

3. **Stripe Configuration**
   - STRIPE_SECRET_KEY
   - STRIPE_WEBHOOK_SECRET

Note: Add all sensitive configuration values to your `.env` file and ensure it's listed in `.gitignore`.

## Database Management

We use SQLAlchemy for database operations and Alembic for migrations:

- Create migration: `flask db migrate -m "description"`
- Apply migrations: `flask db upgrade`
- Rollback migrations: `flask db downgrade`

## Testing

Run tests with pytest:

```bash
pytest
```

## Deployment

Deployed under Heroku

## Working with the Frontend

This backend connects to our React Frontend.

Key integration points:
- RESTful API endpoints
- AWS Cognito authentication
- Stripe payment processing
- Cross-origin resource sharing (CORS)
- Error handling and status codes

## Link to frontend

https://github.com/tagaertner/tatami-store-front-end.git

## Final project link
https://tatami-store-fe-4a4f67c5b2c2.herokuapp.com/

## Team

Tatiana Trofimova & Tami Gaertner

## License

This project is licensed under the MIT License