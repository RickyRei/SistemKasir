from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Interface Repository — mendefinisikan kontrak CRUD
    yang harus diimplementasikan oleh semua repository.

    Menerapkan:
        - Interface  : kelas ABC dengan @abstractmethod
        - Polymorphism: ProductRepository dan TransactionRepository
                        mengimplementasikan interface yang sama
    """

    @abstractmethod
    def add(self, data) -> None:
        """Tambah data baru ke database."""
        pass

    @abstractmethod
    def update(self, data) -> None:
        """Update data yang sudah ada."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Hapus data berdasarkan ID."""
        pass

    @abstractmethod
    def find_by_id(self, id: int):
        """Cari satu data berdasarkan ID."""
        pass

    @abstractmethod
    def find_all(self) -> list:
        """Ambil semua data."""
        pass