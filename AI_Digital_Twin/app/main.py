from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.database import (
    initialize_database,
    fetch_all,
    fetch_one
)

from app.seed import seed_database
from app.security import (
    verify_password,
    create_session_token
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Digital Twin of the Internet",
    description="A simulated AI-powered digital twin dashboard of internet activity.",
    version="1.0.0"
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ============================================================
# SIMPLE SESSION STORAGE
# ============================================================

sessions = {}


# ============================================================
# LOGIN REQUEST MODEL
# ============================================================

class LoginRequest(BaseModel):
    username: str
    password: str


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    initialize_database()

    seed_database()


# ============================================================
# PAGE ROUTES
# ============================================================

@app.get("/")
def login_page():

    return FileResponse(
        TEMPLATES_DIR / "login.html"
    )


@app.get("/dashboard")
def dashboard_page():

    return FileResponse(
        TEMPLATES_DIR / "dashboard.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.post("/api/login")
def login(data: LoginRequest):

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (data.username,)
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    if not verify_password(
        data.password,
        user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    token = create_session_token()

    sessions[token] = user["id"]

    response = JSONResponse(
        {
            "success": True,
            "message": "Login successful",
            "redirect": "/dashboard"
        }
    )

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8
    )

    return response


# ============================================================
# LOGOUT
# ============================================================

@app.post("/api/logout")
def logout(request: Request):

    token = request.cookies.get("session_token")

    if token:

        sessions.pop(token, None)

    response = JSONResponse(
        {
            "success": True
        }
    )

    response.delete_cookie(
        "session_token"
    )

    return response


# ============================================================
# GET CURRENT USER
# ============================================================

@app.get("/api/me")
def current_user(request: Request):

    token = request.cookies.get("session_token")

    if not token or token not in sessions:

        raise HTTPException(
            status_code=401,
            detail="Not logged in."
        )

    user_id = sessions[token]

    user = fetch_one(
        """
        SELECT id, name, username, role, points
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found."
        )

    return user


# ============================================================
# AUTHENTICATION HELPER
# ============================================================

def require_login(request: Request):

    token = request.cookies.get("session_token")

    if not token or token not in sessions:

        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    user_id = sessions[token]

    return user_id


# ============================================================
# COMPLETE DASHBOARD DATA
# ============================================================

@app.get("/api/dashboard")
def dashboard_data(request: Request):

    require_login(request)

    technologies = fetch_all(
        "technologies"
    )

    hiring = fetch_all(
        "hiring_signals"
    )

    ai_tools = fetch_all(
        "ai_tools"
    )

    threats = fetch_all(
        "threats"
    )

    startups = fetch_all(
        "startups"
    )

    activities = fetch_all(
        "activities"
    )

    users = fetch_all(
        "users"
    )

    # Leaderboard
    leaderboard = sorted(
        users,
        key=lambda x: x["points"],
        reverse=True
    )

    # Remove password hash from leaderboard
    leaderboard = [
        {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "role": user["role"],
            "points": user["points"]
        }
        for user in leaderboard
    ]

    return {
        "technology_count": len(technologies),
        "hiring_count": len(hiring),
        "ai_tool_count": len(ai_tools),
        "threat_count": len(threats),
        "startup_count": len(startups),

        "technologies": technologies,
        "hiring": hiring,
        "ai_tools": ai_tools,
        "threats": threats,
        "startups": startups,
        "activities": activities,
        "leaderboard": leaderboard
    }


# ============================================================
# SEARCH
# ============================================================

@app.get("/api/search")
def search(
    request: Request,
    q: Optional[str] = None
):

    require_login(request)

    if not q:

        return {
            "query": "",
            "results": []
        }

    query = q.lower().strip()

    results = []

    technologies = fetch_all(
        "technologies"
    )

    for item in technologies:

        if (
            query in item["name"].lower()
            or query in item["category"].lower()
        ):

            results.append({
                "type": "Technology",
                "name": item["name"],
                "details": item["category"]
            })

    hiring = fetch_all(
        "hiring_signals"
    )

    for item in hiring:

        if (
            query in item["company"].lower()
            or query in item["sector"].lower()
        ):

            results.append({
                "type": "Company",
                "name": item["company"],
                "details": item["sector"]
            })

    ai_tools = fetch_all(
        "ai_tools"
    )

    for item in ai_tools:

        if (
            query in item["name"].lower()
            or query in item["category"].lower()
        ):

            results.append({
                "type": "AI Tool",
                "name": item["name"],
                "details": item["category"]
            })

    startups = fetch_all(
        "startups"
    )

    for item in startups:

        if (
            query in item["name"].lower()
            or query in item["sector"].lower()
            or query in item["location"].lower()
        ):

            results.append({
                "type": "Startup",
                "name": item["name"],
                "details": item["sector"]
            })

    return {
        "query": q,
        "results": results[:20]
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "online",
        "system": "AI Digital Twin",
        "simulation": "active"
    }