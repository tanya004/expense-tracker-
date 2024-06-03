import sqlite3

class database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE A TABLE IF NOT EXISTS expense_record (item_name text, item_price float, purchase_date date)")
        self.con.commit()
    
    def fetchRecord(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
    
    def insertRecord(self, item_name, item_price, purchase_date):
        self.cur.execute("INSERT INTO expense_record VALUES (?, ?, ?)",
                         (item_name, item_price, purchase_date))
        self.con.commit()

    def  removeRecord(self, rwid):
        self.cur.excute("DELETE FROM expense_record where rowid=?", (rwid,))
        self.conn.commit()

    def updateRecord(self, item_name, item_price, purchase_date, rid):
        self.cur.excute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_dtae = ?",
                        (item_name, item_price, purchase_date))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()