from model.item import Item


class Product(Item):
    """
    Kelas Product mewarisi Item dan menambahkan atribut harga dan stok.

    Attributes:
        harga (int) : Harga satuan produk.
        stok  (int) : Jumlah stok tersedia.
    """

    def __init__(self, nama: str, harga: int, stok: int, id: int = None):
        """
        Konstruktor Product.

        Args:
            nama  (str) : Nama produk.
            harga (int) : Harga produk.
            stok  (int) : Stok produk.
            id    (int) : ID produk (opsional).
        """
        super().__init__(nama, id)   # panggil konstruktor parent (inheritance)
        self._harga = harga
        self._stok  = stok

    # ---------- properties ----------

    @property
    def harga(self) -> int:
        """Getter harga."""
        return self._harga

    @harga.setter
    def harga(self, value: int):
        """Setter harga."""
        if value < 0:
            raise ValueError("Harga tidak boleh negatif.")
        self._harga = value

    @property
    def stok(self) -> int:
        """Getter stok."""
        return self._stok

    @stok.setter
    def stok(self, value: int):
        """Setter stok."""
        if value < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self._stok = value

    # ---------- overloading / utility ----------

    def __repr__(self) -> str:
        """Override __repr__ (overloading method dari parent)."""
        return (
            f"Product(id={self._id}, nama='{self._nama}', "
            f"harga={self._harga}, stok={self._stok})"
        )

    def to_tuple(self) -> tuple:
        """
        Konversi objek ke tuple untuk keperluan insert DB.

        Returns:
            tuple: (nama, harga, stok)
        """
        return (self._nama, self._harga, self._stok)