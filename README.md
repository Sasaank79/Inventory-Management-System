# Cloud-Based Inventory Management System

A production-ready, 3-tier Inventory Management System built with Python (Flask), MySQL, and Bootstrap. Designed to demonstrate strict 3NF database design, raw SQL analytics, and secure JWT authentication.

## Resume Match
This project directly implements the following:
- **Tech Stack**: Python, Flask, MySQL, JWT, SQLAlchemy, Bootstrap, Render.
- **Database**: Strict 3NF schema (`schema.sql`) with foreign keys and indexes.
- **Backend**: REST API with JWT auth (`app/auth.py`, `app/routes/`).
- **Analytics**: Raw ANSI SQL queries for top-selling/low-stock (`app/routes/analytics.py`).
- **Deployment**: Configured for Render with managed MySQL (`render.yaml`).

## Setup & Installation

### Local Development
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Seed the Database**:
   ```bash
   python seed_db.py
   ```
   *Creates a local SQLite DB `instance/inventory.db` with 500+ items.*

3. **Run the Application**:
   ```bash
   python run.py
   ```
   Visit `http://localhost:5000`.
   *   **Username**: `admin`
   *   **Password**: `admin`

### Cloud Deployment (Optional)
This project is configured for **Infrastructure as Code** deployment on Render. You can deploy it if you wish, or just run it locally.

1.  **Push to GitHub**:
    Create a new repository on GitHub and push this code:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/inventory-system.git
    git push -u origin main
    ```

2.  **Deploy on Render**:
    *   Go to [dashboard.render.com](https://dashboard.render.com).
    *   Click **New +** -> **Blueprint**.
    *   Connect your GitHub repository.
    *   Render will automatically detect `render.yaml` and create:
        *   **Web Service**: The Flask App.
        *   **Database**: A managed MySQL instance.
    *   Click **Apply**.

3.  **Seed the Live Database**:
    Once deployed, the database will be empty. To seed it:
    *   Go to the **Web Service** in Render Dashboard.
    *   Click **Shell** (SSH).
    *   Run: `python seed_db.py`

## API Endpoints
- `POST /auth/login`: Get JWT token.
- `GET /api/products`: List all products.
- `POST /api/transactions`: Record stock movement.
- `GET /api/analytics/top-selling`: Raw SQL analytics.

## Gallery
*(Add your screenshots here)*
- **Dashboard**: Overview of stock and value.
- **Products**: Searchable list with pagination.
- **Analytics**: Top selling items report.

