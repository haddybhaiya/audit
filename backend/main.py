from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.upload import router as upload_router
from backend.api.scan import router as scan_router
from backend.api.audit import router as audit_router
from backend.api.probe import router as probe_router
from backend.api.mock_model import router as mock_router
from backend.api.surrogate import router as surrogate_router
from backend.api.report import router as report_router
from dotenv import load_dotenv
load_dotenv()




app = FastAPI(title="Audit")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False
)
app.include_router(upload_router)
app.include_router(scan_router)
app.include_router(audit_router)
app.include_router(probe_router)
app.include_router(mock_router)
app.include_router(surrogate_router)
app.include_router(report_router)



@app.get("/")
def root():
    return {"message": "audit is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
