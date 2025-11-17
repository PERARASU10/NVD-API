# 📂 NVD CVE Data Explorer (FastAPI + MongoDB + Frontend)

This project provides a local, robust, and user-friendly interface for querying and analyzing National Vulnerability Database (NVD) data stored in a local MongoDB instance.

---

## ✨ Features

* **Paginated Listing:** View a large number of CVE records efficiently with customizable page sizes (5, 10, 25, etc.).
* **Detailed View:** Click any CVE ID to navigate to a dedicated detail page. This page clearly displays **key vulnerability metrics** (CVSS Score, Severity, Vector Breakdown, Vulnerable Products) and includes a section for the **full raw JSON** for advanced analysis.
* **Direct Search:** Search for specific CVE IDs (e.g., `CVE-2024-8001`) via a dedicated lookup bar.
* **Robust Backend:** **FastAPI** manages API routing, handles database connection state checks, and includes necessary **CORS middleware** for seamless local development.
* **Front-end:** Pure **HTML/JavaScript** with Tailwind CSS for rapid styling and interactivity.

---

## 🚀 Getting Started

Follow these steps to set up and run the NVD CVE Data Explorer locally.

### Prerequisites

You must have the following software installed:

1.  **Python 3.8+**
2.  **MongoDB Server:** Must be running locally, typically accessible at `mongodb://localhost:27017/`.
3.  **Data Set:** Your MongoDB instance needs a database named **`nvd_cve_data`** with a collection named **`cves`** populated with NVD JSON data.

### 1. Backend Setup

The backend requires Python and specific packages for web serving and MongoDB interaction.

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 2. Install required packages
pip install fastapi uvicorn pymongo python-multipart pydantic
```

### 2. Run the FastAPI Backend

Run the server using Uvicorn with the --reload flag for development convenience.
```bash
uvicorn main:app --reload
```

The server should start running at http://127.0.0.1:8000. The console will display a connection status for MongoDB. If the connection fails, the API will immediately return a 503 Service Unavailable error until MongoDB is started.


### 3. Run the Frontend

The frontend uses standard HTML and JavaScript and does not require a separate build step.

* Ensure the FastAPI backend is running (Step 2).

* Open index.html in your web browser (by double-clicking the file).

* Click the "Load First Page" button to begin retrieving data from the backend.


### 🌐 API Endpoints (Backend Reference)

The FastAPI application exposes the following endpoints:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/count` | Returns the total document count in the cves collection. |
| GET | `/cves` | Retrieves a list of CVEs with pagination. Query Params: skip (int), limit (int). |
| GET | `/cve/{cve_id}` | Retrieves the full JSON document for a specific CVE ID. |

### Output 

![Uploading Screenshot (33).png…]()

![Uploading Screenshot (34).png…]()

![Uploading Screenshot (35).png…]()

![Uploading Screenshot (36).png…]()

![Uploading Screenshot (37).png…]()




### 🗂️ Project Files

The project is structured with minimal files for clarity and simplicity.

| File | Role | Details |
| :--- | :--- | :--- |
| `main.py` | **Backend API** | Defines connection logic and three FastAPI endpoints (`/count`, `/cves`, `/cve/{cve_id}`). |
| `index.html` | **Main Frontend** | Displays the paginated table and search bar. Contains the logic for fetching lists and redirecting to the detail page. |
| `cve_detail.html` | **Detail Page** | Fetches the full JSON for a specific CVE ID and parses it to display key vulnerability data (CVSS, Configurations) in a readable format, alongside the raw data. |
