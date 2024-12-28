# Cloudflare DNS Manager

A simple CLI tool to manage Cloudflare DNS records. 
Supports creating and deleting

v0.1:
- [x] Type [A] records
- [ ] Type [CNAME] records
- [ ] Proxy configurable 

## Prerequisites

- Python 3.6+
- Cloudflare API Token with DNS edit permissions

## Setup

### Option 1: Direct Use (Portable Version)
1. Download `cloudflare_portable.py`
2. Make it executable:
```bash
chmod +x cloudflare_portable.py
```

### Option 2: Virtual Environment
1. Clone the repository
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Set your Cloudflare API Token as an environment variable:
```bash
export CLOUDFLARE_API_TOKEN='your-token-here'
```

## Usage

### Create DNS Record
```bash
./cloudflare.py create -s subdomain -d example.com -i 12.34.12.34
```

### Delete DNS Record
```bash
./cloudflare.py delete -s subdomain -d example.com
```

### Options
- `-s, --subdomain`: Subdomain to create/delete
- `-d, --domain`: Main domain
- `-i, --ip`: IP address (only for create action)
- `-v, --verbose`: Show detailed API responses

## Alfred Workflow

This script is used in an Alfred workflow to quickly manage DNS records.

https://github.com/pbdco/cloudflare-alfredworkflow
