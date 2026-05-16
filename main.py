import os
import httpx
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse

load_dotenv()

app = FastAPI()

GITHUB_USERNAME = "JoeFanning"
REPO_NAME = "FastApi_Data_as_a_Service"
WORKFLOW_FILE = "run_program.yml"
GITHUB_TOKEN = os.getenv("MY_SECRET_GITHUB_TOKEN")

EXCEL_FILE = "Premium_Undervalued_Deals.xlsx"


async def download_latest_excel_from_github():

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{EXCEL_FILE}"

    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                with open(EXCEL_FILE, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Skipping sync: Repository file returned status code {response.status_code}")
        except Exception as e:
            print(f"Could not sync file from GitHub: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def home_page():
    await download_latest_excel_from_github()
    table_html = "<p class='no-data'>No data loaded yet. Click 'Refresh Market Data' to pull new data.</p>"

    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            table_html = df.to_html(classes='data-table', index=False)
        except Exception as e:
            table_html = f"<p class='error'>Error reading data file: {str(e)}</p>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real Estate Deal Pipeline</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }}
            .container {{ max-width: 1100px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
            h1 {{ color: #1a202c; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
            .controls {{ margin: 20px 0; display: flex; gap: 10px; align-items: center; }}
            input[type="text"] {{ padding: 10px; width: 250px; border: 1px solid #cbd5e0; border-radius: 4px; font-size: 14px; }}
            button {{ background: #3182ce; color: white; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 4px; cursor: pointer; }}
            #status {{ font-weight: bold; margin-bottom: 20px; color: #4a5568; }}
            .table-container {{ margin-top: 25px; overflow-x: auto; }}
            .data-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
            .data-table th {{ background-color: #edf2f7; text-align: left; padding: 12px; border-bottom: 2px solid #cbd5e0; }}
            .data-table td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>New Houses Market Pipeline</h1>
            <p>Enter a target location or criteria to scan the market for new undervalued housing deals.</p>
            <div class="controls">
                <input type="text" id="filterText" placeholder="e.g., Dallas, TX or 3-bed">
                <button onclick="triggerPipeline()">Refresh Market Data</button>
            </div>
            <div id="status">Ready</div>
            <div class="table-container">
                <h2>Current Live Listings</h2>
                {table_html}
            </div>
        </div>
        <script>
            async function triggerPipeline() {{
                const filter = document.getElementById('filterText').value;
                const statusDiv = document.getElementById('status');
                statusDiv.innerText = "Spawning cloud runner via GitHub API...";
                try {{
                    const response = await fetch(`/run-pipeline?filter_text=${{encodeURIComponent(filter)}}`, {{ method: 'POST' }});
                    const data = await response.json();
                    if (response.ok) {{
                        statusDiv.innerText = "Pipeline started: " + data.message + " | Wait 1-2 mins, then refresh page.";
                    }} else {{
                        statusDiv.innerText = "Error: " + data.detail;
                    }}
                }} catch (err) {{
                    statusDiv.innerText = "Failed to connect to backend.";
                }}
            }}
        </script>
    </body>
    </html>
    """


@app.post("/run-pipeline")
async def trigger_daas_pipeline(filter_text: str = Query("")):
    url = f"https://api.github.com/repos/JoeFanning/FastApi_Data_as_a_Service/actions/workflows/run_program.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {"ref": "main", "inputs": {"custom_msg": filter_text}}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
    if response.status_code == 204:
        return {"status": "Success", "message": f"Market refresh started for: '{filter_text}'"}
    raise HTTPException(status_code=response.status_code, detail=response.text)
