#!/usr/bin/env python3
"""
simple_osint.py — A simple OSINT gathering tool

Given a domain, this fetches:
  - WHOIS info (registrar, dates, nameservers)
  - DNS records (A, MX, NS, TXT)
  - Basic tech stack hints (server header, common CMS signatures)
  - Any emails visible on the homepage

Passive only — no brute forcing, no login attempts, no breach lookups.
Only run this against domains you own or are authorized to check.

Usage:
    python3 simple_osint.py example.com
"""

import re
import sys

import socket

import requests
import whois
import dns.resolver

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# label -> regex pattern to look for in page HTML / headers
TECH_HINTS = {
    "WordPress": r"wp-content|wp-includes",
    "Shopify": r"cdn\.shopify\.com",
    "React": r"react-dom|data-reactroot",
    "jQuery": r"jquery(\.min)?\.js",
    "Bootstrap": r"bootstrap(\.min)?\.css",
}


def get_whois(domain):
    print("\n[+] WHOIS Info")
    socket.setdefaulttimeout(8)
    try:
        w = whois.whois(domain)
        print(f"    Registrar:   {w.registrar}")
        print(f"    Created:     {w.creation_date}")
        print(f"    Expires:     {w.expiration_date}")
        print(f"    Name Servers:{w.name_servers}")
    except Exception as e:
        print(f"    [!] WHOIS lookup failed: {e}")


def get_dns(domain):
    print("\n[+] DNS Records")
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5
    for record_type in ["A", "MX", "NS", "TXT"]:
        try:
            answers = resolver.resolve(domain, record_type)
            for a in answers:
                print(f"    {record_type}: {a}")
        except Exception:
            print(f"    {record_type}: (none found)")


def get_tech_and_emails(domain):
    print("\n[+] Tech Stack & Emails (from homepage)")
    url = f"https://{domain}"
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "simple-osint/1.0"})
    except requests.RequestException as e:
        print(f"    [!] Could not fetch {url}: {e}")
        return

    # Server header
    server = r.headers.get("Server")
    if server:
        print(f"    Server header: {server}")

    # Tech signatures in page HTML
    found_tech = [label for label, pattern in TECH_HINTS.items() if re.search(pattern, r.text, re.IGNORECASE)]
    if found_tech:
        print(f"    Detected tech: {', '.join(found_tech)}")
    else:
        print("    Detected tech: none matched")

    # Emails on the page
    emails = set(re.findall(EMAIL_PATTERN, r.text))
    if emails:
        print(f"    Emails found: {', '.join(sorted(emails))}")
    else:
        print("    Emails found: none")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 simple_osint.py <domain>")
        sys.exit(1)

    domain = sys.argv[1].replace("https://", "").replace("http://", "").strip("/")

    print(f"[*] Gathering OSINT for: {domain}")
    get_whois(domain)
    get_dns(domain)
    get_tech_and_emails(domain)
    print("\n[*] Done.")


if __name__ == "__main__":
    main()