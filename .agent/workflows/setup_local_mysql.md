---
description: How to set up a local MySQL server using Docker
---

# Setting up Local MySQL

You have a `docker-compose.yml` file ready to go. This is the easiest way to run MySQL.

1.  **Start MySQL Container**:
    Run this command in your terminal:
    ```bash
    docker-compose up -d db
    ```
    This will:
    - Start a MySQL 8.0 server.
    - Expose it on port `3306`.
    - Set user: `root`, password: `root`, database: `inventory_db`.
    - Automatically run `schema.sql` to create tables.

2.  **Verify Connection**:
    You can check if it's running:
    ```bash
    docker ps
    ```

3.  **Connect App to MySQL**:
    Update your `.env` file to use the MySQL connection string instead of SQLite:
    ```properties
    DATABASE_URL=mysql+pymysql://root:root@localhost/inventory_db
    ```

4.  **Seed Data**:
    Since this is a fresh database, run the seed script again:
    ```bash
    python seed_db.py
    ```

5.  **Stop Server**:
    When done, you can stop it with:
    ```bash
    docker-compose down
    ```
