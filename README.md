# FastAPI Data as a Service (DaaS)

[![Python Version](https://shields.io)](https://python.org)
[![FastAPI](https://shields.io)](https://tiangolo.com)
[![Status](https://shields.io)]()

An efficient, lightweight Data-as-a-Service (DaaS) application powered by **FastAPI** and **Pandas**. This project parses analytical data inputs (such as Excel financial worksheets) and exposes them through standard REST API endpoints, paired with an interactive frontend viewer.

> ⚠️ **Note:** This project is currently under active development. Some endpoints and processing pipelines are still being implemented.

---

## 📌 Project Architecture

The application relies on a data pipeline that processes raw data spreadsheets and serves them programmatically:

## 🚀 Key Features

- **Automated Data Processing**: Dynamically extracts data matrices using `process_data.py`.
- **High-Performance Routing**: Async endpoints native to FastAPI.
- **Self-Documenting API**: Instant access to interactive OpenAPI/Swagger web documentation.
- **Built-in Dashboard**: Clean `index.html` frontend mapping directly to active endpoints.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com
cd FastApi_Data_as_a_Service
```

### 2. Set Up Virtual Environment
* **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn pandas openpyxl
```

---

## 🏃 Running the Application

Launch the local development environment using Uvicorn:

```bash
uvicorn main:app --reload
```

Once initialized, navigate to the following local URLs:
- **Interactive UI (Frontend):** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Docs (Swagger UI):** [http://127.0.0](http://127.0.0)

---

## 📡 API Endpoints (Planned & Active)


| Method | Endpoint | Description | Status |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Serves the `index.html` user dashboard | ✅ Active |
| **GET** | `/api/v1/deals` | Fetches parsed JSON payload from `Premium_Undervalued_Deals.xlsx` | 🛠️ In Progress |
| **GET** | `/api/v1/deals/{id}` | Filters and retrieves data for a single record id | ⏳ Planned |

*(Modify these endpoints based on your actual routes in `main.py`)*

---

## 🛠️ Work in Progress / Roadmap
- [ ] Complete dataset filtering methods inside `process_data.py`.
- [ ] Bind endpoints inside `main.py` to support dynamic query parameters.
- [ ] Connect `index.html` via JavaScript `fetch()` calls to display deals dynamically.
- [ ] Implement robust error handling for missing spreadsheet records.

---

## 📄 License
