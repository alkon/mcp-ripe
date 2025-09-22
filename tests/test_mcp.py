import requests

def test_query_ripe():
    url = "http://127.0.0.1:8000/mcp"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "query_ripe",
        "params": {"query": "193.0.6.142", "limit": 5}
    }
    r = requests.post(url, json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "result" in data or "error" in data