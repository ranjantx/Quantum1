from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os
import json
import sys
import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure you have the required packages installed:
# pip install fastapi qiskit qiskit-ibm-runtime python-dotenv uvicorn
# To run the FastAPI app, use the command: uvicorn main:app --reload
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Load environment variables from .env.local file
# If you don't have a .env.local file, create one with your IBM Quantum API token
# Load .env.local only if variables are not already set
if os.getenv("IBM_CLOUD_EXECUTION_ENVIRONMENT") != "code_engine":
    load_dotenv(dotenv_path=".env.local", override=False)

IBM_QUANTUM_API_TOKEN = os.getenv("IBM_QUANTUM_API_TOKEN")
if not IBM_QUANTUM_API_TOKEN:
    sys.exit("❌ IBM_QUANTUM_API_TOKEN is missing. Set it in .env.local or Code Engine env vars.")

# Initialize FastAPI app
app = FastAPI()

IBM_QUANTUM_API_TOKEN = os.getenv("IBM_QUANTUM_API_TOKEN") or "<your-quantum-api-token>"
service = QiskitRuntimeService(channel="ibm_cloud", token=IBM_QUANTUM_API_TOKEN)

@app.get("/predict")
def quantum_stock_prediction():
    try:
        qc = QuantumCircuit(1)
        qc.h(0)

        sampler = SamplerV2(service=service)
        job = sampler.run(circuits=[qc], shots=1024)
        result = job.result()

        counts = result.quasi_dists[0].binary_probabilities()
        return {"prediction": counts}
    except Exception as e:
        return {"error": str(e)}
@app.get("/")
def root():
    return {"message": "Welcome to the Quantum Stock Prediction API. Use /predict to get predictions."}
@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.get("/version")
def version():
    return {"version": "1.0.0", "description": "Quantum Stock Prediction API using Qiskit and IBM Quantum."}
@app.get("/docs")
def docs():
    return {"message": "API documentation is available at /docs."}
@app.get("/about")
def about():
    return {
        "name": "Quantum Stock Prediction API from AccelCQ",
        "version": "1.0.0",
        "description": "An API that uses quantum computing to predict stock market trends.",
        "author": "Your Name",
        "contact": "ranjan@accelcq.com"
    }
@app.get("/contact")
def contact():
    return {
        "email": "ranjan@accelcq.com",
        "phone": "+1234567890",
        "website": "https://www.accelcq.com",
        "social_media": {
            "twitter": "@accelcq",
            "linkedin": "https://www.linkedin.com/company/accelcq"
        }
    }
@app.get("/privacy")
def privacy_policy():
    return {
        "policy": "We respect your privacy. No personal data is collected through this API.",
        "data_usage": "Data is used solely for the purpose of providing quantum stock predictions.",
        "contact": "For any privacy concerns, please contact us at ranjan@accelcq.com"
    }
@app.get("/terms")
def terms_of_service():
    return {
        "terms": "By using this API, you agree to the terms and conditions set forth by AccelCQ.",
        "usage": "The API is provided 'as is' without any warranties.",
        "liability": "AccelCQ is not liable for any damages arising from the use of this API.",
        "contact": "For any inquiries, please contact us at ranjan@accelcq.com"
    }
@app.get("/feedback")
def feedback():
    return {
        "message": "We welcome your feedback to improve our API.",
        "email": "ranjan@accelcq.com"
    }
@app.get("/support")
def support():
    return {
        "message": "For support, please contact us at ranjan@accelcq.com"
    }   