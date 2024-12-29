# Cloudflare DNS Manager

A simple CLI tool to manage Cloudflare DNS records through command line interface.

## Features

Current (v0.1):
- [x] Create and delete Type A records
- [x] Command line interface
- [x] CNAME record support
- [x] Configurable proxy settings
- [x] Alfred Workflow integration
- [x] Single-file bundled executable

Planned:
- [ ] List existing DNS records
- [ ] Update existing records

## Prerequisites

For using the bundled executable:
- No Python installation required
- Cloudflare API Token with DNS edit permissions

For development:
- Python 3.6+
- pip (Python package installer)

## Installation

### Option 1: Bundled Executable (Recommended)
1. Download the latest bundled executable from the [Releases](https://github.com/yourusername/cloudflare-python/releases) page
2. Make it executable:
```bash
chmod +x dist/cloudflare
```

### Option 2: Virtual Environment (Development)
1. Clone the repository:
```bash
git clone https://github.com/yourusername/cloudflare-python.git
cd cloudflare-python
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

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
./dist/cloudflare create -s subdomain -d example.com -i 12.34.12.34
```

### Delete DNS Record
Remove a DNS record for a subdomain:
```bash
./dist/cloudflare delete -s subdomain -d example.com
```

### Command Line Options
- `-s, --subdomain`: Subdomain to create/delete (required)
- `-d, --domain`: Main domain (required)
- `-i, --ip`: IP address (required for create action)
- `-v, --verbose`: Show detailed API responses
- `-h, --help`: Show help message

## Alfred Workflow Integration

This script powers a custom Alfred workflow for quick DNS management. The workflow uses the bundled executable version for simplified deployment.

[Cloudflare Alfred Workflow Repository](https://github.com/pbdco/cloudflare-alfredworkflow)

## Building from Source

The bundled executable is automatically created by GitHub Actions on each release. If you want to build it manually:

```bash
pip install pyinstaller
pyinstaller --onefile cloudflare.py
```

The executable will be created in the `dist` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
