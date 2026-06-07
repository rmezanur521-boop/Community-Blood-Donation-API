from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.donor_router import router as donor_router
from app.routers.blood_request_router import router as blood_request_router
from app.routers.dashboard_router import router as dashboard_router

app = FastAPI(
    title="Community Blood Donation API",
    description="A REST API for managing blood donations and requests",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


# Include Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(donor_router, prefix="/api/v1")
app.include_router(blood_request_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Community Blood Donation API is running!",
        "docs": "/docs",
        "version": "1.0.0"
    }