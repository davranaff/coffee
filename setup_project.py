#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Coffee Shop API project.
Used to create databases, install dependencies etc.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def create_databases():
    """Create main and test databases"""
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Get database name from environment variables or use default value
        db_name = os.getenv("DB_NAME", "coffee")
        test_db_name = f"test_{db_name}"

        print(f"📦 Creating main database '{db_name}'...")
        subprocess.run(["createdb", db_name], check=False)

        print(f"📦 Creating test database '{test_db_name}'...")
        subprocess.run(["createdb", test_db_name], check=False)

        print("✅ Databases successfully created")
    except Exception as e:
        print(f"❌ Error creating databases: {e}")
        sys.exit(1)


def install_dependencies():
    """Install dependencies from requirements.txt"""
    try:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies successfully installed")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)


def create_env_file():
    """Create .env file from template"""
    try:
        if not os.path.exists(".env"):
            print("📄 Creating .env file from template...")

            # Check if .env.example exists
            if not os.path.exists(".env.example"):
                with open(".env.example", "w") as f:
                    f.write("""# Database settings
                            DB_DRIVER=postgresql
                            DB_HOST=localhost
                            DB_PORT=5432
                            DB_USER=postgres
                            DB_PASSWORD=postgres
                            DB_NAME=coffee

                            # JWT settings
                            SECRET_KEY=your_secret_key_here
                            ALGORITHM=HS256
                            ACCESS_TOKEN_EXPIRE_MINUTES=30
                            REFRESH_TOKEN_EXPIRE_DAYS=7

                            # Application settings
                            DEBUG=True
                        """)

            # Copy .env.example to .env
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())

            print("✅ .env file successfully created")
        else:
            print("🔄 .env file already exists")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Coffee Shop API Project Setup")
    parser.add_argument("--db", action="store_true", help="Create databases")
    parser.add_argument("--deps", action="store_true", help="Install dependencies")
    parser.add_argument("--env", action="store_true", help="Create .env file")
    parser.add_argument("--all", action="store_true", help="Perform all setup steps")

    args = parser.parse_args()

    # If no arguments are specified, display help
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)

    # Perform setup steps based on arguments
    if args.all or args.env:
        create_env_file()

    if args.all or args.deps:
        install_dependencies()

    if args.all or args.db:
        create_databases()

    print("✨ Project setup completed")


if __name__ == "__main__":
    main()
