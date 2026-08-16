# simple_osint.py

A simple OSINT gathering tool. Given a domain, it fetches WHOIS info,
DNS records (A, MX, NS, TXT), basic tech stack hints, and any emails
visible on the homepage.

Passive only — no brute forcing, no login attempts, no breach lookups.
Only run this against domains you own or are authorized to check.

## Setup

```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install requests python-whois dnspython
```

## Usage

```bash
python3 simple_osint.py example.com
```

## Deactivating

When you're done:

```bash
deactivate
```

## Notes

- You'll need to run `source venv/bin/activate` again each time you open
  a new terminal, before running the script.
- If `pip install` fails on macOS with an "externally managed environment"
  error, make sure the venv is actually activated first (check your prompt
  shows `(venv)`).
