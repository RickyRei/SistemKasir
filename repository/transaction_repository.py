from repository.repository import Repository
from model.transaction import Transaction, TransactionDetail


class TransactionRepository(Repository):

    def __init__(self, db):
        self.db = db

    def add(self, transaction):
        self.db.cursor.execute(
            "INSERT INTO transaksi (tanggal, total) VALUES (?, ?)",
            (transaction.tanggal, transaction.total)
        )
        transaksi_id = self.db.cursor.lastrowid
        for detail in transaction.details:
            self.db.cursor.execute(
                "INSERT INTO detail_transaksi (transaksi_id, produk_id, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                (transaksi_id, detail.produk_id, detail.jumlah, detail.subtotal)
            )
        self.db.conn.commit()
        return transaksi_id

    def update(self, transaction):
        self.db.cursor.execute(
            "UPDATE transaksi SET tanggal=?, total=? WHERE id=?",
            (transaction.tanggal, transaction.total, transaction.id)
        )
        self.db.conn.commit()

    def delete(self, id):
        self.db.cursor.execute("DELETE FROM detail_transaksi WHERE transaksi_id=?", (id,))
        self.db.cursor.execute("DELETE FROM transaksi WHERE id=?", (id,))
        self.db.conn.commit()

    def find_by_id(self, id):
        self.db.cursor.execute("SELECT * FROM transaksi WHERE id=?", (id,))
        row = self.db.cursor.fetchone()
        if row is None:
            return None
        trx = Transaction(id=row[0], tanggal=row[1], total=row[2])
        self.db.cursor.execute(
            "SELECT dt.produk_id, p.nama, dt.jumlah, dt.subtotal FROM detail_transaksi dt JOIN produk p ON p.id = dt.produk_id WHERE dt.transaksi_id=?",
            (id,)
        )
        for d in self.db.cursor.fetchall():
            trx.tambah_detail(TransactionDetail(d[0], d[1], d[2], d[3]))
        return trx

    def find_all(self):
        self.db.cursor.execute("SELECT * FROM transaksi ORDER BY id DESC")
        rows = self.db.cursor.fetchall()
        return [Transaction(id=r[0], tanggal=r[1], total=r[2]) for r in rows]