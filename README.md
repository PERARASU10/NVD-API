###📂 NVD CVE Data Explorer (FastAPI + MongoDB + Frontend)

This project provides a local, robust, and user-friendly interface for querying and analyzing National Vulnerability Database (NVD) data stored in a local MongoDB instance.

##✨ Features

Paginated Listing: View thousands of CVE records efficiently with customizable page sizes (5, 10, 25, etc.).

Detailed View: Click any CVE ID to navigate to a dedicated detail page showing CVSS scores, severity levels, vector breakdowns, and vulnerable product configurations, plus full raw JSON.

Direct Search: Quickly search for specific CVE IDs (e.g., CVE-2024-8001).

Robust Backend: Built with FastAPI, includes database connection state checks, and supports local development with CORS middleware.

Frontend: Pure HTML + JavaScript with Tailwind CSS, requiring no build tools.

##🚀 Getting Started

Follow these steps to set up and run the NVD CVE Data Explorer locally.

##🧩 Prerequisites

Ensure you have:

Python 3.8+

MongoDB Server running locally (mongodb://localhost:27017/)

NVD JSON dataset imported into a MongoDB database:

Database: nvd_cve_data

Collection: cves

##⚙️ 1. Backend Setup

Create a virtual environment and install dependencies.

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install backend requirements
pip install fastapi uvicorn pymongo python-multipart pydantic

▶️ 2. Run the FastAPI Backend

Start the backend server:

uvicorn main:app --reload


The API will be available at:

👉 http://127.0.0.1:8000

If MongoDB is not running, API requests will return:

503 Service Unavailable
until MongoDB is active.

💻 3. Run the Frontend

No build step required — everything runs directly in the browser.

Start the FastAPI backend.

Open index.html in your web browser.

Click "Load First Page" to pull data from the backend.

🌐 API Endpoints
Method	Endpoint	Description
GET	/count	Returns total documents in the cves collection.
GET	/cves	Returns paginated CVEs. Query params: skip, limit.
GET	/cve/{cve_id}	Returns full JSON for a specific CVE ID.
📁 Project Structure
File	Role	Description
main.py	Backend API	Defines MongoDB connection + endpoints (/count, /cves, /cve/{cve_id}).
index.html	Main Frontend	Pagination, table display, search bar, data fetching.
cve_detail.html	Detail Page	Displays CVSS data, configurations, and raw JSON for a CVE.
📦 Example Use Case

Search for a CVE (e.g., CVE-2024-8001)

Click the result to open the detail page

Review:

CVSS Score

Severity

Attack Vector

Impact Metrics

Affected Products

Complete Raw NVD JSON

📌 Notes

This project is ideal for local research, offline NVD analysis, and security auditing workflows.

No external API calls — fully local and fast.

🤝 Contributions

Contributions are welcome!
Feel free to open issues or submit pull requests.

📜 License

MIT License — free for personal and commercial use.
