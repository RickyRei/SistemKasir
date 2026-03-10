import sqlite3


class Database:
    """
    Kelas untuk mengelola koneksi ke database SQLite.

    Menggunakan pola singleton-like connection agar hanya satu
    koneksi aktif selama program berjalan.

    External Library:
        sqlite3 — library bawaan Python untuk database SQLite.
    """

    def __init__(self, db_name: str = "kasir.db"):
        """
        Konstruktor Database. Membuka koneksi ke file SQLite.

        Args:
            db_name (str): Nama file database. Default 'kasir.db'.
        """
        self.conn   = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        Membuat tabel-tabel yang dibutuhkan jika belum ada.

        Tables:
            - produk
            - transaksi
            - detail_transaksi
        """

        # Tabel produk
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produk (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                nama  TEXT    NOT NULL,
                harga INTEGER NOT NULL,
                stok  INTEGER NOT NULL
            )
        """)

        # Tabel transaksi
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT    NOT NULL,
                total   INTEGER NOT NULL
            )
        """)

        # Tabel detail_transaksi (relasi ke transaksi dan produk)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detail_transaksi (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                transaksi_id  INTEGER NOT NULL,
                produk_id     INTEGER NOT NULL,
                jumlah        INTEGER NOT NULL,
                subtotal      INTEGER NOT NULL,
                FOREIGN KEY (transaksi_id) REFERENCES transaksi(id),
                FOREIGN KEY (produk_id)    REFERENCES produk(id)
            )
        """)

        self.conn.commit()

    def close(self):
        """Menutup koneksi database."""
        self.conn.close()