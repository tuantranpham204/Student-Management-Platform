from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any
import json
import math


def get_all_subjects() -> List[sn]:
    query = "SELECT id, name, coff FROM subjects"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_subject_by_id(id: str) -> Optional[sn]:
    query = "SELECT id, name, coff FROM subjects WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)


def add_subject(id: str, name: str, reg1: float, reg2: float, reg3: float, mid: float, fin: float) -> bool:
    validate_coefficients(reg1, reg2, reg3, mid, fin)

    # Create dictionary and convert to JSON string
    coff_dict = {
        "reg1": reg1, "reg2": reg2, "reg3": reg3,
        "mid": mid, "fin": fin
    }
    coff_json = json.dumps(coff_dict)

    query = "INSERT INTO subjects (id, name, coff) VALUES (%s, %s, %s)"
    cursor.execute(query, (id, name, coff_json))
    conn.commit()
    return True

def delete_subject(id: str) -> bool:
    query = "DELETE FROM subjects WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True


def validate_coefficients(reg1, reg2, reg3, mid, fin):
    """Validates that coefficients are between 0-1 and sum to exactly 1.0"""
    coeffs = [reg1, reg2, reg3, mid, fin]

    # Check range (0 <= x < 1)
    # Note: If a subject is 100% final, fin=1.0. The requirement "below 1" strictly would prevent this.
    # However, standard logic usually allows 0 <= x <= 1.
    # Based on prompt "between 0 and below 1", we strictly check < 1 for individual components.
    # This implies no single component can be 100%.
    for c in coeffs:
        if not (0 <= c < 1):
            raise ValueError(f"Coefficient value {c} must be >= 0 and < 1")

    # Check sum (using close comparison for float precision)
    total = sum(coeffs)
    if not math.isclose(total, 1.0, rel_tol=1e-9):
        raise ValueError(f"Coefficients must sum to 1.0. Current sum: {total}")


def get_subjects_by_params(subject: dict) -> List[sn]:
    where, binds = select_binds(subject)
    query = f"SELECT id, name, coff FROM subjects s {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]


def update_subject(subject: dict) -> bool:
    # If coefficients are present in the update dict, we need to process them
    # This assumes if one coefficient is updated, all must be provided to ensure validation
    # Or at least we need to reconstruct the json.

    # Check if we have coefficient keys
    if all(k in subject for k in ['reg1', 'reg2', 'reg3', 'mid', 'fin']):
        validate_coefficients(
            subject['reg1'], subject['reg2'], subject['reg3'],
            subject['mid'], subject['fin']
        )
        coff_dict = {
            "reg1": subject['reg1'], "reg2": subject['reg2'], "reg3": subject['reg3'],
            "mid": subject['mid'], "fin": subject['fin']
        }
        subject['coff'] = json.dumps(coff_dict)
        # Remove individual keys so they don't confuse update_binds
        for k in ['reg1', 'reg2', 'reg3', 'mid', 'fin']:
            if k in subject: del subject[k]

    set_clause, binds = update_binds(subject)
    query = f"UPDATE subjects s {set_clause} WHERE s.id = '{subject['id']}'"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(subject: dict):
    where, binds, params = ' WHERE ', [], 0
    if subject.get("id"):
        if params != 0: where += ' AND'
        where += f" s.id LIKE '%{subject['id']}%' "
        params += 1
    if subject.get("name"):
        if params != 0: where += ' AND'
        where += f" s.name LIKE '%{subject['name']}%' "
        params += 1
    if subject.get("coff"):
        if params != 0: where += ' AND'
        where += ' s.coff = %s '
        binds.append(subject["coff"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(subject: dict):
    set_clause, binds = ' SET', []
    if subject.get("name"):
        set_clause += " s.name = %s ,"
        binds.append(subject["name"])
    if subject.get("coff"):
        set_clause += " s.coff = %s ,"
        binds.append(subject["coff"])
    set_clause = set_clause[:-1]
    return set_clause, binds
