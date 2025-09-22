# RIPE Database JSON-RPC Server

A lightweight JSON-RPC server that exposes **RIPE Database queries** via a simple API. This provides real-time, filtered network information using RIPE's REST API.

---

## Table of Contents

1. [Overview](#overview)
2. [Why RIPE for Subdomain Analysis](#why-ripe-for-subdomain-analysis)
3. [Features](#features)
4. [Requirements](#requirements)
5. [Setup & Installation](#setup--installation)
6. [Usage](#usage)
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

## Why RIPE for Subdomain Analysis

RIPE's database is exceptionally valuable for subdomain analysis and security reconnaissance:

### Regional Authority
RIPE manages European, Middle Eastern, and Central Asian IP allocations - regions with high concentrations of hosting infrastructure, CDNs, and cloud services that attackers often exploit for subdomain takeover attacks.

### Detailed Network Records
Unlike simple DNS lookups, RIPE provides comprehensive network registration data including:
- **inetnum/inet6num** records showing exact IP ranges and their owners
- **route** objects revealing BGP routing relationships
- **domain** objects linking reverse DNS to organizations
- Contact information and abuse contacts for incident response

### Historical Context
RIPE maintains historical records of IP ownership changes, crucial for identifying:
- Recently transferred IP blocks (often targets for abuse)
- Infrastructure previously associated with malicious actors
- Patterns in subdomain hosting across different time periods

### Cross-Reference Capability
RIPE data allows correlating subdomains across multiple dimensions:
- Finding all IPs owned by the same organization
- Discovering shared infrastructure between seemingly unrelated domains
- Identifying shadow IT or forgotten subdomains on legacy IP ranges

### Abuse Detection
The **remarks** and **descr** fields often contain valuable metadata about network purpose, helping distinguish between legitimate corporate infrastructure and potentially compromised or suspicious hosting.

For security analysis, this means you can map an organization's entire attack surface by discovering subdomains hosted on IP ranges they own but may have forgotten about - a critical blind spot in many security programs.

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
