"""
Medium OAuth integration
Handles OAuth flow for Medium publishing
"""
import os
from typing import Optional, Dict
from authlib.integrations.requests_client import OAuth2Session

# Medium OAuth Configuration
MEDIUM_CLIENT_ID = os.getenv("MEDIUM_CLIENT_ID", "")
MEDIUM_CLIENT_SECRET = os.getenv("MEDIUM_CLIENT_SECRET", "")
MEDIUM_REDIRECT_URI = os.getenv("MEDIUM_REDIRECT_URI", "http://localhost:8000/auth/medium/callback")
MEDIUM_AUTH_URL = "https://medium.com/m/oauth/authorize"
MEDIUM_TOKEN_URL = "https://medium.com/v1/tokens"
MEDIUM_SCOPE = "basicProfile,publishPost"


def get_authorization_url(state: str) -> str:
    """
    Get Medium OAuth authorization URL
    
    Args:
        state: Random state for CSRF protection
        
    Returns:
        Authorization URL
    """
    client = OAuth2Session(
        MEDIUM_CLIENT_ID,
        MEDIUM_CLIENT_SECRET,
        redirect_uri=MEDIUM_REDIRECT_URI,
        scope=MEDIUM_SCOPE,
        state=state
    )
    
    authorization_url, _ = client.create_authorization_url(MEDIUM_AUTH_URL)
    return authorization_url


async def exchange_code_for_token(code: str) -> Optional[Dict]:
    """
    Exchange authorization code for access token
    
    Args:
        code: Authorization code from callback
        
    Returns:
        Token data including access_token
    """
    try:
        client = OAuth2Session(
            MEDIUM_CLIENT_ID,
            MEDIUM_CLIENT_SECRET,
            redirect_uri=MEDIUM_REDIRECT_URI
        )
        
        token = client.fetch_token(
            MEDIUM_TOKEN_URL,
            code=code,
            grant_type="authorization_code"
        )
        
        return {
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
            "expires_in": token.get("expires_in"),
            "scope": token.get("scope")
        }
    except Exception as e:
        print(f"Error exchanging code for token: {e}")
        return None


async def get_medium_user_info(access_token: str) -> Optional[Dict]:
    """
    Get Medium user information
    
    Args:
        access_token: Medium access token
        
    Returns:
        User info including id and username
    """
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.medium.com/v1/me",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()["data"]
                return {
                    "user_id": data["id"],
                    "username": data["username"],
                    "name": data.get("name"),
                    "url": data.get("url")
                }
        
        return None
    except Exception as e:
        print(f"Error getting Medium user info: {e}")
        return None
