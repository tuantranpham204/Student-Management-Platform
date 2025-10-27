from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any
from config.auth import hash_password, verify_password


def get_all_users() -> List[sn]:
    query = "SELECT id, username, password, name, email FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_user_by_id(id: int) -> Optional[sn]:
    query = "SELECT id, username, password, name, email FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def get_user_by_username(username: str) -> Optional[sn]:
    query = "SELECT id, username, password, name, email FROM users WHERE username = %s"
    cursor.execute(query, [username])
    row = cursor.fetchone()
    return sn(**row)

def add_user(username: str, email: str, plain_password: str, name: Optional[str] = None) -> Optional[int]:
    hashed_pass = hash_password(plain_password)
    query = "INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (username, hashed_pass, name, email))
    conn.commit()
    return cursor.lastrowid

def update_user(id: int, username: str, email: str, name: Optional[str] = None) -> bool:
    query = "UPDATE users SET username = %s, email = %s, name = %s WHERE id = %s"
    cursor.execute(query, (username, email, name, id))
    conn.commit()
    return True



