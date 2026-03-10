from model.product import Product
from repository.product_repository import ProductRepository


class ProductService:
    """
    Kelas service yang mengatur operasi CRUD produk.

    Memisahkan logika bisnis dari lapisan UI.
    """

    def __init__(self, db):
        """
        Konstruktor ProductService.

        Args:
            db: Instance Database.
        """
        self.repo = ProductRepository(db)

    def tambah_produk(self, nama: str, harga: int, stok: int) -> dict:
        """
        Validasi dan tambah produk baru.

        Args:
            nama  (str): Nama produk.
            harga (int): Harga produk.
            stok  (int): Stok produk.

        Returns:
            dict: {'success': bool, 'message': str}
        """
        if not nama.strip():
            return {"success": False, "message": "Nama produk tidak boleh kosong."}
        if harga <= 0:
            return {"success": False, "message": "Harga harus lebih dari 0."}
        if stok < 0:
            return {"success": False, "message": "Stok tidak boleh negatif."}

        product = Product(nama=nama.strip(), harga=harga, stok=stok)
        self.repo.add(product)
        return {"success": True, "message": f"Produk '{nama}' berhasil ditambahkan."}

    def update_produk(self, id: int, nama: str, harga: int, stok: int) -> dict:
        """
        Update data produk berdasarkan ID.

        Args:
            id    (int): ID produk.
            nama  (str): Nama baru.
            harga (int): Harga baru.
            stok  (int): Stok baru.

        Returns:
            dict: {'success': bool, 'message': str}
        """
        produk = self.repo.find_by_id(id)
        if produk is None:
            return {"success": False, "message": "Produk tidak ditemukan."}

        produk.nama  = nama.strip()
        produk.harga = harga
        produk.stok  = stok

        self.repo.update(produk)
        return {"success": True, "message": f"Produk ID {id} berhasil diupdate."}

    def hapus_produk(self, id: int) -> dict:
        """
        Hapus produk berdasarkan ID.

        Args:
            id (int): ID produk.

        Returns:
            dict: {'success': bool, 'message': str}
        """
        produk = self.repo.find_by_id(id)
        if produk is None:
            return {"success": False, "message": "Produk tidak ditemukan."}

        self.repo.delete(id)
        return {"success": True, "message": f"Produk '{produk.nama}' berhasil dihapus."}

    def get_semua_produk(self) -> list[Product]:
        """
        Ambil semua produk.

        Returns:
            list[Product]: Daftar produk.
        """
        return self.repo.find_all()

    def get_produk_by_id(self, id: int) -> Product | None:
        """
        Cari produk berdasarkan ID.

        Args:
            id (int): ID produk.

        Returns:
            Product | None
        """
        return self.repo.find_by_id(id)