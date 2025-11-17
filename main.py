import time
from typing import Any, Dict, List
from fastapi import FastAPI, status, HTTPException
# 🚨 REQUIRED IMPORT FOR CORS FIX 🚨
from fastapi.middleware.cors import CORSMiddleware 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure, OperationFailure

# --- Configuration (MUST match your existing database name) ---
MONGO_DB_NAME = "nvd_cve_data"

# --- Database Connection Setup ---
client: MongoClient | None = None
collection = None

try:
    # Attempt to connect to MongoDB with a short timeout
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.admin.command('ping') 
    collection = client[MONGO_DB_NAME]["cves"]
    print("MongoDB connection established successfully.")
except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    client = None
    collection = None 
    print(f"FATAL: Could not connect to MongoDB. Please ensure your mongod service is running. Error: {e}")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="NVD CVE Retrieval API",
    description="Provides search and count endpoints for locally stored CVE data."
)

# --- CORS Middleware FIX ---
# This allows the HTML file running on your local machine (or any origin, *) 
# to make requests to this API server.
origins = [
    "*"  # Allow all origins for local development simplicity
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- END CORS FIX ---

# Middleware to check if the database is available before running endpoints
def check_db_connection():
    if client is None or collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable. Please check the MongoDB server status."
        )

# --- Endpoint 1: Paginated CVE List (Used by the Frontend) ---
@app.get(
    "/cves", 
    response_model=Dict[str, Any], 
    tags=["Data Retrieval"]
)
def get_paginated_cves(skip: int = 0, limit: int = 10):
    """Retrieves a list of CVE records with pagination."""
    check_db_connection()

    try:
        total_count = collection.count_documents({})
        cve_list = list(collection.find().skip(skip).limit(limit))
        
        response_list = []
        for document in cve_list:
            document['_id'] = str(document['_id'])
            response_list.append(document) 

        return {
            "total_count": total_count,
            "data": response_list
        }

    except (OperationFailure, ServerSelectionTimeoutError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB query failed during pagination: Database connection lost or query error: {e}"
        )
    except Exception as e:
        print(f"Unexpected error in GET /cves: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected internal error occurred during data retrieval: {e}"
        )


# --- Endpoint 2: Search by CVE Number ---
@app.get(
    "/cve/{cve_id}", 
    response_model=Dict[str, Any], 
    tags=["Data Retrieval"]
)
def get_cve_details(cve_id: str):
    """
    Retrieves the full details for a specific CVE ID from the local MongoDB.
    """
    check_db_connection()
    
    cve_id_standard = cve_id.upper()
    
    try:
        cve_document = collection.find_one({
            "$or": [
                {"cveId": cve_id_standard},
                {"id": cve_id_standard}
            ]
        })
        
        if cve_document:
            cve_document['_id'] = str(cve_document['_id'])
            return cve_document
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CVE ID '{cve_id}' not found in the local database."
            )
    except (OperationFailure, ServerSelectionTimeoutError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB query failed during search: Database connection lost or query error: {e}"
        )
    except Exception as e:
        print(f"Unexpected error in GET /cve/{cve_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected internal error occurred: {e}"
        )


# --- Endpoint 3: Get Document Count ---
@app.get(
    "/count", 
    response_model=Dict[str, Any], 
    tags=["Data Retrieval"]
)
def get_document_count():
    """
    Returns the total number of CVE documents stored in the MongoDB collection.
    """
    check_db_connection()
    
    try:
        total_count = collection.count_documents({})
        
        return {
            "database": collection.database.name,
            "collection": collection.name,
            "total_documents": total_count,
            "status": "success"
        }
    except (OperationFailure, ServerSelectionTimeoutError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB query failed during count: Database connection lost or query error: {e}"
        )
    except Exception as e:
        print(f"Error retrieving document count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected internal application error occurred."
        )