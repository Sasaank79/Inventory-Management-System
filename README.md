# Inventory Management System

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue.svg)
![Build](https://github.com/Sasaank79/Inventory-Management-System/workflows/CI/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A production-ready inventory management system built with Flask and PostgreSQL, featuring JWT authentication, RESTful APIs, and real-time analytics.

## Features

- **Authentication**: Secure JWT-based authentication with password hashing
- **Product Management**: Full CRUD operations with SKU tracking and categorization
- **Supplier Management**: Maintain supplier relationships and contact information
- **Inventory Tracking**: Transaction-based stock management (IN/OUT)
- **Analytics**: Real-time insights including top-selling products, low stock alerts, and inventory valuation
- **RESTful API**: Clean API design with proper HTTP status codes and JSON responses
- **Pagination & Search**: Efficient data browsing with server-side pagination
- **Docker Support**: Complete containerization for local development and production
- **CI/CD**: Automated testing and linting via GitHub Actions

## Architecture

![Architecture Diagram](docs/architecture.png)

The system follows a three-tier architecture:
- **Frontend**: Browser-based interface
- **Backend**: Flask application with modular route blueprints (Auth, Products, Suppliers, Transactions, Analytics)
- **Database**: PostgreSQL with strict 3NF schema design

## Tech Stack

- **Backend**: Python 3.11, Flask 3.0
- **Database**: PostgreSQL 15, SQLAlchemy ORM
- **Authentication**: JWT (PyJWT)
- **Testing**: pytest, pytest-cov
- **Linting**: flake8
- **Server**: Gunicorn
- **Containerization**: Docker, Docker Compose
- **Cloud**: Render (managed PostgreSQL + web service)

## Local Setup

### Using Docker (Recommended)

```bash
git clone https://github.com/Sasaank79/Inventory-Management-System.git
cd Inventory-Management-System

docker-compose up --build
```

The application will be available at `http://localhost:5000`.

Default credentials:
- **Username**: `admin`
- **Password**: `SecurePass123!`

### Manual Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set your ADMIN_USERNAME and ADMIN_PASSWORD

python seed_db.py
python run.py
```

Visit `http://localhost:5000` and login with the credentials you set in `.env`.

## Cloud Deployment

### Render

This project includes a `render.yaml` blueprint for one-click deployment:

1. Fork this repository
2. Create a Render account at [render.com](https://render.com)
3. Click "New Blueprint Instance"
4. Connect your GitHub repository
5. Set environment variables:
   - `ADMIN_USERNAME`: Your admin username
   - `ADMIN_PASSWORD`: Secure admin password
6. Deploy

The blueprint automatically provisions:
- Web service with Gunicorn
- Managed PostgreSQL database (free tier)
- Environment variables and secrets

**Live Demo**: `<!-- RENDER_URL_HERE -->`

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

With coverage report:

```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

Linting:

```bash
flake8 app/ config/ tests/
```

## API Documentation

### Authentication

**POST** `/auth/login`
```json
{
  "username": "admin",
  "password": "password"
}
```
Returns: `{ "token": "jwt_token" }`

### Products

**GET** `/api/products?page=1&per_page=20&q=search`

**POST** `/api/products`
```json
{
  "name": "Widget",
  "sku": "WDG-001",
  "category": "Electronics",
  "supplier_id": 1,
  "unit_price": 49.99,
  "initial_stock": 100
}
```

**PUT** `/api/products/<id>`

**DELETE** `/api/products/<id>`

### Transactions

**POST** `/api/transactions`
```json
{
  "product_id": 1,
  "quantity": 10,
  "transaction_type": "IN",
  "notes": "Restock"
}
```

### Analytics

**GET** `/api/analytics/top-selling` - Top 10 products by sales volume

**GET** `/api/analytics/low-stock` - Products with stock < 20

**GET** `/api/analytics/stock-value` - Total inventory valuation

All endpoints (except `/auth/login`) require `Authorization: Bearer <token>` header.

## Project Structure

```
.
├── app/
│   ├── __init__.py          # App factory and blueprint registration
│   ├── models.py            # SQLAlchemy models
│   ├── auth.py              # JWT utilities
│   ├── routes/              # Route blueprints
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── suppliers.py
│   │   ├── transactions.py
│   │   └── analytics.py
│   └── templates/           # HTML templates
├── config/
│   ├── settings.py          # Environment-based configuration
│   └── logging.py           # Logging setup
├── tests/
│   └── test_app.py          # Test suite
├── docs/
│   └── architecture.png     # Architecture diagram
├── Dockerfile               # Production container
├── docker-compose.yml       # Local development setup
├── render.yaml              # Render deployment blueprint
├── schema.sql               # PostgreSQL schema
├── seed_db.py               # Database seeding script
├── requirements.txt         # Python dependencies
└── run.py                   # Application entry point
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | `development` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `JWT_SECRET` | JWT signing secret | Auto-generated |
| `ADMIN_USERNAME` | Initial admin username | `admin` |
| `ADMIN_PASSWORD` | Initial admin password | Required |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
