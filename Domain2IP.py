#!/usr/bin/env python3

import dns.resolver
import argparse
from urllib.parse import urlparse
from tabulate import tabulate
import requests

def clean_domain(domain):
    """Remove schema (http://, https://) and trailing colon if present."""
    parsed_url = urlparse(domain)
    cleaned_domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    return cleaned_domain.rstrip(':')

def get_ip(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.to_text() for ip in result]
    except Exception:
        return ["IP Not Found"]

def check_http_status(domain):
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

def enumerate_technology(domain):
    url = f"https://{domain}"  # Use https by default for scanning
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        # Simple CMS detection using headers
        cms = "Not found"
        if "x-powered-by" in headers:
            cms = headers["x-powered-by"]
        elif "server" in headers:
            if "WordPress" in headers["server"]:
                cms = "WordPress"
            elif "Wix" in headers["server"]:
                cms = "Wix"
            elif "Squarespace" in headers["server"]:
                cms = "Squarespace"

        # Detect programming language if possible
        tech = headers.get("x-powered-by", "Not found")
        return cms, tech

    except requests.RequestException:
        return "Not found", "Not found"

def resolve_domains_from_file(filename):
    try:
        with open(filename, 'r') as file:
            domains = [line.strip() for line in file.readlines()]

        table = []
        for i, domain in enumerate(domains, start=1):
            if domain:
                cleaned_domain = clean_domain(domain)
                ips = get_ip(cleaned_domain)
                status_codes = check_http_status(cleaned_domain)
                cms, tech = enumerate_technology(cleaned_domain)
                table.append([
                    i, 
                    cleaned_domain, 
                    ', '.join(ips), 
                    ', '.join(status_codes), 
                    cms, 
                    tech
                ])

        # Left-align columns
        print(tabulate(table, headers=["No.", "Domain", "IP Addresses", "Status Code", "CMS", "Programming Language"], tablefmt="pretty", colalign=("left", "left", "left", "left", "left", "left")))

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
