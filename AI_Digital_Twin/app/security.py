import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    Converts a password into a secure hash.
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Checks whether the entered password is correct.
    """

    return secrets.compare_digest(
        hash_password(password),
        password_hash
    )


def create_session_token() -> str:
    """
    Creates a random login session token.
    """

    return secrets.token_urlsafe(32)