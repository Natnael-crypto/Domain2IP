#!/usr/bin/env python3

import dns.resolver
import argparse
from urllib.parse import urlparse
from tabulate import tabulate

def clean_domain(domain):
    """Remove schema (http://, https://) and trailing colon if present."""
    parsed_url = urlparse(domain)
    # If scheme is present, use netloc, otherwise use the domain directly
    cleaned_domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    # Strip any trailing colon
    return cleaned_domain.rstrip(':')

def get_ip(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.to_text() for ip in result]
    except Exception:
        return ["IP Not Found"]

def resolve_domains_from_file(filename):
    try:
        with open(filename, 'r') as file:
            domains = [line.strip() for line in file.readlines()]

        table = []
        for i, domain in enumerate(domains, start=1):
            if domain:  # Check if the line is not empty
                cleaned_domain = clean_domain(domain)
                ips = get_ip(cleaned_domain)
                table.append([i, cleaned_domain, ', '.join(ips)])

        # Left-align the columns
        print(tabulate(table, headers=["No.", "Domain", "IP Addresses"], tablefmt="pretty", colalign=("right", "left", "left")))

    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Resolve IP addresses for a list of domains.")
    parser.add_argument('filename', type=str, help='The file containing the list of domain names')
    
    args = parser.parse_args()
    resolve_domains_from_file(args.filename)

# Run the script
if __name__ == "__main__":
    main()
