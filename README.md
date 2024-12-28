# Cloudflare DNS Manager

A simple CLI tool to manage Cloudflare DNS records. Supports creating and deleting A records.

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
./cloudflare.py create -s subdomain -d example.com -i 192.168.1.1
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

This script can be used as an Alfred workflow to quickly manage DNS records.

### Workflow Setup
1. Download the `.alfredworkflow` file from Releases
2. Double click to import into Alfred
3. Set your `CLOUDFLARE_API_TOKEN` in the workflow environment variables

### Workflow Usage
```bash
dns create mysubdomain example.com 192.168.1.1
dns delete mysubdomain example.com
```

## Development

### Project Structure
```
.
├── cloudflare.py          # Main script (with requests)
├── portable/
│   └── cloudflare_portable.py  # Standalone version
├── requirements.txt
└── workflow/              # Alfred workflow files
    ├── info.plist
    └── run.sh
```

### Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details