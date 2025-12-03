"""
Twitter/X OAuth 2.0 integration
Handles OAuth flow and token management
"""
import os
import secrets
from typing import Optional, Dict
from datetime import datetime, timedelta
from authlib.integrations.requests_client import OAuth2Session

# Twitter OAuth Configuration
TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID", "")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET", "")
TWITTER_REDIRECT_URI = os.getenv("TWITTER_REDIRECT_URI", "http://localhost:8000/auth/twitter/callback")
TWITTER_AUTH_URL = "https://twitter.com/i/oauth2/authorize"
TWITTER_TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
TWITTER_SCOPE = "tweet.read tweet.write users.read offline.access"


def generate_oauth_state() -> str:
    """Generate a secure random state for OAuth"""
    return secrets.token_urlsafe(32)


def get_authorization_url(state: str) -> tuple[str, str]:
    """
    Get Twitter OAuth authorization URL
    
    Returns:
        Tuple of (authorization_url, code_verifier)
    """
    client = OAuth2Session(
        TWITTER_CLIENT_ID,
        TWITTER_CLIENT_SECRET,
        redirect_uri=TWITTER_REDIRECT_URI,
        scope=TWITTER_SCOPE,
        state=state
    )
    
    # Generate PKCE code verifier and challenge
    code_verifier = secrets.token_urlsafe(32)
    
    authorization_url, state = client.create_authorization_url(
        TWITTER_AUTH_URL,
        code_verifier=code_verifier
    )
    
    return authorization_url, code_verifier


async def exchange_code_for_token(code: str, code_verifier: str) -> Optional[Dict]:
    """
    Exchange authorization code for access token
    
    Args:
        code: Authorization code from callback
        code_verifier: PKCE code verifier
        
    Returns:
        Token data including access_token and refresh_token
    """
    try:
        client = OAuth2Session(
            TWITTER_CLIENT_ID,
            TWITTER_CLIENT_SECRET,
            redirect_uri=TWITTER_REDIRECT_URI
        )
        
        token = client.fetch_token(
            TWITTER_TOKEN_URL,
            code=code,
            code_verifier=code_verifier
        )
        
        return {
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
            "expires_in": token.get("expires_in", 7200),
            "scope": token.get("scope"),
            "token_type": token.get("token_type")
        }
    except Exception as e:
        print(f"Error exchanging code for token: {e}")
        return None


async def refresh_access_token(refresh_token: str) -> Optional[Dict]:
    """
    Refresh an expired access token
    
    Args:
        refresh_token: The refresh token
        
    Returns:
        New token data
    """
    try:
        client = OAuth2Session(
            TWITTER_CLIENT_ID,
            TWITTER_CLIENT_SECRET
        )
        
        token = client.refresh_token(
            TWITTER_TOKEN_URL,
            refresh_token=refresh_token
        )
        
        return {
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
            "expires_in": token.get("expires_in", 7200)
        }
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return None


async def get_twitter_user_info(access_token: str) -> Optional[Dict]:
    """
    Get Twitter user information using access token
    
    Args:
        access_token: Twitter access token
        
    Returns:
        User info including id and username
    """
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.twitter.com/2/users/me",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "user_id": data["data"]["id"],
                    "username": data["data"]["username"],
                    "name": data["data"].get("name")
                }
        
        return None
    except Exception as e:
        print(f"Error getting Twitter user info: {e}")
        return None
