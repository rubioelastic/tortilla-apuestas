"""
🔐 Autenticación y Seguridad
Manejo de JWT tokens y hashing de contraseñas
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

SECRET_KEY = os.getenv("SECRET_KEY", "my-super-secret-key-change-this-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 30 días

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad HTTP Bearer
security = HTTPBearer()


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE CONTRASEÑA
# ═══════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    """Hashear contraseña (bcrypt tiene límite de 72 bytes)"""
    # Truncar a 72 caracteres para evitar el límite de bcrypt
    truncated = password[:72]
    return pwd_context.hash(truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    # Truncar a 72 caracteres como en hash_password
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)


# ═══════════════════════════════════════════════════════════════
# FUNCIONES JWT
# ═══════════════════════════════════════════════════════════════

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear JWT token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Verificar y decodificar JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ═══════════════════════════════════════════════════════════════
# DEPENDENCY PARA FASTAPI
# ═══════════════════════════════════════════════════════════════

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtener usuario actual desde el token
    
    Uso en endpoints:
    @app.get("/protected")
    async def protected_route(username: str = Depends(get_current_user)):
        ...
    """
    token = credentials.credentials
    username = verify_token(token)
    return username
