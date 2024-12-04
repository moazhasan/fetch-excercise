# HTTP Endpoint Monitor

A Python application that monitors HTTP endpoints and tracks their availability percentages.

## Overview

This application periodically checks configured HTTP endpoints and reports their status and availability statistics. It supports:

- Multiple HTTP endpoints with custom configurations
- Different HTTP methods (GET, POST, etc.)
- Load endpoints with arbitrary file path
- Custom headers and request bodies
- Domain-based availability tracking, logs cumulative
- Exponential backoff retry for failed URLs and prints retry seconds
- Slack notification (placeholder function)
- YAML safe loading using YAML.safe_load
- Graceful shutdown with Ctrl+C (signal handling)

I have used well-defined functions using KISS (Keep It Simple and Stupid) philosophy for code clarity

## Requirements
- Python 3.x [Downloading and installing Python](https://www.python.org/downloads/)
- Python Requests  https://requests.readthedocs.io/en/latest/
- PyYAML https://pypi.org/project/PyYAML/

Install dependencies:
```
$ pip install requests PyYAML
```
## Usage
Run with a config file or an arbitrary file path:
```
$ python monitor.py endpoints.yaml
```
## Example Output

```
$ python monitor.py endpoints.yaml

https://fetch.com/ has 100% availability percentage
https://fetch.com/careers has 100% availability percentage
sending slack notif for down URL https://fetch.com/some/post/endpoint 
https://fetch.com/some/post/endpoint has 0% availability percentage
https://fetch.com/rewards has 100% availability percentage
```

