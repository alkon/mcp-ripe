# src/mcp_ripe_jsonrpc.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Use your RIPE DB API key in Authorization header
RIPE_DB_AUTH = "Basic RkZRWlFVQ1lTMURLUlJPTUxMTldRSlVFOmNBbXprZU0zNzNCUWZyTVRXcVpzdTNIZQ=="
RIPE_DB_URL = "https://rest.db.ripe.net/search.json"


def query_ripe_db(query: str, limit: int = 10):
    """
    Query the RIPE Database and return filtered results.
    """
    headers = {
        "Authorization": RIPE_DB_AUTH,
        "Accept": "application/json"
    }
    params = {"query-string": query, "flags": "no-filtering"}

    try:
        resp = requests.get(RIPE_DB_URL, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        results = []
        # Extract relevant objects (e.g., inetnum, inet6num, domain)
        objects = data.get("objects", {}).get("object", [])
        for obj in objects:
            # Each object may have 'primary-key' and 'attributes'
            obj_type = obj.get("type", "")
            attrs = {attr["name"]: attr["value"] for attr in obj.get("attributes", {}).get("attribute", [])}
            if "inetnum" in attrs or "inet6num" in attrs or "domain" in attrs:
                results.append({
                    "type": obj_type,
                    "attributes": attrs
                })
            if len(results) >= limit:
                break

        return results

    except Exception as e:
        raise RuntimeError(f"RIPE DB query error: {e}")


@app.post("/mcp")
async def mcp_handler(request: Request):
    """
    MCP JSON-RPC entrypoint for RIPE DB queries.

    Example request:
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "query_ripe",
        "params": {"query": "193.0.6.142", "limit": 5}
    }
    """
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    req_id = body.get("id")

    try:
        if method == "query_ripe":
            query = params.get("query", "")
            limit = params.get("limit", 10)

            results = query_ripe_db(query, limit)
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": results
            })

        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Method not found"}
            })

    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32000, "message": str(e)}
        })
