import sqlite3
import requests
from fastapi import APIRouter, HTTPException
from backend.db import get_db

router = APIRouter()


# -------------------------
# List connectors
# -------------------------

@router.get("/connectors")
def list_connectors():

    db = get_db()
    cur = db.cursor()

    rows = cur.execute(
        "SELECT id,type,name,host,username,token_name,token_secret,port FROM connectors"
    ).fetchall()

    connectors = []

    for r in rows:
        connectors.append({
            "id": r[0],
            "type": r[1],
            "name": r[2],
            "host": r[3],
            "username": r[4],
            "token_name": r[5],
            "token_secret": r[6],
            "port": r[7]
        })

    return connectors


# -------------------------
# Add connector
# -------------------------

@router.post("/connectors")
def add_connector(data: dict):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO connectors(type,name,host,username,token_name,token_secret,port)
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            data["type"],
            data["name"],
            data["host"],
            data.get("username"),
            data.get("token_name"),
            data.get("token_secret"),
            data.get("port")
        )
    )

    db.commit()

    return {"status": "added"}


# -------------------------
# Update connector
# -------------------------

@router.put("/connectors/{cid}")
def update_connector(cid: int, data: dict):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE connectors
        SET type=?, name=?, host=?, username=?, token_name=?, token_secret=?, port=?
        WHERE id=?
        """,
        (
            data["type"],
            data["name"],
            data["host"],
            data.get("username"),
            data.get("token_name"),
            data.get("token_secret"),
            data.get("port"),
            cid
        )
    )

    db.commit()

    return {"status": "updated"}


# -------------------------
# Delete connector
# -------------------------

@router.delete("/connectors/{cid}")
def delete_connector(cid: int):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "DELETE FROM connectors WHERE id=?",
        (cid,)
    )

    db.commit()

    return {"status": "deleted"}


# -------------------------
# Test connector
# -------------------------

@router.get("/connectors/test/{cid}")
def test_connector(cid: int):

    db = get_db()
    cur = db.cursor()

    row = cur.execute(
        "SELECT type,host,username,token_name,token_secret,port FROM connectors WHERE id=?",
        (cid,)
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Connector not found")

    type_, host, username, token_name, token_secret, port = row

    if type_ != "proxmox":
        return {"success": False, "message": "Unsupported connector type"}

    try:

        headers = {
            "Authorization": f"PVEAPIToken={username}!{token_name}={token_secret}"
        }

        r = requests.get(
            f"https://{host}:{port}/api2/json/nodes",
            headers=headers,
            verify=False,
            timeout=5
        )

        if r.status_code == 200:
            return {"success": True}

        return {"success": False}

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
