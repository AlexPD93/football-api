"""
Login router for the Football API.

Handles routes for the HTML login page.
"""

import os
from urllib.parse import quote
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request

from starlette.responses import RedirectResponse

router = APIRouter()

# This middleware is required for OAuth to track the login state

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    """
    Initiates the Google OAuth login process.

    Redirects the user to the Google login page.
    """
    redirect_uri = request.url_for("auth_callback")

    # Force HTTPS for the redirect URI if the request was forwarded via HTTPS
    if request.headers.get("x-forwarded-proto") == "https":
        redirect_uri = str(redirect_uri).replace("http://", "https://", 1)

    return await oauth.google.authorize_redirect(request, redirect_uri)


# 2. Handle the Callback & Check the Whitelist
@router.get("/auth/callback")
async def auth_callback(request: Request):
    """
    Handles the Google OAuth callback.

    Verifies the user's Google account, checks against an admin whitelist,
    and either logs the user in or denies access.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        # Improved error logging for debugging production issues
        print(f"OAuth Access Token Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    email = user_info["email"]
    whitelist = os.environ.get("ADMIN_WHITELIST", "").split(",")

    # THE BOUNCER LOGIC
    if email not in whitelist:
        # Clear any partial session and reject
        request.session.clear()
        # Encode the message so it's safe for a URL
        error_msg = quote(f"Access Denied: {email} is not registered for admin access.")
        return RedirectResponse(url=f"/dashboard?error={error_msg}")

    # Log them in (Save to Session)
    request.session["user"] = email
    return RedirectResponse(url="/dashboard")


@router.get("/logout")
async def logout(request: Request):
    """Clears the session cookie."""
    request.session.clear()
    return RedirectResponse(url="/dashboard")
