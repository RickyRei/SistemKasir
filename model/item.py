class Item:
    """
    Kelas dasar (parent) yang merepresentasikan sebuah item.

    Attributes:
        id   (int) : ID unik item dari database.
        nama (str) : Nama item.
    """

    def __init__(self, nama: str, id: int = None):
        """
        Konstruktor Item.

        Args:
            nama (str) : Nama item.
            id   (int) : ID item (opsional, diisi otomatis dari DB).
        """
        self._id   = id    # private, akses via property
        self._nama = nama  # private, akses via property

    # ---------- properties ----------

    @property
    def id(self) -> int:
        """Getter id."""
        return self._id

    @id.setter
    def id(self, value: int):
        """Setter id."""
        self._id = value

    @property
    def nama(self) -> str:
        """Getter nama."""
        return self._nama

    @nama.setter
    def nama(self, value: str):
        """Setter nama."""
        if not value:
            raise ValueError("Nama tidak boleh kosong.")
        self._nama = value

    def __repr__(self) -> str:
        return f"Item(id={self._id}, nama='{self._nama}')"