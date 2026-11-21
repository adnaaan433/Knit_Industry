"""CLI script to generate a salted PBKDF2 password hash for .streamlit/secrets.toml."""

import getpass
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.security import hash_password


def main():
    if not sys.stdin.isatty():
        pwd = sys.stdin.readline().rstrip("\r\n")
    else:
        pwd = getpass.getpass("Enter password to hash: ")
        confirm = getpass.getpass("Confirm password: ")
        if pwd != confirm:
            print("Error: Passwords do not match.", file=sys.stderr)
            sys.exit(1)

    if not pwd:
        print("Error: Password cannot be empty.", file=sys.stderr)
        sys.exit(1)

    hashed = hash_password(pwd)
    print(f'app_password_hash = "{hashed}"')


if __name__ == "__main__":
    main()
