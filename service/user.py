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

def get_users_by_params(user: dict) -> List[sn]:
    where, binds = select_binds(user)
    query = f"SELECT id, username, password, name, email FROM users u {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_user(user: dict) -> bool:
    set_clause, binds = update_binds(user)
    query = f"UPDATE users u {set_clause} WHERE u.id = {user['id']}"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(user: dict):
    where, binds, params = ' WHERE ', [], 0
    if user.get("id"):
        if params != 0: where += ' AND'
        where += ' u.id = %s '
        binds.append(user["id"])
        params += 1
    if user.get("username"):
        if params != 0: where += ' AND'
        where += f" u.username LIKE '%{user['username']}%' "
        params += 1
    if user.get("name"):
        if params != 0: where += ' AND'
        where += f" u.name LIKE '%{user['name']}%' "
        params += 1
    if user.get("email"):
        if params != 0: where += ' AND'
        where += f" u.email LIKE '%{user['email']}%' "
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(user: dict):
    set_clause, binds = ' SET', []
    if user.get("username"):
        set_clause += " u.username = %s ,"
        binds.append(user["username"])
    if user.get("password"):
        set_clause += " u.password = %s ,"
        binds.append(user["password"])
    if user.get("name"):
        set_clause += " u.name = %s ,"
        binds.append(user["name"])
    if user.get("email"):
        set_clause += " u.email = %s ,"
        binds.append(user["email"])
    set_clause = set_clause[:-1]
    return set_clause, binds



