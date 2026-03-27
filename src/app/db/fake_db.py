from typing import Any

from pwdlib import PasswordHash

ph: PasswordHash = PasswordHash.recommended()

fake_users_db: dict[str, dict[str, Any]] = {
    "johndoe": {
        "id": "1",
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": ph.hash("secret"),
        "disabled": False,
    },
    "alice": {
        "id": "2",
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": ph.hash("secret2"),
        "disabled": True,
    },
}
