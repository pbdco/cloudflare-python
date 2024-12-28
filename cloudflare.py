import requests
import sys
import argparse
import json
import os

# Get Cloudflare API token from environment variable
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
print(f"Debug - CLOUDFLARE_API_TOKEN: {API_TOKEN}", file=sys.stderr)
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

def create_dns_record(subdomain, domain, ip="127.0.0.1", verbose=False):
    """Create a DNS A record for the given subdomain."""
    zone_id = get_zone_id(domain, verbose)
    if not zone_id:
        return

    record_data = {
        "type": "A",
        "name": f"{subdomain}.{domain}",
        "content": ip,
        "ttl": 1,
        "proxied": False
    }

    response = requests.post(f"{BASE_URL}/zones/{zone_id}/dns_records", headers=HEADERS, json=record_data)
    response_data = response.json()

    if response.status_code == 200 and response_data["success"]:
        print(f"DNS record created: {subdomain}.{domain} -> {ip}")
    else:
        error_msg = response_data.get("errors", [{}])[0].get("message", "Unknown error")
        print_error(f"Failed to create DNS record: {error_msg}", response_data, verbose)

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
    parser.add_argument("-i", "--ip", default="127.0.0.1", help="IP address for the A record (only for create action).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed error messages and API responses.")

    args = parser.parse_args()

    if args.action == "create":
        create_dns_record(args.subdomain, args.domain, args.ip, args.verbose)
    elif args.action == "delete":
        delete_dns_record(args.subdomain, args.domain, args.verbose)

if __name__ == "__main__":
    main()
