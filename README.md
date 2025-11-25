# Cloud-Based Inventory Management System

A production-ready, 3-tier Inventory Management System built with Python (Flask), MySQL, and Bootstrap. Designed to demonstrate strict 3NF database design, raw SQL analytics, and secure JWT authentication.

## Tech Stack
- **Backend**: Python 3, Flask, SQLAlchemy
- **Database**: MySQL (Strict 3NF Schema)
- **Auth**: JWT (JSON Web Tokens)
- **Frontend**: HTML5, Bootstrap 5, Vanilla JS
- **Deployment**: Render / Railway

## Features
- **3NF Normalized Schema**: Optimized for data integrity with foreign keys and indexes.
- **Bulk Seeding**: Script to generate 500+ realistic products and transactions.
- **Inventory Tracking**: Real-time stock calculation based on IN/OUT transactions.
- **Analytics Dashboard**: Top-selling items, low stock alerts, and total inventory value using **Raw ANSI SQL**.
- **Secure API**: All write endpoints protected via JWT.

## Setup & Installation

### Local Development
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd inventory-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**:
   - Create a MySQL database (or use SQLite default for testing).
   - Copy `.env.example` to `.env` (if applicable) or set env vars:
     ```bash
     export DATABASE_URL="mysql+pymysql://user:pass@localhost/db_name"
     export JWT_SECRET="your-secret"
     ```

5. **Seed the Database**:
   ```bash
   python seed_db.py
   ```
   *This will create tables and insert 500+ products and an admin user (admin/admin).*

6. **Run the Application**:
   ```bash
   python run.py
   ```
   Visit `http://localhost:5000`.

### Deployment (Render)
1. Connect your GitHub repo to Render.
2. Create a **Web Service** using the `render.yaml` blueprint or manually:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
3. Add a **MySQL Database** service and link it via `DATABASE_URL`.
4. **Seeding on Cloud**:
   - Use the Render Shell (or SSH) to run: `python seed_db.py`

## API Endpoints
- `POST /auth/login`: Get JWT token.
- `GET /api/products`: List all products.
- `POST /api/transactions`: Record stock movement.
- `GET /api/analytics/top-selling`: Raw SQL analytics.

## Database Schema
See `schema.sql` for the full DDL.
- `users`: Auth credentials.
- `suppliers`: Vendor info.
- `products`: Catalog items (linked to suppliers).
- `inventory_transactions`: Ledger of all stock changes (linked to products).
