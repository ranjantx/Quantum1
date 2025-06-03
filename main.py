from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit_ibm_runtime import Sampler
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
logging.info("Initializing QiskitRuntimeService with IBM Quantum API token...", IBM_QUANTUM_API_TOKEN=IBM_QUANTUM_API_TOKEN)
service = QiskitRuntimeService(channel="ibm_cloud", token=IBM_QUANTUM_API_TOKEN)

        # Check if the service is initialized correctly
if not service:
    raise Exception("QiskitRuntimeService is not initialized. Check your IBM Quantum API token.")
if not isinstance(service, QiskitRuntimeService):
    raise Exception("Invalid QiskitRuntimeService instance. Ensure you are using the correct service.")

logging.info("Creating quantum circuit for stock prediction...")
        # Print available backends for debugging
logging.info("Available backends:")
if not service.backends():
            raise Exception("No available backends found. Ensure your IBM Quantum API token is valid and you have access to the backends.")
        # Print the backends for debugging
logging.info("Available backends: %s", service.backends())
        # Uncomment the line below to see the backends in the console
print(service.backends())   
        
@app.get("/predict")
def quantum_stock_prediction():
    try:
        
        # define the bell state circuit to run on the IBM Quantum backend using qiskit 2.0.0
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        logging.info("Quantum circuit created successfully.")
        logging.info("Running the quantum circuit on IBM Quantum backend...")
        # Run the circuit using the Qiskit-ibm-runtime 0.40.0
        if not service:
            raise Exception("QiskitRuntimeService is not initialized. Check your IBM Quantum API token.")
        if not isinstance(service, QiskitRuntimeService):
            raise Exception("Invalid QiskitRuntimeService instance. Ensure you are using the correct service.")
        if not service.backends():
            raise Exception("No available backends found.")
        backend = service.get_backend("ibm_perth")  # Use a specific backend, e.g., "ibm_perth"
        if not backend:
            raise Exception("Backend not found. Ensure the backend name is correct and available.")
        # Use Sampler inside service.run()
        options = {"backend": "ibm_perth"}
        sampler = Sampler(circuits=[qc], options=options)
        job = service.run(sampler, shots=1024)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()
        print(counts)    
            # logging.info("Creating a sampler instance...")
            # sampler = SamplerV2()
            # job = sampler.run(circuits=[qc], shots=1024)
            # result = job.result()

            # counts = result.quasi_dists[0].binary_probabilities()
            # return {"prediction": counts}
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