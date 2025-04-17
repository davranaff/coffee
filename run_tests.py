#!/usr/bin/env python
import os
import sys
import argparse
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "test_coffee")


def parse_args():
    parser = argparse.ArgumentParser(description='Test runner utility')
    parser.add_argument('path', nargs='?', default='tests', 
                       help='Path to test file or directory (default: tests)')
    parser.add_argument('--cov', action='store_true', 
                       help='Enable coverage report')
    parser.add_argument('--db-init', action='store_true',
                       help='Initialize test database')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                       help='Verbosity level (can be used multiple times)')
    return parser.parse_args()


def init_test_db():
    """Initialize test database"""
    print(f"Creating test database '{TEST_DB_NAME}'...")

    try:
        # Drop database if exists
        subprocess.run(['dropdb', '--if-exists', TEST_DB_NAME], check=False)

        # Create new database
        subprocess.run(['createdb', TEST_DB_NAME], check=True)

        # Apply migrations
        os.environ['DATABASE_URL'] = f"postgresql://postgres:postgres@localhost/{TEST_DB_NAME}"
        subprocess.run(['python', 'migrate.py', 'upgrade', 'head'], check=True)

        print("Test database initialization completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing test database: {e}")
        sys.exit(1)


def run_tests(path, cov=False, verbose=0):
    """Run pytest with specified options"""
    cmd = ['pytest', path]

    # Add verbosity level
    if verbose > 0:
        cmd.append('-' + 'v' * verbose)

    # Add coverage if requested
    if cov:
        cmd.extend(['--cov=app', '--cov-report=term-missing'])

    # Run tests
    print(f"Running tests: {' '.join(cmd)}")
    start_time = time.time()
    result = subprocess.run(cmd)
    elapsed_time = time.time() - start_time

    # Report
    if result.returncode == 0:
        print(f"✅ All tests passed! ({elapsed_time:.2f}s)")
    else:
        print(f"❌ Some tests failed. ({elapsed_time:.2f}s)")

    return result.returncode


def main():
    args = parse_args()

    # Initialize test database if requested
    if args.db_init:
        init_test_db()
        if len(sys.argv) == 2 and args.db_init:
            return 0

    # Run tests
    return run_tests(args.path, args.cov, args.verbose)


if __name__ == '__main__':
    sys.exit(main())
