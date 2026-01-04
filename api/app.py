# FastAPI app entry

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import discovery, data, stats, search, export, sync, logs

app = FastAPI(
    title="UPEOS - Uttar Pradesh E-Procurement Service",
    description="API for accessing and analyzing Uttar Pradesh paddy procurement data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(discovery.router, prefix="/api/v1", tags=["discovery"])
app.include_router(data.router, prefix="/api/v1", tags=["data"])
app.include_router(stats.router, prefix="/api/v1", tags=["statistics"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(export.router, prefix="/api/v1", tags=["export"])
app.include_router(sync.router, prefix="/api/v1", tags=["synchronization"])
app.include_router(logs.router, prefix="/api/v1", tags=["logs"])

@app.get("/")
async def root():
    """
    Root endpoint that returns basic information about the API.
    """
    return {
        "message": "UPEOS - Uttar Pradesh E-Procurement Service",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}