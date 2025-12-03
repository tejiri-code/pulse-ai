"""
User database operations
CRUD operations for users, social connections, and sessions
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from user_models import User, SocialConnection, UserSession
from auth_utils import hash_password, encrypt_token, decrypt_token


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, password: str, full_name: str = None) -> User:
    """Create a new user"""
    hashed_pwd = hash_password(password)
    user = User(
        email=email,
        hashed_password=hashed_pwd,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_session(db: Session, user_id: int, session_token: str, expires_hours: int = 24) -> UserSession:
    """Create a new user session"""
    session = UserSession(
        user_id=user_id,
        session_token=session_token,
        expires_at=datetime.utcnow() + timedelta(hours=expires_hours)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_token: str) -> Optional[UserSession]:
    """Get session by token"""
    session = db.query(UserSession).filter(UserSession.session_token == session_token).first()
    if session and session.expires_at > datetime.utcnow():
        return session
    return None


def save_social_connection(
    db: Session,
    user_id: int,
    provider: str,
    access_token: str,
    refresh_token: str = None,
    provider_user_id: str = None,
    expires_in: int = None,
    scope: str = None
) -> SocialConnection:
    """Save or update a social media connection"""
    
    # Encrypt tokens before storing
    encrypted_access = encrypt_token(access_token)
    encrypted_refresh = encrypt_token(refresh_token) if refresh_token else None
    
    # Check if connection already exists
    connection = db.query(SocialConnection).filter(
        SocialConnection.user_id == user_id,
        SocialConnection.provider == provider
    ).first()
    
    if connection:
        # Update existing
        connection.access_token = encrypted_access
        connection.refresh_token = encrypted_refresh
        connection.provider_user_id = provider_user_id
        connection.scope = scope
        connection.updated_at = datetime.utcnow()
        if expires_in:
            connection.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    else:
        # Create new
        connection = SocialConnection(
            user_id=user_id,
            provider=provider,
            access_token=encrypted_access,
            refresh_token=encrypted_refresh,
            provider_user_id=provider_user_id,
            scope=scope,
            token_expires_at=datetime.utcnow() + timedelta(seconds=expires_in) if expires_in else None
        )
        db.add(connection)
    
    db.commit()
    db.refresh(connection)
    return connection


def get_social_connection(db: Session, user_id: int, provider: str) -> Optional[SocialConnection]:
    """Get a user's social connection"""
    return db.query(SocialConnection).filter(
        SocialConnection.user_id == user_id,
        SocialConnection.provider == provider
    ).first()


def get_decrypted_tokens(connection: SocialConnection) -> dict:
    """Get decrypted tokens from a social connection"""
    return {
        "access_token": decrypt_token(connection.access_token),
        "refresh_token": decrypt_token(connection.refresh_token) if connection.refresh_token else None
    }


def delete_social_connection(db: Session, user_id: int, provider: str) -> bool:
    """Delete a social connection"""
    connection = get_social_connection(db, user_id, provider)
    if connection:
        db.delete(connection)
        db.commit()
        return True
    return False


def get_user_connections(db: Session, user_id: int) -> List[dict]:
    """Get all social connections for a user"""
    connections = db.query(SocialConnection).filter(SocialConnection.user_id == user_id).all()
    return [
        {
            "provider": conn.provider,
            "connected_at": conn.connected_at.isoformat(),
            "provider_user_id": conn.provider_user_id
        }
        for conn in connections
    ]
