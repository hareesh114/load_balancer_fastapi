from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
import requests

app = FastAPI()

servers = [
    "http://127.0.0.1:8001/",
    "http://127.0.0.1:8002/",
    "http://127.0.0.1:8003/"
]

current = 0  # round robin pointer


@app.api_route('/{endpoint:path}', methods=['GET', 'POST'])
async def load_balance(endpoint:str, request:Request):
    global current
    # Select server
    server = servers[current]
    # Move pointer
    current = (current + 1) % len(servers)

    url = f"{server}/{endpoint}"
    print(url)
    print(f"Load Balancer forwarded to {server}")

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() != "host"
    }

    # print("Incoming headers:", request.headers)
    # print("Forwarded headers:", headers)

    try:
        if request.method == "POST":
            body = await request.json()
            response = requests.post(url, json=body, headers=headers)
            return JSONResponse({
                "forwarded_to": server,
                "backend_response": response.json()
            })
        else:
            response = requests.get(url, headers=headers, allow_redirects=False)
            
            if response.status_code in [301, 302]:            
                return RedirectResponse(response.headers["Location"])

            return JSONResponse(
                content={"response": response.text},
                status_code=response.status_code
            )
            
    except requests.exceptions.RequestException:
        return JSONResponse({"error": "Backend server unavailable"}, status_code=500 )

    

if __name__ == '__main__':
    app.run(port=8000)