# Enterprise Inventory Management System Walkthrough

I have successfully upgraded the system to a scalable, secure Enterprise architecture.

## Key Features Implemented

### 1. Enterprise Architecture
- **3NF Schema**: `Users`, `Roles`, `Suppliers`, `Products`, `Transactions` with strict constraints.
- **Connection Pooling**: Optimized database connections using `mysql.connector.pooling`.
- **Security**: Passwords hashed with `werkzeug.security`. Credentials loaded from `.env`.

### 2. Backend Logic & Auth
- **JWT Authentication**: Secure API access using JSON Web Tokens.
- **Role-Based Access Control**: `@token_required` decorator restricts actions (e.g., Admins only for adding users/products).
- **Advanced Analytics**: Complex SQL aggregates for "Monthly Turnover" and "Critical Stock".
- **Bulk Data Seeding**: `seed_data.py` uses Pandas to load 500+ products efficiently.

### 3. Professional Frontend
- **Dashboard**:
    - **Chart.js**: Visualizes "Monthly Turnover" (Line Chart) and "Top Categories" (Bar Chart).
    - **Dark Mode**: Modern UI using Bootstrap 5 Dark Mode.
- **Inventory**:
    - **DataTables.js**: Handles 500+ records with Pagination, Search, and Sorting.
    - **CSV Export**: Built-in button to export stock data.
- **Login**:
    - New `login.html` to authenticate and obtain JWT tokens.

### 4. DevOps & QA
- **Containerization**:
    - `Dockerfile`: Builds a lightweight Python image for the app.
    - `docker-compose.yml`: Orchestrates the Flask app and MySQL database services.
- **Testing**:
    - `tests/test_app.py`: Unit tests using `pytest` to verify Auth and Logic.
- **Documentation**:
    - **Swagger UI**: Interactive API documentation available at `/apidocs`.

## How to Run

### Option A: Docker (Recommended)
1.  **Run with Compose**:
    ```bash
    docker-compose up --build
    ```
2.  **Access**:
    - App: `http://localhost:5000`
    - Swagger UI: `http://localhost:5000/apidocs`

### Option B: Manual Setup
1.  **Database Setup**:
    - Create a MySQL database.
    - Run `schema.sql` to create the new tables (Warning: This replaces old tables).
    - Create an Admin user manually in DB or use a registration script (not exposed publicly for security).

2.  **Environment Variables**:
    - Create a `.env` file with `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `SECRET_KEY`.

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Seed Data**:
    ```bash
    python seed_data.py
    ```

5.  **Run Application**:
    ```bash
    python app.py
    ```

6.  **Run Tests**:
    ```bash
    pytest
    ```

7.  **Access Frontend**:
    - Open `login.html` to sign in.
    - Navigate to `dashboard.html` for analytics.
    - Navigate to `inventory.html` to manage stock.
