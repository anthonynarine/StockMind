from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routes.auth import router as auth_router
from app.holdings.routes import router as holdings_router

"""
Main application entry point for the Dwight Assistant API.

This file:
- Instantiates the FastAPI app
- Registers modular API routes
- Defines the root health check endpoint

FastAPI automatically generates OpenAPI docs at:
- /docs     → Swagger UI
- /redoc    → ReDoc UI
"""

# ----------------------------------------
# 🚀 Create FastAPI app instance
# ----------------------------------------
app = FastAPI(
    title="Dwight Assistant",
    description="AI-powered assistant to manage and analyze your stock/crypto portfolio.",
    version="0.1.0"
)

# ----------------------------------------
# 🌐 CORS Middleware (for frontend)
# ----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 🔁 Change to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# 🔐 Authentication Routes
# ----------------------------------------
app.include_router(auth_router)

# ----------------------------------------
# 📊 Holdings Routes
# ----------------------------------------
app.include_router(holdings_router, prefix="/holdings", tags=["Holdings"])

# ----------------------------------------
# ✅ Root Health Check
# ----------------------------------------
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint to confirm the API is online.
    """
    return {"message": "Dwight is running"}
