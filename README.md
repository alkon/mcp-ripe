# RIPE Database JSON-RPC Server

A lightweight JSON-RPC server that exposes **RIPE Database queries** via a simple API. This provides real-time, filtered network information using RIPE's REST API.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup & Installation](#setup--installation)
5. [Usage](#usage)
6. [Testing](#testing)
7. [JSON-RPC Methods](#json-rpc-methods)
8. [Pros & Cons](#pros--cons)
9. [Future Enhancements](#future-enhancements)

---

## Overview

This server allows users to:

- Query RIPE DB for IP addresses, AS numbers, and domain objects.  
- Filter results dynamically based on patterns and limits.  
- Access structured JSON output via **JSON-RPC**.  
Built with **FastAPI** for high performance and easy deployment.

---

## Features

- Real-time queries to **RIPE DB** using an **API key**.  
- JSON-RPC interface for easy integration with other systems.  
- Configurable limits on results to prevent overload.  
- Easily extendable for multiple query types (IP, ASN, domain).  
- Lightweight: no massive local databases required.  

---

## Requirements

- Python 3.13+
- FastAPI >= 0.111.0
- Uvicorn[standard] >= 0.25.0
- httpx >= 0.28.1
- Pydantic >= 2.5.0
- tqdm >= 4.66.0
- pytest >= 7.4.0
- requests >= 2.31.0

See `requirements.txt` for exact versions.



---

## Setup & Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# Run the server
uvicorn src.mcp_ripe_jsonrpc:app --reload --port 8000
```
## Usage

Send JSON-RPC requests to the MCP endpoint:
```bash
curl -X POST "http://127.0.0.1:8000/mcp" \
-H "Content-Type: application/json" \
-d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "query_ripe",
    "params": {"query": "193.0.6.142", "limit": 5}
}'
```

## Testing

Run the test suite to verify the API functionality:

```bash
# Test dependencies are included in requirements.txt
# If you need to install them separately:
# pip install pytest requests

# Start the server in one terminal
uvicorn src.mcp_ripe_jsonrpc:app --reload --port 8000

# Run tests in another terminal
pytest tests/test_mcp.py -v
```

The test suite includes:
- JSON-RPC endpoint validation
- Query parameter testing
- Response format verification
- Error handling checks

For manual testing, you can use the curl commands shown in the Usage section above.

## JSON-RPC Methods
***query_ripe***

Description: Query RIPE DB for IPs, domains, or ASN objects.

Parameters:

query (string) — IPv4, IPv6, or domain.

limit (integer, optional) — Max number of results. Default: 10.

Returns: List of objects with type and attributes.

Example request:
```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "query_ripe",
    "params": {"query": "8.8.8.8", "limit": 3}
}
```

## Pros & Cons
- Pros

✅ Real-time queries; no local massive datasets required.

✅ Lightweight and cloud-friendly.

✅ JSON-RPC interface for microservice orchestration.

✅ Supports filtering and result limits, saving API usage tokens.

✅ Easy to extend to multiple network query types.

- Cons

⚠ Requires RIPE DB API key for full functionality.

⚠ Limited to RIPE DB coverage (mostly European Internet resources).

⚠ No historical full-dataset queries.

⚠ Relies on external API availability and rate limits.

## Future Enhancements

- Caching: Store recent query results to reduce API calls.

- Additional methods: Support ASN lookups, reverse DNS queries, or RIPE Atlas probes.
  - **ASN lookups**: Identify which network/organization owns IP ranges. Essential for understanding infrastructure relationships, detecting suspicious hosting patterns, and tracking threat actors who often use specific ASNs.
  - **Reverse DNS queries**: Map IPs back to hostnames to discover hidden subdomains, identify naming patterns, and uncover related infrastructure that forward DNS might miss.
  - **RIPE Atlas probes**: Provide distributed network measurements from multiple vantage points worldwide, helping detect DNS hijacking, route manipulation, and regional blocking - critical for identifying attacks that only affect specific geographic areas.

- Input validation: Ensure queries match IPv4/IPv6/domain format.

- Extended filtering: Regex or advanced pattern matching.
