import requests
import sys
import argparse
import json
import os

# Get Cloudflare API token from environment variable
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
if not API_TOKEN:
    print("Error: CLOUDFLARE_API_TOKEN environment variable is not set")
    sys.exit(1)

# Cloudflare API base URL
BASE_URL = "https://api.cloudflare.com/client/v4"

# Headers for the API requests
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def print_error(message, response_data=None, verbose=False):
    """Print error message, with full response data only in verbose mode."""
    if verbose and response_data:
        print(f"Error: {message}\nFull response: {json.dumps(response_data, indent=2)}")
    else:
        print(f"Error: {message}")

def get_zone_id(domain, verbose=False):
    """Get the Zone ID for the given domain."""
    response = requests.get(f"{BASE_URL}/zones", headers=HEADERS, params={"name": domain})
    response_data = response.json()

    if response.status_code == 200 and response_data["success"]:
        zones = response_data.get("result", [])
        if zones:
            return zones[0]["id"]
        else:
            print_error(f"Domain {domain} not found in Cloudflare", response_data, verbose)
    else:
        error_msg = response_data.get("errors", [{}])[0].get("message", "Unknown error")
        print_error(f"Failed to fetch zones: {error_msg}", response_data, verbose)

    return None

def create_dns_record(subdomain, domain, value, record_type="A", proxy=False, verbose=False):
    """Create a DNS record for the given subdomain.
    
    Args:
        subdomain: The subdomain to create
        domain: The parent domain
        value: The value for the record (IP for A records, target for CNAME)
        record_type: The type of DNS record (A or CNAME)
        proxy: Whether to enable Cloudflare proxy
        verbose: Whether to show detailed error messages
    """
    zone_id = get_zone_id(domain, verbose)
    if not zone_id:
        return

    # Validate record type
    record_type = record_type.upper()
    if record_type not in ["A", "CNAME"]:
        print_error(f"Unsupported record type: {record_type}")
        return

    record_data = {
        "type": record_type,
        "name": f"{subdomain}.{domain}",
        "content": value,
        "ttl": 1,
        "proxied": proxy
    }

    response = requests.post(f"{BASE_URL}/zones/{zone_id}/dns_records", headers=HEADERS, json=record_data)
    response_data = response.json()

    if response.status_code == 200 and response_data["success"]:
        print(f"{record_type} record created: {subdomain}.{domain} -> {value} (proxy: {'enabled' if proxy else 'disabled'})")
    else:
        error_msg = response_data.get("errors", [{}])[0].get("message", "Unknown error")
        print_error(f"Failed to create {record_type} record: {error_msg}", response_data, verbose)

def delete_dns_record(subdomain, domain, verbose=False):
    """Delete a DNS record for the given subdomain."""
    zone_id = get_zone_id(domain, verbose)
    if not zone_id:
        return

    response = requests.get(f"{BASE_URL}/zones/{zone_id}/dns_records", headers=HEADERS, params={"name": f"{subdomain}.{domain}"})
    response_data = response.json()

    if response.status_code == 200 and response_data["success"]:
        records = response_data.get("result", [])
        if records:
            record_id = records[0]["id"]

            delete_response = requests.delete(f"{BASE_URL}/zones/{zone_id}/dns_records/{record_id}", headers=HEADERS)
            delete_data = delete_response.json()

            if delete_response.status_code == 200 and delete_data["success"]:
                print(f"DNS record deleted: {subdomain}.{domain}")
            else:
                error_msg = delete_data.get("errors", [{}])[0].get("message", "Unknown error")
                print_error(f"Failed to delete DNS record: {error_msg}", delete_data, verbose)
        else:
            print_error(f"DNS record not found: {subdomain}.{domain}")
    else:
        error_msg = response_data.get("errors", [{}])[0].get("message", "Unknown error")
        print_error(f"Failed to fetch DNS records: {error_msg}", response_data, verbose)

def main():
    parser = argparse.ArgumentParser(description="Manage Cloudflare DNS records.")
    parser.add_argument("action", choices=["create", "delete"], help="Action to perform: create or delete.")
    parser.add_argument("-s", "--subdomain", required=True, help="Subdomain to create or delete.")
    parser.add_argument("-d", "--domain", required=True, help="Parent domain.")
    parser.add_argument("-t", "--type", default="A", choices=["A", "CNAME"], help="DNS record type (default: A).")
    parser.add_argument("-v", "--value", help="Record value (IP for A records, target for CNAME records).")
    parser.add_argument("-p", "--proxy", action="store_true", help="Enable Cloudflare proxy.")
    parser.add_argument("--verbose", action="store_true", help="Show detailed error messages and API responses.")

    args = parser.parse_args()

    if args.action == "create":
        if not args.value:
            parser.error("the following arguments are required for create: -v/--value")
        create_dns_record(args.subdomain, args.domain, args.value, args.type, args.proxy, args.verbose)
    elif args.action == "delete":
        delete_dns_record(args.subdomain, args.domain, args.verbose)

if __name__ == "__main__":
    main()
