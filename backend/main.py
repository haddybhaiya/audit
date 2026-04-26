from fastapi import FastAPI
from backend.api.upload import router as upload_router
from backend.api.scan import router as scan_router
from backend.api.audit import router as audit_router
from backend.api.probe import router as probe_router
from backend.api.mock_model import router as mock_router # Import the mock model router

app = FastAPI(title = "Audit")
app.include_router(upload_router)
app.include_router(scan_router)
app.include_router(audit_router)
app.include_router(probe_router)
app.include_router(mock_router) # Include the mock model router for testing purposes



@app.get("/")
def root():
    return {"message": "audit is running"}
