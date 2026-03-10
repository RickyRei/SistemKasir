from datetime import datetime
from model.transaction import Transaction, TransactionDetail
from repository.product_repository import ProductRepository
from repository.transaction_repository import TransactionRepository


class TransactionService:
    """
    Kelas service yang mengatur alur proses transaksi.

    Memisahkan logika bisnis dari lapisan UI dan repository.
    """

    def __init__(self, db):
        """
        Konstruktor TransactionService.

        Args:
            db: Instance Database.
        """
        self.product_repo     = ProductRepository(db)
        self.transaction_repo = TransactionRepository(db)

        # Cart disimpan sebagai list of TransactionDetail (Array)
        self._cart: list[TransactionDetail] = []
        self._total: int = 0

    # -------------------------------------------------------
    # CART MANAGEMENT
    # -------------------------------------------------------

    def reset_cart(self):
        """Reset keranjang belanja untuk transaksi baru."""
        self._cart  = []
        self._total = 0

    def get_cart(self) -> list[TransactionDetail]:
        """
        Ambil isi keranjang belanja saat ini.

        Returns:
            list[TransactionDetail]: Daftar item di keranjang.
        """
        return self._cart

    def get_total(self) -> int:
        """
        Ambil total harga transaksi saat ini.

        Returns:
            int: Total harga.
        """
        return self._total

    def tambah_ke_cart(self, id_produk: int, jumlah: int) -> dict:
        """
        Tambah produk ke keranjang belanja.

        Args:
            id_produk (int): ID produk yang dipilih.
            jumlah    (int): Jumlah yang dibeli.

        Returns:
            dict: {'success': bool, 'message': str, 'detail': TransactionDetail|None}
        """
        produk = self.product_repo.find_by_id(id_produk)

        # Percabangan if-else untuk validasi
        if produk is None:
            return {"success": False, "message": "Produk tidak ditemukan.", "detail": None}

        if jumlah <= 0:
            return {"success": False, "message": "Jumlah harus lebih dari 0.", "detail": None}

        if jumlah > produk.stok:
            return {"success": False, "message": f"Stok tidak cukup. Stok tersedia: {produk.stok}.", "detail": None}

        subtotal = produk.harga * jumlah
        self._total += subtotal

        detail = TransactionDetail(
            produk_id=produk.id,
            nama=produk.nama,
            jumlah=jumlah,
            subtotal=subtotal
        )
        self._cart.append(detail)

        return {"success": True, "message": "Berhasil ditambahkan.", "detail": detail}

    def proses_bayar(self, bayar: int) -> dict:
        """
        Proses pembayaran dan simpan transaksi ke database.

        Args:
            bayar (int): Uang yang dibayarkan pelanggan.

        Returns:
            dict: {'success': bool, 'message': str, 'kembalian': int}
        """
        if not self._cart:
            return {"success": False, "message": "Keranjang kosong.", "kembalian": 0}

        if bayar < self._total:
            return {"success": False, "message": "Uang tidak cukup.", "kembalian": 0}

        kembalian = bayar - self._total

        # Buat objek Transaction
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trx = Transaction(tanggal=tanggal, total=self._total)

        # Iterasi cart dengan for loop, simpan detail dan kurangi stok
        for detail in self._cart:
            trx.tambah_detail(detail)
            self.product_repo.kurangi_stok(detail.produk_id, detail.jumlah)

        # Simpan ke DB
        self.transaction_repo.add(trx)

        # Reset cart setelah transaksi berhasil
        self.reset_cart()

        return {
            "success"  : True,
            "message"  : "Transaksi berhasil!",
            "kembalian": kembalian
        }

    # -------------------------------------------------------
    # READ DATA
    # -------------------------------------------------------

    def get_semua_produk(self):
        """Ambil semua produk dari repository."""
        return self.product_repo.find_all()

    def get_semua_transaksi(self):
        """Ambil semua transaksi dari repository."""
        return self.transaction_repo.find_all()

    def get_detail_transaksi(self, id_transaksi: int) -> Transaction | None:
        """
        Ambil detail sebuah transaksi.

        Args:
            id_transaksi (int): ID transaksi.

        Returns:
            Transaction | None
        """
        return self.transaction_repo.find_by_id(id_transaksi)

    def hitung_kembalian(self, bayar: int) -> int:
        """
        Hitung kembalian tanpa memproses transaksi.

        Args:
            bayar (int): Uang yang dibayarkan.

        Returns:
            int: Nominal kembalian.
        """
        return bayar - self._total