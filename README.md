# Domain-to-IP Resolver

A Python script that resolves the IP addresses of a list of domain names provided in a file. It handles domains that may include schemas such as `http://` or `https://` and removes any trailing colons if present.

## Features

- Resolves the IP addresses of domains provided in a file.
- Handles domains with schemas (e.g., `https://example.com`) and removes any unnecessary parts such as `http://`, `https://`, or trailing colons (`:`).
- Provides clear error messages when a domain cannot be resolved or if the file is not found.

## Prerequisites

Before you begin, ensure you have Python installed on your system. This script requires the following Python package:

- `dnspython` for resolving DNS queries.

To install `dnspython`, run:

```bash
pip install dnspython
```

## Usage
1. Clone the repository:
  ```bash
  git clone https://github.com/Natnael-crypto/Domain2IP.git
  cd Domain2IP
  ```
2. Prepare a file with the list of domain names:

  Create a file (e.g., domains.txt) and add domain names, one per line. The domains can include schemas such as http:// or https:// and may contain a trailing colon (:).
  Example domains.txt:
  ```txt
  https://example.com
  http://google.com
  facebook.com:443
  ```
3. Run the script:

  You can run the script by passing the filename as an argument.
  ```bash
  python Domain2Ip.py domains.txt
  ```
  Output:
  The script will print the resolved IP addresses for each domain. Example output:
  ```
+---------+-----------------+----------------------------+
|  Number | Domain          | [IP Addresses]             |
+---------+-----------------+----------------------------+
|       1 | example.com      | ['93.184.216.34']         |
|       2 | google.com       | ['172.217.164.110']       |
|       3 | facebook.com     | ['157.240.23.35']         |
+---------+-----------------+----------------------------+

  ```
## Command-Line Arguments
  filename: The file containing the domain names to resolve. Each domain should be on a new line.
  Example Command
  ```bash
  python Domain2Ip.py domains.txt
  ```
