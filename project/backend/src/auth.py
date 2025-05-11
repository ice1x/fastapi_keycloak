from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.utils import base64url_decode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from typing import Dict, Any, Callable, Awaitable
import httpx

from src.config import settings

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

OPENID_CONFIG_URL: str = f"{settings.keycloak_url}/realms/{settings.realm}/.well-known/openid-configuration"


async def get_public_key() -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(OPENID_CONFIG_URL)
        jwks_uri: str = resp.json()["jwks_uri"]
        keys_resp = await client.get(jwks_uri)
        return keys_resp.json()["keys"][0]


def construct_rsa_public_key(jwk: Dict[str, str]) -> rsa.RSAPublicKey:
    e: int = int.from_bytes(base64url_decode(jwk["e"].encode()), "big")
    n: int = int.from_bytes(base64url_decode(jwk["n"].encode()), "big")
    public_numbers: rsa.RSAPublicNumbers = rsa.RSAPublicNumbers(e, n)
    return public_numbers.public_key()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        jwk: Dict[str, str] = await get_public_key()
        public_key: rsa.RSAPublicKey = construct_rsa_public_key(jwk)
        pem: bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        payload: Dict[str, Any] = jwt.decode(token, pem, algorithms=[settings.algorithm], audience=settings.client_id)
        username: str = payload.get("preferred_username")
        roles: list[str] = payload.get("realm_access", {}).get("roles", [])
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"username": username, "roles": roles}
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid token: {e}")


def require_role(role: str) -> Callable[[Any], Awaitable[Dict[str, Any]]]:
    async def role_checker(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if role not in user["roles"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return role_checker
