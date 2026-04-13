from fastapi import FastAPI
from backend.api.upload import router as upload_router
from backend.api.scan import router as scan_router
from backend.api.audit import router as audit_router

app = FastAPI(title = "Audit")
app.include_router(upload_router)
app.include_router(scan_router)
app.include_router(audit_router)

@app.get("/")
def root():
    return {"message": "audit is running"}
