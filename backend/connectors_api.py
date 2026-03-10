from fastapi import APIRouter
from backend.db import get_db

router = APIRouter()


@router.get("/connectors")
def list_connectors():

    conn = get_db()
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT id,type,name,host,username FROM connectors"
    ).fetchall()

    result = []

    for r in rows:

        result.append({
            "id": r["id"],
            "type": r["type"],
            "name": r["name"],
            "host": r["host"],
            "username": r["username"]
        })

    conn.close()

    return result


@router.post("/connectors")
def add_connector(connector: dict):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO connectors(type,name,host,username,token)
        VALUES(?,?,?,?,?)
        """,
        (
            connector.get("type"),
            connector.get("name"),
            connector.get("host"),
            connector.get("username"),
            connector.get("token")
        )
    )

    conn.commit()
    conn.close()

    return {"status": "connector added"}


@router.delete("/connectors/{connector_id}")
def delete_connector(connector_id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM connectors WHERE id=?",
        (connector_id,)
    )

    conn.commit()
    conn.close()

    return {"status": "connector removed"}
