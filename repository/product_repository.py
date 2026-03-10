from repository.repository import Repository
from model.product import Product


class ProductRepository(Repository):
    """
    Implementasi Repository untuk tabel 'produk'.

    Semua operasi CRUD terhadap data produk dilakukan di sini.
    Menerapkan interface Repository → polymorphism.
    """

    def __init__(self, db):
        """
        Konstruktor ProductRepository.

        Args:
            db: Instance Database (dependency injection).
        """
        self.db = db

    def add(self, product: Product) -> None:
        """
        Tambah produk baru ke database.

        Args:
            product (Product): Objek produk yang akan disimpan.
        """
        self.db.cursor.execute(
            "INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)",
            (product.nama, product.harga, product.stok)
        )
        self.db.conn.commit()

    def update(self, product: Product) -> None:
        """
        Update data produk berdasarkan ID.

        Args:
            product (Product): Objek produk dengan data baru.
        """
        self.db.cursor.execute(
            "UPDATE produk SET nama=?, harga=?, stok=? WHERE id=?",
            (product.nama, product.harga, product.stok, product.id)
        )
        self.db.conn.commit()

    def delete(self, id: int) -> None:
        """
        Hapus produk berdasarkan ID.

        Args:
            id (int): ID produk yang akan dihapus.
        """
        self.db.cursor.execute("DELETE FROM produk WHERE id=?", (id,))
        self.db.conn.commit()

    def find_by_id(self, id: int) -> Product | None:
        """
        Cari produk berdasarkan ID.

        Args:
            id (int): ID produk.

        Returns:
            Product | None: Objek Product atau None jika tidak ditemukan.
        """
        self.db.cursor.execute("SELECT * FROM produk WHERE id=?", (id,))
        row = self.db.cursor.fetchone()
        if row is None:
            return None
        return Product(id=row[0], nama=row[1], harga=row[2], stok=row[3])

    def find_all(self) -> list[Product]:
        """
        Ambil semua data produk dari database.

        Returns:
            list[Product]: Daftar objek Product.
        """
        self.db.cursor.execute("SELECT * FROM produk ORDER BY id")
        rows = self.db.cursor.fetchall()
        return [Product(id=r[0], nama=r[1], harga=r[2], stok=r[3]) for r in rows]

    def kurangi_stok(self, id: int, jumlah: int) -> None:
        """
        Kurangi stok produk sejumlah yang dibeli.

        Args:
            id     (int): ID produk.
            jumlah (int): Jumlah yang dikurangi.
        """
        self.db.cursor.execute(
            "UPDATE produk SET stok = stok - ? WHERE id=?",
            (jumlah, id)
        )
        self.db.conn.commit()