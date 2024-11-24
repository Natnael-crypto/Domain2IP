#!/usr/bin/env python3

import dns.resolver
import argparse
from urllib.parse import urlparse
from tabulate import tabulate
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_domain(domain):
    """Remove schema (http://, https://) and trailing colon if present."""
    parsed_url = urlparse(domain)
    cleaned_domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    return cleaned_domain.rstrip(':')

def get_ip(domain):
    """Resolve IP addresses for a domain."""
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.to_text() for ip in result]
    except Exception:
        return ["IP Not Found"]

def check_http_status(domain):
    """Check HTTP and HTTPS status codes for a domain."""
    results = []
    protocols = ["http", "https"]

    for protocol in protocols:
        url = f"{protocol}://{domain}"
        try:
            response = requests.head(url, timeout=5)
            results.append(f"{protocol} {response.status_code}")
        except requests.RequestException:
            results.append(f"{protocol} Not Reachable")
    
    return results

def process_domain(domain):
    """Process a single domain to get IPs and HTTP status codes."""
    cleaned_domain = clean_domain(domain)
    ips = get_ip(cleaned_domain)
    status_codes = check_http_status(cleaned_domain)
    return [cleaned_domain, ', '.join(ips), ', '.join(status_codes)]

def resolve_domains_from_file(filename):
    """Read domains from a file and process them concurrently."""
    try:
        with open(filename, 'r') as file:
            domains = [line.strip() for line in file.readlines() if line.strip()]

        table = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_domain, domain): domain for domain in domains}
            for i, future in enumerate(as_completed(futures), start=1):
                try:
                    domain_data = future.result()
                    table.append([i, *domain_data])
                except Exception as e:
                    table.append([i, futures[future], "Error", str(e)])
        
        # Left-align columns
        print(tabulate(table, headers=["No.", "Domain", "IP Addresses", "Status Code"], tablefmt="pretty", colalign=("left", "left", "left", "left")))

    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Resolve IP addresses for a list of domains.")
    parser.add_argument('filename', type=str, help='The file containing the list of domain names')
    args = parser.parse_args()
    resolve_domains_from_file(args.filename)

# Run the script
if __name__ == "__main__":
    main()
