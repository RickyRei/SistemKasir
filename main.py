from database.database import Database
from service.product_service import ProductService
from service.transaction_service import TransactionService


def cetak_garis():
    """Cetak garis pemisah."""
    print("-" * 40)


def menu_produk(product_service: ProductService):
    """
    Sub-menu pengelolaan produk.

    Args:
        product_service (ProductService): Service produk.
    """
    while True:
        print("\n===== KELOLA PRODUK =====")
        print("1. Tambah Produk")
        print("2. Lihat Semua Produk")
        print("3. Update Produk")
        print("4. Hapus Produk")
        print("5. Kembali")
        cetak_garis()

        pilih = input("Pilih menu: ")

        if pilih == "1":
            nama  = input("Nama produk : ")
            harga = int(input("Harga       : "))
            stok  = int(input("Stok        : "))
            hasil = product_service.tambah_produk(nama, harga, stok)
            print(hasil["message"])

        elif pilih == "2":
            produk_list = product_service.get_semua_produk()
            if not produk_list:
                print("Belum ada produk.")
            else:
                print(f"\n{'ID':<5} {'Nama':<25} {'Harga':>12} {'Stok':>6}")
                cetak_garis()
                # for loop untuk iterasi list produk (Array)
                for p in produk_list:
                    print(f"{p.id:<5} {p.nama:<25} {p.harga:>12,} {p.stok:>6}")

        elif pilih == "3":
            id_p  = int(input("ID produk   : "))
            nama  = input("Nama baru   : ")
            harga = int(input("Harga baru  : "))
            stok  = int(input("Stok baru   : "))
            hasil = product_service.update_produk(id_p, nama, harga, stok)
            print(hasil["message"])

        elif pilih == "4":
            id_p  = int(input("ID produk yang dihapus: "))
            hasil = product_service.hapus_produk(id_p)
            print(hasil["message"])

        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid.")


def menu_transaksi(transaction_service: TransactionService):
    """
    Sub-menu transaksi penjualan.

    Args:
        transaction_service (TransactionService): Service transaksi.
    """
    transaction_service.reset_cart()

    while True:
        print("\n===== TRANSAKSI =====")
        print("1. Pilih Produk")
        print("2. Lihat Keranjang")
        print("3. Proses Pembayaran")
        print("4. Batal / Kembali")
        cetak_garis()

        pilih = input("Pilih: ")

        if pilih == "1":
            # Tampilkan produk
            produk_list = transaction_service.get_semua_produk()
            print(f"\n{'ID':<5} {'Nama':<25} {'Harga':>12} {'Stok':>6}")
            cetak_garis()
            for p in produk_list:
                print(f"{p.id:<5} {p.nama:<25} {p.harga:>12,} {p.stok:>6}")

            id_p   = int(input("\nID Produk : "))
            jumlah = int(input("Jumlah    : "))

            hasil = transaction_service.tambah_ke_cart(id_p, jumlah)
            print(hasil["message"])

        elif pilih == "2":
            cart = transaction_service.get_cart()
            if not cart:
                print("Keranjang kosong.")
            else:
                print(f"\n{'Produk':<25} {'Jumlah':>8} {'Subtotal':>14}")
                cetak_garis()
                for item in cart:
                    print(f"{item.nama:<25} {item.jumlah:>8} {item.subtotal:>14,}")
                print(f"\nTotal: Rp {transaction_service.get_total():,}")

        elif pilih == "3":
            if not transaction_service.get_cart():
                print("Keranjang masih kosong.")
                continue

            print(f"Total belanja: Rp {transaction_service.get_total():,}")
            bayar = int(input("Uang bayar  : Rp "))

            hasil = transaction_service.proses_bayar(bayar)
            print(hasil["message"])

            if hasil["success"]:
                print(f"Kembalian   : Rp {hasil['kembalian']:,}")
                break

        elif pilih == "4":
            transaction_service.reset_cart()
            break
        else:
            print("Pilihan tidak valid.")


def menu_histori(transaction_service: TransactionService):
    """
    Tampilkan riwayat transaksi.

    Args:
        transaction_service (TransactionService): Service transaksi.
    """
    semua = transaction_service.get_semua_transaksi()

    if not semua:
        print("\nBelum ada transaksi.")
        return

    print(f"\n{'ID':<5} {'Tanggal':<22} {'Total':>14}")
    cetak_garis()
    for t in semua:
        print(f"{t.id:<5} {t.tanggal:<22} {t.total:>14,}")


def main():
    """Fungsi utama — menjalankan program mode console."""

    db = Database()
    db.create_tables()

    product_service     = ProductService(db)
    transaction_service = TransactionService(db)

    while True:
        print("\n===== SISTEM KASIR =====")
        print("1. Kelola Produk")
        print("2. Transaksi Penjualan")
        print("3. Riwayat Transaksi")
        print("4. Keluar")
        cetak_garis()

        pilih = input("Pilih menu: ")

        if pilih == "1":
            menu_produk(product_service)

        elif pilih == "2":
            menu_transaksi(transaction_service)

        elif pilih == "3":
            menu_histori(transaction_service)

        elif pilih == "4":
            print("Terima kasih. Program selesai.")
            db.close()
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()