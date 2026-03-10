class TransactionDetail:
    """
    Merepresentasikan satu baris item dalam sebuah transaksi.

    Attributes:
        produk_id (int) : ID produk.
        nama      (str) : Nama produk (untuk tampilan).
        jumlah    (int) : Jumlah produk dibeli.
        subtotal  (int) : Harga * jumlah.
    """

    def __init__(self, produk_id: int, nama: str, jumlah: int, subtotal: int):
        self.produk_id = produk_id
        self.nama      = nama
        self.jumlah    = jumlah
        self.subtotal  = subtotal

    def __repr__(self) -> str:
        return (
            f"Detail(produk_id={self.produk_id}, nama='{self.nama}', "
            f"jumlah={self.jumlah}, subtotal={self.subtotal})"
        )


class Transaction:
    """
    Merepresentasikan sebuah transaksi penjualan.

    Attributes:
        id      (int)              : ID transaksi.
        tanggal (str)              : Tanggal dan waktu transaksi.
        total   (int)              : Total harga transaksi.
        details (list)             : Daftar TransactionDetail.
    """

    def __init__(self, tanggal: str, total: int, id: int = None):
        self._id      = id
        self._tanggal = tanggal
        self._total   = total
        self.details: list[TransactionDetail] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def tanggal(self) -> str:
        return self._tanggal

    @property
    def total(self) -> int:
        return self._total

    def tambah_detail(self, detail: TransactionDetail):
        """Tambahkan item ke daftar detail transaksi."""
        self.details.append(detail)

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self._id}, tanggal='{self._tanggal}', "
            f"total={self._total})"
        )