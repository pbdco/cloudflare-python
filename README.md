# Cloudflare DNS Manager

A simple CLI tool to manage Cloudflare DNS records through command line interface.

## Features

Current (v0.1):
- [x] Create and delete Type A records
- [x] Command line interface
- [x] CNAME record support
- [x] Configurable proxy settings
- [x] Alfred Workflow integration

## Prerequisites

- Python 3.9+
- Cloudflare API Token with DNS edit permissions
- pip (Python package installer)

## Installation

### Option 1: Direct Use
1. Clone the repository:
```bash
git clone https://github.com/pbdco/cloudflare-python.git
cd cloudflare-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Build Executable (Testing)
1. Clone the repository:
```bash
git clone https://github.com/pbdco/cloudflare-python.git
cd cloudflare-python
```

2. Install PyInstaller and dependencies:
```bash
pip install pyinstaller
pip install -r requirements.txt
```

3. Build the executable:
```bash
pyinstaller --onefile cloudflare.py
```

4. The executable will be created in the `dist` directory. Test it:
```bash
./dist/cloudflare create -s subdomain -d example.com -v 12.34.12.34
```

### Option 3: Alfred Workflow
Download the latest Alfred workflow from:
- [Cloudflare Alfred Workflow Repository](https://github.com/pbdco/cloudflare-alfredworkflow)

## Configuration

Set your Cloudflare API Token as an environment variable:
```bash
export CLOUDFLARE_API_TOKEN='your-token-here'
```

Or on Windows:
```cmd
set CLOUDFLARE_API_TOKEN=your-token-here
```

## Usage

### Create DNS Record
Create an A record for a subdomain:
```bash
python cloudflare.py create -s subdomain -d example.com -v 12.34.12.34
```

Create a CNAME record:
```bash
python cloudflare.py create -s subdomain -d example.com -t CNAME -v target.example.com
```

Create a proxied record (orange cloud in Cloudflare):
```bash
python cloudflare.py create -s subdomain -d example.com -v 12.34.12.34 -p
```

### Delete DNS Record
Remove a DNS record for a subdomain:
```bash
python cloudflare.py delete -s subdomain -d example.com
```

### Command Line Options
- `-s, --subdomain`: Subdomain to create/delete (required)
- `-d, --domain`: Main domain (required)
- `-t, --type`: Record type (A or CNAME, defaults to A)
- `-v, --value`: IP address or CNAME target (required for create)
- `-p, --proxy`: Enable Cloudflare proxy (optional)
- `--verbose`: Show detailed API responses

## Alfred Workflow Integration

This script powers a custom Alfred workflow for quick DNS management. For more information and installation instructions, visit:

[Cloudflare Alfred Workflow Repository](https://github.com/pbdco/cloudflare-alfredworkflow)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
