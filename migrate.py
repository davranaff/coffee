#!/usr/bin/env python
import os
import sys
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, 'migrations')


def parse_args():
    parser = argparse.ArgumentParser(description='Database migration management utility')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Upgrade command
    upgrade_parser = subparsers.add_parser('upgrade', help='Apply migrations')
    upgrade_parser.add_argument('revision', nargs='?', default='head',
                               help='Version to migrate to (default: head)')

    # Downgrade command
    downgrade_parser = subparsers.add_parser('downgrade', help='Rollback migrations')
    downgrade_parser.add_argument('revision', help='Version to rollback to')

    # Revision command
    revision_parser = subparsers.add_parser('revision', help='Create a new migration')
    revision_parser.add_argument('-m', '--message', required=True, help='Migration name')
    revision_parser.add_argument('--autogenerate', action='store_true', help='Autogenerate based on models')

    # History command
    subparsers.add_parser('history', help='Show migration history')

    # Current command
    subparsers.add_parser('current', help='Show current database version')

    return parser.parse_args()


def run_alembic(command_args):
    os.chdir(MIGRATIONS_DIR)

    # Add project root directory to PYTHONPATH
    env = os.environ.copy()
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = f"{BASE_DIR}:{env['PYTHONPATH']}"
    else:
        env['PYTHONPATH'] = BASE_DIR

    cmd = ['alembic'] + command_args
    subprocess.run(cmd, env=env)


def main():
    args = parse_args()

    if not args.command:
        print("Error: command not specified")
        return 1

    if args.command == 'upgrade':
        run_alembic(['upgrade', args.revision])
    elif args.command == 'downgrade':
        run_alembic(['downgrade', args.revision])
    elif args.command == 'revision':
        cmd = ['revision', '-m', args.message]
        if args.autogenerate:
            cmd.append('--autogenerate')
        run_alembic(cmd)
    elif args.command == 'history':
        run_alembic(['history'])
    elif args.command == 'current':
        run_alembic(['current'])

    return 0


if __name__ == '__main__':
    sys.exit(main())
