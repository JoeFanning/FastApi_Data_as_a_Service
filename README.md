# FastAPI Data as a Service (DaaS) — House Price Analytics

[![Python Version](https://shields.io)](https://python.org)
[![FastAPI](https://shields.io)](https://tiangolo.com)
[![Status](https://shields.io)]()

An agile, lightweight Data-as-a-Service (DaaS) application built with **FastAPI** and **Pandas**. This service acts as an intelligent intermediary layer that communicates with external corporate JSON endpoints to fetch, structure, and serve property valuation and real estate pricing data.

> ⚠️ **Note:** This project is currently under active development. Connection parameters, API schemas, and data pipelines are still being finalized.

---

## 📌 Project Architecture

├── .github/workflows/ # Automated CI/CD configurations
├── main.py # FastAPI application router & API gateway
├── process_data.py # Data processing, normalization, and business logic
├── index.html # Frontend property dashboard
└── README.md # Project documentation


## 🚀 Key Features

- **External API Integration**: Connects upstream to corporate JSON endpoints for real-time housing metrics.
- **Data Normalization**: Leverages Pandas (`process_data.py`) to parse, clean, and re-structure complex JSON payloads.
- **Asynchronous Routing**: Fast, highly parallel REST endpoints via FastAPI.
- **Property Dashboard**: An integrated `index.html` frontend UI to visually query and display property values.
- **Self-Documenting API**: Live, interactive OpenAPI/Swagger developer documentation.

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
pip install fastapi uvicorn pandas httpx
```

---

## 🏃 Running the Application

Launch your Uvicorn development server:

```bash
uvicorn main:app --reload
```

Once started, access the project services here:
- **Property Dashboard UI:** http://127.0.0.1:8000
- **Interactive Swagger Docs:** http://127.0.0:8000/docs

---

## 📡 API Endpoints (Planned & Active)


| Method | Endpoint | Description | Status |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Serves the `index.html` interface | ✅ Active |
| **GET** | `/api.rentcast.io/v1/listings/sale` | Sale listings in a geographical area, or by a specific address, from corporate JSON endpoints. | ✅ Active |
| **GET** | `/api.rentcast.io/v1/listings/sale/{id})` | Returns a single sale listing matching the specified id. | ✅ Active |
| **GET** | `/api.rentcast.io/v1/listings/rental/long-term` | Search rental listings in a geographical area, or by a specific address. | ✅ Active |
| **GET** | `/api.rentcast.io/v1/listings/rental/long-term/{id}` | Returns a single rental listing matching the specified id. | ✅ Active |
---

## 🛠️ Work in Progress / Roadmap
- [ ] Implement secure authentication handles for the upstream corporate API.
- [ ] Map complex JSON responses into clean Pandas DataFrames within `process_data.py`.
- [ ] Add query filtering parameters (e.g., zip code, price ranges) to the FastAPI endpoints.
- [ ] Write asynchronous `fetch()` methods inside `index.html` to load housing stats into UI graphs.

---

## 📄 License
This project is open-source software created by **Joe Fanning** and is licensed under the [MIT License](LICENSE).



 
