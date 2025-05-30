from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

app = FastAPI()

IBM_QUANTUM_API_TOKEN = os.getenv("IBM_QUANTUM_API_TOKEN") or "<your-quantum-api-token>"
service = QiskitRuntimeService(channel="cloud", token=IBM_QUANTUM_API_TOKEN)

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
