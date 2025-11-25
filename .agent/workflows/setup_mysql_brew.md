---
description: How to set up a local MySQL server using Homebrew (macOS)
---

# Setting up Local MySQL with Homebrew

Since you have Homebrew installed, this is the easiest way to get MySQL running natively on your Mac.

1.  **Install MySQL**:
    Run this command in your terminal:
    ```bash
    brew install mysql
    ```

2.  **Start the Service**:
    Start MySQL and have it run in the background:
    ```bash
    brew services start mysql
    ```

3.  **Secure Installation (Optional but Recommended)**:
    Run the security script to set a root password:
    ```bash
    mysql_secure_installation
    ```
    *Follow the prompts. You can set the password to `root` for local development simplicity if you like.*

4.  **Create the Database**:
    Log in to MySQL:
    ```bash
    mysql -u root -p
    ```
    Then run:
    ```sql
    CREATE DATABASE inventory_db;
    EXIT;
    ```

5.  **Configure App**:
    Update your `.env` file to match your local MySQL credentials:
    ```properties
    DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/inventory_db
    ```

6.  **Seed Data**:
    Now populate the new database:
    ```bash
    python seed_db.py
    ```
