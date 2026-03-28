import sqlite3

def connect_db():
    conn = sqlite3.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("successfully created")

def add_item(name,price,quantity):
    conn = sqlite3.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (name,price,quantity) VALUES (?,?,?)",(name,price,quantity))
    conn.commit()
    conn.close()
    print("successfully added")


def delete_item(item_id):
    conn = sqlite3.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?",(item_id,))_
    conn.commit()
    conn.close()
    print("successfully deleted")

def fetch_all():
    conn = sqlite3.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    row=cursor.fetchall()
    conn.close()
    return row