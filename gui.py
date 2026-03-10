import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.database import Database
from service.product_service import ProductService
from service.transaction_service import TransactionService


# ================================================================
# COLOR PALETTE - Modern Light / Clean Professional
# ================================================================

C = {
    # Background
    "bg_root"    : "#f0f4f8",
    "bg_sidebar" : "#1e293b",
    "bg_white"   : "#ffffff",
    "bg_card"    : "#ffffff",
    "bg_input"   : "#f8fafc",
    "bg_header"  : "#1e293b",

    # Accent
    "accent"     : "#3b82f6",   # Biru utama
    "accent_dark": "#1d4ed8",   # Biru gelap (hover)
    "accent_light": "#eff6ff",  # Biru sangat muda (bg aktif)
    "success"    : "#10b981",   # Hijau
    "danger"     : "#ef4444",   # Merah
    "warning"    : "#f59e0b",   # Kuning
    "purple"     : "#8b5cf6",   # Ungu

    # Text
    "text_dark"  : "#0f172a",
    "text_body"  : "#334155",
    "text_dim"   : "#94a3b8",
    "text_white" : "#ffffff",
    "text_accent": "#3b82f6",

    # Border
    "border"     : "#e2e8f0",
    "border_dark": "#cbd5e1",
    "sidebar_active": "#3b82f6",
    "sidebar_text"  : "#94a3b8",
    "sidebar_hover" : "#334155",
}

# Font
F_TITLE  = ("Segoe UI", 20, "bold")
F_HEAD   = ("Segoe UI", 12, "bold")
F_SUB    = ("Segoe UI", 10)
F_BODY   = ("Segoe UI", 10)
F_SMALL  = ("Segoe UI", 9)
F_BTN    = ("Segoe UI", 10, "bold")
F_NUM    = ("Segoe UI", 24, "bold")


# ================================================================
# INIT
# ================================================================

db = Database()
db.create_tables()
product_service     = ProductService(db)
transaction_service = TransactionService(db)


# ================================================================
# ROOT
# ================================================================

root = tk.Tk()
root.title("Sistem Kasir")
root.geometry("1280x720")
root.minsize(1000, 600)
root.configure(bg=C["bg_root"])


# ================================================================
# TTK STYLE
# ================================================================

style = ttk.Style()
style.theme_use("clam")

style.configure("App.Treeview",
    background    = C["bg_white"],
    foreground    = C["text_body"],
    fieldbackground = C["bg_white"],
    borderwidth   = 0,
    rowheight     = 34,
    font          = F_BODY,
)
style.configure("App.Treeview.Heading",
    background    = C["bg_input"],
    foreground    = C["text_body"],
    borderwidth   = 0,
    font          = ("Segoe UI", 9, "bold"),
    relief        = "flat",
    padding       = 6,
)
style.map("App.Treeview",
    background    = [("selected", C["accent_light"])],
    foreground    = [("selected", C["accent"])],
)
style.map("App.Treeview.Heading",
    background    = [("active", C["border"])],
)
style.configure("TScrollbar",
    background    = C["border"],
    troughcolor   = C["bg_input"],
    borderwidth   = 0,
    arrowcolor    = C["text_dim"],
    relief        = "flat",
)


# ================================================================
# WIDGET HELPERS
# ================================================================

def fmt_rp(n: int) -> str:
    """Format integer ke string Rupiah."""
    return "Rp {:,}".format(n).replace(",", ".")


def entry(parent, w=28, **kw):
    """Entry dengan style modern."""
    e = tk.Entry(
        parent, width=w,
        bg=C["bg_input"], fg=C["text_dark"],
        insertbackground=C["accent"],
        relief="flat", font=F_BODY,
        highlightthickness=1,
        highlightbackground=C["border_dark"],
        highlightcolor=C["accent"],
        **kw
    )
    return e


def btn(parent, text, cmd, bg=None, fg=None, w=20, pad_y=7):
    """Button dengan style dan hover."""
    _bg = bg or C["accent"]
    _fg = fg or C["text_white"]
    b = tk.Button(
        parent, text=text, command=cmd,
        bg=_bg, fg=_fg,
        activebackground=C["accent_dark"],
        activeforeground=C["text_white"],
        font=F_BTN, relief="flat",
        cursor="hand2", width=w,
        pady=pad_y, bd=0,
    )
    b.bind("<Enter>", lambda e: b.config(bg=C["accent_dark"], fg=C["text_white"]))
    b.bind("<Leave>", lambda e: b.config(bg=_bg, fg=_fg))
    return b


def card_frame(parent, title="", **kw):
    """
    Buat frame card dengan border, shadow tipis, dan judul opsional.
    Return frame dalam (tempat isi konten).
    """
    outer = tk.Frame(parent, bg=C["border"], bd=0)
    inner = tk.Frame(outer, bg=C["bg_card"], **kw)
    inner.pack(fill="both", expand=True, padx=1, pady=1)

    if title:
        hdr = tk.Frame(inner, bg=C["bg_card"])
        hdr.pack(fill="x", padx=16, pady=(14, 0))
        tk.Label(hdr, text=title, font=F_HEAD,
                 fg=C["text_dark"], bg=C["bg_card"]).pack(side="left")
        tk.Frame(inner, bg=C["border"], height=1).pack(
            fill="x", padx=16, pady=(8, 0))

    return outer, inner


def label(parent, text, font=F_BODY, color=None, **kw):
    return tk.Label(parent, text=text, font=font,
                    fg=color or C["text_body"],
                    bg=parent.cget("bg"), **kw)


def section_title(parent, text):
    """Judul halaman besar."""
    tk.Label(parent, text=text, font=("Segoe UI", 16, "bold"),
             fg=C["text_dark"], bg=C["bg_root"]).pack(anchor="w")


def page_wrap(title, subtitle=""):
    """Buat container halaman standar, return frame isi."""
    clear_content()
    outer = tk.Frame(content, bg=C["bg_root"])
    outer.pack(fill="both", expand=True, padx=24, pady=20)
    tk.Label(outer, text=title, font=("Segoe UI", 16, "bold"),
             fg=C["text_dark"], bg=C["bg_root"]).pack(anchor="w")
    if subtitle:
        tk.Label(outer, text=subtitle, font=F_SMALL,
                 fg=C["text_dim"], bg=C["bg_root"]).pack(anchor="w", pady=(2, 12))
    else:
        tk.Frame(outer, bg=C["bg_root"], height=12).pack()
    return outer


# ================================================================
# LAYOUT UTAMA
# ================================================================

# --- Header ---
header_bar = tk.Frame(root, bg=C["bg_header"], height=54)
header_bar.pack(fill="x", side="top")
header_bar.pack_propagate(False)

tk.Label(header_bar, text="  Sistem Kasir",
         font=("Segoe UI", 15, "bold"),
         fg=C["text_white"], bg=C["bg_header"]).pack(side="left", padx=16, pady=12)

clock_lbl = tk.Label(header_bar, text="",
                      font=("Segoe UI", 9),
                      fg=C["sidebar_text"], bg=C["bg_header"])
clock_lbl.pack(side="right", padx=20)

tk.Label(header_bar, text="● Aktif",
         font=("Segoe UI", 9, "bold"),
         fg=C["success"], bg=C["bg_header"]).pack(side="right", padx=(0, 8))


def tick():
    clock_lbl.config(text=datetime.now().strftime("%A, %d %b %Y  |  %H:%M:%S"))
    root.after(1000, tick)

tick()

# Garis bawah header
tk.Frame(root, bg=C["accent"], height=2).pack(fill="x")

# --- Body ---
body = tk.Frame(root, bg=C["bg_root"])
body.pack(fill="both", expand=True)

# --- Sidebar ---
sidebar = tk.Frame(body, bg=C["bg_sidebar"], width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Frame(sidebar, bg=C["bg_sidebar"], height=16).pack()

# --- Content area ---
content = tk.Frame(body, bg=C["bg_root"])
content.pack(side="right", fill="both", expand=True)


def clear_content():
    for w in content.winfo_children():
        w.destroy()


# ================================================================
# SIDEBAR NAVIGATION
# ================================================================

_nav_buttons = []


def make_nav_btn(icon, label_text, cmd):
    """Buat tombol navigasi sidebar."""
    frm = tk.Frame(sidebar, bg=C["bg_sidebar"], cursor="hand2")
    frm.pack(fill="x", padx=10, pady=2)

    bar = tk.Frame(frm, bg=C["bg_sidebar"], width=4)
    bar.pack(side="left", fill="y")

    inner = tk.Frame(frm, bg=C["bg_sidebar"], padx=12, pady=11)
    inner.pack(side="left", fill="both", expand=True)

    ico_lbl = tk.Label(inner, text=icon, font=("Segoe UI", 13),
                       fg=C["sidebar_text"], bg=C["bg_sidebar"])
    ico_lbl.pack(side="left")

    txt_lbl = tk.Label(inner, text="  " + label_text, font=("Segoe UI", 10),
                       fg=C["sidebar_text"], bg=C["bg_sidebar"])
    txt_lbl.pack(side="left")

    parts = [frm, bar, inner, ico_lbl, txt_lbl]

    def activate():
        # Reset semua
        for item in _nav_buttons:
            item["bar"].config(bg=C["bg_sidebar"])
            item["inner"].config(bg=C["bg_sidebar"])
            item["ico"].config(fg=C["sidebar_text"], bg=C["bg_sidebar"])
            item["txt"].config(fg=C["sidebar_text"], bg=C["bg_sidebar"])
            item["frm"].config(bg=C["bg_sidebar"])
        # Set aktif
        bar.config(bg=C["accent"])
        inner.config(bg=C["sidebar_hover"])
        ico_lbl.config(fg=C["text_white"], bg=C["sidebar_hover"])
        txt_lbl.config(fg=C["text_white"], bg=C["sidebar_hover"])
        frm.config(bg=C["sidebar_hover"])
        cmd()

    for w in [frm, inner, ico_lbl, txt_lbl]:
        w.bind("<Button-1>", lambda e, a=activate: a())
        w.bind("<Enter>", lambda e, i=inner, ic=ico_lbl, t=txt_lbl, f=frm: (
            i.config(bg=C["sidebar_hover"]),
            ic.config(bg=C["sidebar_hover"], fg="#cbd5e1"),
            t.config(bg=C["sidebar_hover"], fg="#cbd5e1"),
            f.config(bg=C["sidebar_hover"]),
        ))
        w.bind("<Leave>", lambda e, i=inner, ic=ico_lbl, t=txt_lbl, f=frm: (
            i.config(bg=C["bg_sidebar"]),
            ic.config(bg=C["bg_sidebar"], fg=C["sidebar_text"]),
            t.config(bg=C["bg_sidebar"], fg=C["sidebar_text"]),
            f.config(bg=C["bg_sidebar"]),
        ))

    _nav_buttons.append({
        "frm": frm, "bar": bar, "inner": inner,
        "ico": ico_lbl, "txt": txt_lbl,
    })
    return activate


# ================================================================
# PAGE: DASHBOARD
# ================================================================

def show_dashboard():
    outer = page_wrap("Dashboard", "Ringkasan data sistem kasir")

    # Stat cards
    row = tk.Frame(outer, bg=C["bg_root"])
    row.pack(fill="x", pady=(0, 16))

    produk_list   = product_service.get_semua_produk()
    transaksi_list = transaction_service.get_semua_transaksi()
    revenue_total = sum(t.total for t in transaksi_list)
    stok_habis    = sum(1 for p in produk_list if p.stok == 0)

    stats = [
        ("Produk",         len(produk_list),       "#3b82f6", "📦"),
        ("Transaksi",      len(transaksi_list),     "#8b5cf6", "🧾"),
        ("Total Revenue",  fmt_rp(revenue_total),   "#10b981", "💰"),
        ("Stok Habis",     stok_habis,              "#ef4444", "⚠"),
    ]

    for title, val, color, icon in stats:
        o, i = card_frame(row, padx=20, pady=16)
        o.pack(side="left", expand=True, fill="both", padx=(0, 14))
        tk.Label(i, text=icon, font=("Segoe UI", 22),
                 bg=C["bg_card"]).pack(anchor="w")
        tk.Label(i, text=str(val),
                 font=("Segoe UI", 26, "bold"),
                 fg=color, bg=C["bg_card"]).pack(anchor="w")
        tk.Label(i, text=title, font=F_SMALL,
                 fg=C["text_dim"], bg=C["bg_card"]).pack(anchor="w")

    # Tabel produk
    o2, i2 = card_frame(outer, title="Daftar Produk", padx=0, pady=0)
    o2.pack(fill="both", expand=True)

    cols = ("ID", "Nama Produk", "Harga", "Stok", "Status")
    tree = ttk.Treeview(i2, columns=cols, show="headings",
                        style="App.Treeview", height=10)
    tree.heading("ID",          text="ID")
    tree.heading("Nama Produk", text="Nama Produk")
    tree.heading("Harga",       text="Harga")
    tree.heading("Stok",        text="Stok")
    tree.heading("Status",      text="Status")
    tree.column("ID",          width=50,  anchor="center")
    tree.column("Nama Produk", width=300)
    tree.column("Harga",       width=140, anchor="e")
    tree.column("Stok",        width=80,  anchor="center")
    tree.column("Status",      width=100, anchor="center")

    sc = ttk.Scrollbar(i2, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sc.set)
    tree.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(8, 16))
    sc.pack(side="right", fill="y", pady=(8, 16), padx=(0, 8))

    for p in produk_list:
        status = "Ada" if p.stok > 0 else "Habis"
        tree.insert("", tk.END,
                    values=(p.id, p.nama, fmt_rp(p.harga), p.stok, status))


# ================================================================
# PAGE: KELOLA PRODUK
# ================================================================

def show_produk():
    outer = page_wrap("Kelola Produk", "Tambah, edit, dan hapus data produk")

    split = tk.Frame(outer, bg=C["bg_root"])
    split.pack(fill="both", expand=True)

    # ============ FORM KIRI ============
    o_f, i_f = card_frame(split, title="Form Produk", padx=18, pady=14)
    o_f.pack(side="left", fill="y", padx=(0, 14))

    fields = {}
    field_defs = [
        ("id",    "ID  (untuk edit / hapus)"),
        ("nama",  "Nama Produk"),
        ("harga", "Harga  (Rp)"),
        ("stok",  "Stok"),
    ]
    for key, lbl_text in field_defs:
        tk.Label(i_f, text=lbl_text, font=F_SMALL,
                 fg=C["text_dim"], bg=C["bg_card"]).pack(anchor="w", pady=(10, 2))
        e = entry(i_f, w=28)
        e.pack(fill="x", ipady=5)
        fields[key] = e

    tk.Frame(i_f, bg=C["border"], height=1).pack(fill="x", pady=14)

    def _get():
        return (fields["id"].get().strip(),
                fields["nama"].get().strip(),
                fields["harga"].get().strip(),
                fields["stok"].get().strip())

    def _clear():
        for e in fields.values():
            e.delete(0, tk.END)

    def _tambah():
        _, nama, harga, stok = _get()
        try:
            r = product_service.tambah_produk(nama, int(harga), int(stok))
            if r["success"]:
                _clear()
                _refresh()
                messagebox.showinfo("Sukses", r["message"])
            else:
                messagebox.showerror("Error", r["message"])
        except ValueError:
            messagebox.showerror("Error", "Harga dan stok harus berupa angka.")

    def _update():
        id_v, nama, harga, stok = _get()
        try:
            r = product_service.update_produk(int(id_v), nama, int(harga), int(stok))
            if r["success"]:
                _clear()
                _refresh()
                messagebox.showinfo("Sukses", r["message"])
            else:
                messagebox.showerror("Error", r["message"])
        except ValueError:
            messagebox.showerror("Error", "ID, Harga, dan Stok harus berupa angka.")

    def _hapus():
        id_v, *_ = _get()
        try:
            if messagebox.askyesno("Konfirmasi", f"Hapus produk ID {id_v}?"):
                r = product_service.hapus_produk(int(id_v))
                if r["success"]:
                    _clear()
                    _refresh()
                    messagebox.showinfo("Sukses", r["message"])
                else:
                    messagebox.showerror("Error", r["message"])
        except ValueError:
            messagebox.showerror("Error", "Isi ID dengan angka.")

    btn_defs = [
        ("+ Tambah Produk",  _tambah, C["accent"],   C["text_white"]),
        ("  Edit / Update",  _update, C["purple"],    C["text_white"]),
        ("  Hapus Produk",   _hapus,  C["danger"],    C["text_white"]),
        ("  Reset Form",     _clear,  C["border_dark"], C["text_body"]),
    ]
    for txt, cmd, bg, fg in btn_defs:
        b = btn(i_f, txt, cmd, bg=bg, fg=fg, w=26)
        b.pack(fill="x", pady=3)

    # ============ TABEL KANAN ============
    o_t, i_t = card_frame(split, title="Daftar Produk", padx=0, pady=0)
    o_t.pack(side="left", fill="both", expand=True)

    # Search
    s_row = tk.Frame(i_t, bg=C["bg_card"])
    s_row.pack(fill="x", padx=16, pady=(12, 8))
    tk.Label(s_row, text="Cari:", font=F_SMALL,
             fg=C["text_dim"], bg=C["bg_card"]).pack(side="left", padx=(0, 6))
    e_search = entry(s_row, w=32)
    e_search.pack(side="left", fill="x", expand=True, ipady=4)

    cols = ("ID", "Nama Produk", "Harga", "Stok")
    tree = ttk.Treeview(i_t, columns=cols, show="headings",
                        style="App.Treeview", height=18)
    tree.heading("ID",          text="ID")
    tree.heading("Nama Produk", text="Nama Produk")
    tree.heading("Harga",       text="Harga")
    tree.heading("Stok",        text="Stok")
    tree.column("ID",          width=50,  anchor="center")
    tree.column("Nama Produk", width=280)
    tree.column("Harga",       width=140, anchor="e")
    tree.column("Stok",        width=80,  anchor="center")

    sc2 = ttk.Scrollbar(i_t, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sc2.set)
    tree.pack(side="left", fill="both", expand=True,
              padx=(16, 0), pady=(0, 16))
    sc2.pack(side="right", fill="y", pady=(0, 16), padx=(0, 8))

    def _refresh(keyword=""):
        for r in tree.get_children():
            tree.delete(r)
        for p in product_service.get_semua_produk():
            if keyword.lower() in p.nama.lower():
                tree.insert("", tk.END,
                            values=(p.id, p.nama, fmt_rp(p.harga), p.stok))

    e_search.bind("<KeyRelease>", lambda e: _refresh(e_search.get()))

    def _on_select(event):
        sel = tree.focus()
        if not sel:
            return
        vals = tree.item(sel)["values"]
        # vals = (id, nama, "Rp X.XXX", stok)
        mapping = {
            "id":    str(vals[0]),
            "nama":  str(vals[1]),
            "harga": str(vals[2]).replace("Rp ", "").replace(".", ""),
            "stok":  str(vals[3]),
        }
        for k, v in mapping.items():
            fields[k].delete(0, tk.END)
            fields[k].insert(0, v)

    tree.bind("<<TreeviewSelect>>", _on_select)
    _refresh()


# ================================================================
# PAGE: TRANSAKSI
# ================================================================

def show_transaksi():
    transaction_service.reset_cart()
    clear_content()

    # ── Satu Canvas besar, scroll seluruh halaman ──────────────
    canvas = tk.Canvas(content, bg=C["bg_root"], highlightthickness=0)
    vsb    = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    page     = tk.Frame(canvas, bg=C["bg_root"])
    page_win = canvas.create_window((0, 0), window=page, anchor="nw")

    page.bind("<Configure>",
              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfig(page_win, width=e.width))

    def _scroll(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    canvas.bind("<MouseWheel>", _scroll)
    page.bind(  "<MouseWheel>", _scroll)

    # ── Judul ──────────────────────────────────────────────────
    hdr = tk.Frame(page, bg=C["bg_root"])
    hdr.pack(fill="x", padx=24, pady=(20, 4))
    hdr.bind("<MouseWheel>", _scroll)
    tk.Label(hdr, text="Transaksi Penjualan",
             font=("Segoe UI", 16, "bold"),
             fg=C["text_dark"], bg=C["bg_root"]).pack(anchor="w")
    tk.Label(hdr, text="Proses penjualan dan pembayaran",
             font=F_SMALL, fg=C["text_dim"], bg=C["bg_root"]).pack(anchor="w")

    wrap = tk.Frame(page, bg=C["bg_root"])
    wrap.pack(fill="both", expand=True, padx=24, pady=(8, 24))
    wrap.bind("<MouseWheel>", _scroll)

    # ╔══════════════════════════════════════════════════════════╗
    # ║  BARIS 1 — Produk Tersedia (kiri) | Keranjang (kanan)   ║
    # ╚══════════════════════════════════════════════════════════╝
    top_row = tk.Frame(wrap, bg=C["bg_root"])
    top_row.pack(fill="x", pady=(0, 14))
    top_row.bind("<MouseWheel>", _scroll)

    # ── Produk Tersedia ───────────────────────────────────────
    o1, i1 = card_frame(top_row, title="Produk Tersedia", padx=0, pady=0)
    o1.pack(side="left", fill="both", expand=True, padx=(0, 10))
    i1.bind("<MouseWheel>", _scroll)

    cols_p   = ("ID", "Nama Produk", "Harga", "Stok")
    t_produk = ttk.Treeview(i1, columns=cols_p, show="headings",
                             style="App.Treeview", height=10)
    t_produk.heading("ID",          text="ID")
    t_produk.heading("Nama Produk", text="Nama Produk")
    t_produk.heading("Harga",       text="Harga")
    t_produk.heading("Stok",        text="Stok")
    t_produk.column("ID",          width=45,  anchor="center")
    t_produk.column("Nama Produk", width=220)
    t_produk.column("Harga",       width=110, anchor="e")
    t_produk.column("Stok",        width=60,  anchor="center")

    sc_p = ttk.Scrollbar(i1, orient="vertical", command=t_produk.yview)
    t_produk.configure(yscrollcommand=sc_p.set)
    t_produk.pack(side="left", fill="both", expand=True,
                  padx=(14, 0), pady=(8, 14))
    sc_p.pack(side="right", fill="y", pady=(8, 14), padx=(0, 6))
    t_produk.bind("<MouseWheel>", lambda e: "break")

    def _refresh_produk():
        for r in t_produk.get_children():
            t_produk.delete(r)
        for p in product_service.get_semua_produk():
            t_produk.insert("", tk.END,
                            values=(p.id, p.nama, fmt_rp(p.harga), p.stok))

    _refresh_produk()

    # ── Keranjang Belanja ─────────────────────────────────────
    o2, i2 = card_frame(top_row, title="Keranjang Belanja", padx=0, pady=0)
    o2.pack(side="left", fill="both", expand=True)
    i2.bind("<MouseWheel>", _scroll)

    cols_c = ("Produk", "Qty", "Subtotal")
    t_cart  = ttk.Treeview(i2, columns=cols_c, show="headings",
                            style="App.Treeview", height=10)
    t_cart.heading("Produk",   text="Produk")
    t_cart.heading("Qty",      text="Qty")
    t_cart.heading("Subtotal", text="Subtotal")
    t_cart.column("Produk",   width=190)
    t_cart.column("Qty",      width=50,  anchor="center")
    t_cart.column("Subtotal", width=110, anchor="e")

    sc_c = ttk.Scrollbar(i2, orient="vertical", command=t_cart.yview)
    t_cart.configure(yscrollcommand=sc_c.set)
    t_cart.pack(side="left", fill="both", expand=True,
                padx=(14, 0), pady=(8, 0))
    sc_c.pack(side="right", fill="y", pady=(8, 0), padx=(0, 6))
    t_cart.bind("<MouseWheel>", lambda e: "break")

    # Total strip di bawah tabel keranjang
    total_strip = tk.Frame(i2, bg=C["accent_light"], pady=10, padx=14)
    total_strip.pack(fill="x", pady=(8, 14), padx=14)
    total_strip.bind("<MouseWheel>", _scroll)
    tk.Label(total_strip, text="TOTAL BELANJA",
             font=("Segoe UI", 8, "bold"),
             fg=C["accent"], bg=C["accent_light"]).pack(side="left")
    lbl_total = tk.Label(total_strip, text="Rp 0",
                          font=("Segoe UI", 16, "bold"),
                          fg=C["accent"], bg=C["accent_light"])
    lbl_total.pack(side="right")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  BARIS 2 — Tambah ke Keranjang (penuh)                  ║
    # ╚══════════════════════════════════════════════════════════╝
    o3, i3 = card_frame(wrap, title="Tambah ke Keranjang", padx=18, pady=16)
    o3.pack(fill="x", pady=(0, 14))
    i3.bind("<MouseWheel>", _scroll)

    row_f = tk.Frame(i3, bg=C["bg_card"])
    row_f.pack(fill="x")
    row_f.bind("<MouseWheel>", _scroll)

    tk.Label(row_f, text="ID Produk", font=F_SMALL,
             fg=C["text_dim"], bg=C["bg_card"]).grid(
             row=0, column=0, sticky="w", padx=(0, 4))
    e_id = entry(row_f, w=14)
    e_id.grid(row=1, column=0, padx=(0, 16), ipady=6, sticky="w")

    tk.Label(row_f, text="Jumlah", font=F_SMALL,
             fg=C["text_dim"], bg=C["bg_card"]).grid(
             row=0, column=1, sticky="w", padx=(0, 4))
    e_qty = entry(row_f, w=14)
    e_qty.grid(row=1, column=1, padx=(0, 16), ipady=6, sticky="w")

    def _tambah_cart():
        try:
            id_p   = int(e_id.get())
            jumlah = int(e_qty.get())
        except ValueError:
            messagebox.showerror("Error", "ID dan jumlah harus angka.")
            return
        r = transaction_service.tambah_ke_cart(id_p, jumlah)
        if r["success"]:
            d = r["detail"]
            t_cart.insert("", tk.END,
                          values=(d.nama, d.jumlah, fmt_rp(d.subtotal)))
            t_cart.yview_moveto(1)
            e_id.delete(0, tk.END)
            e_qty.delete(0, tk.END)
            lbl_total.config(text=fmt_rp(transaction_service.get_total()))
            _refresh_produk()
            _update_kembalian()
        else:
            messagebox.showerror("Error", r["message"])

    def _pilih_produk(event):
        sel = t_produk.focus()
        if sel:
            val = t_produk.item(sel)["values"]
            e_id.delete(0, tk.END)
            e_id.insert(0, val[0])
            e_qty.focus()

    t_produk.bind("<<TreeviewSelect>>", _pilih_produk)

    btn(row_f, "+ Tambah ke Keranjang", _tambah_cart,
        bg=C["accent"], fg=C["text_white"], w=22).grid(
        row=1, column=2, ipady=5, sticky="w")

    # ╔══════════════════════════════════════════════════════════╗
    # ║  BARIS 3 — Pembayaran (penuh)                           ║
    # ╚══════════════════════════════════════════════════════════╝
    o4, i4 = card_frame(wrap, title="Pembayaran", padx=18, pady=16)
    o4.pack(fill="x", pady=(0, 14))
    i4.bind("<MouseWheel>", _scroll)

    pay_row = tk.Frame(i4, bg=C["bg_card"])
    pay_row.pack(fill="x")
    pay_row.bind("<MouseWheel>", _scroll)

    # Kolom input bayar
    col_a = tk.Frame(pay_row, bg=C["bg_card"])
    col_a.pack(side="left", padx=(0, 20))
    col_a.bind("<MouseWheel>", _scroll)
    tk.Label(col_a, text="Uang Bayar (Rp)", font=F_SMALL,
             fg=C["text_dim"], bg=C["bg_card"]).pack(anchor="w", pady=(0, 3))
    e_bayar = entry(col_a, w=22)
    e_bayar.pack(ipady=7)

    # Kolom preview kembalian
    col_b = tk.Frame(pay_row, bg="#f0fdf4", padx=20, pady=12)
    col_b.pack(side="left", padx=(0, 20))
    col_b.bind("<MouseWheel>", _scroll)
    tk.Label(col_b, text="KEMBALIAN",
             font=("Segoe UI", 8, "bold"),
             fg=C["success"], bg="#f0fdf4").pack(anchor="w")
    lbl_kem = tk.Label(col_b, text="Rp 0",
                        font=("Segoe UI", 20, "bold"),
                        fg=C["success"], bg="#f0fdf4")
    lbl_kem.pack(anchor="w")

    def _update_kembalian(*args):
        try:
            bayar = int(e_bayar.get())
            kem   = bayar - transaction_service.get_total()
            lbl_kem.config(
                text=fmt_rp(max(kem, 0)),
                fg=C["success"] if kem >= 0 else C["danger"])
        except ValueError:
            lbl_kem.config(text="Rp 0", fg=C["success"])

    e_bayar.bind("<KeyRelease>", _update_kembalian)

    # Kolom tombol
    col_c = tk.Frame(pay_row, bg=C["bg_card"])
    col_c.pack(side="left")
    col_c.bind("<MouseWheel>", _scroll)

    def _proses_bayar():
        try:
            bayar = int(e_bayar.get())
        except ValueError:
            messagebox.showerror("Error", "Uang bayar harus angka.")
            return
        r = transaction_service.proses_bayar(bayar)
        if r["success"]:
            messagebox.showinfo("Transaksi Berhasil",
                                f"Kembalian: {fmt_rp(r['kembalian'])}")
            for row in t_cart.get_children():
                t_cart.delete(row)
            lbl_total.config(text="Rp 0")
            lbl_kem.config(text="Rp 0")
            e_bayar.delete(0, tk.END)
            _refresh_produk()
        else:
            messagebox.showerror("Error", r["message"])

    def _batal():
        transaction_service.reset_cart()
        for row in t_cart.get_children():
            t_cart.delete(row)
        lbl_total.config(text="Rp 0")
        lbl_kem.config(text="Rp 0")
        e_bayar.delete(0, tk.END)
        _refresh_produk()

    btn(col_c, "  Proses Pembayaran  ", _proses_bayar,
        bg=C["success"], fg=C["text_white"], w=22).pack(pady=(0, 6))
    btn(col_c, "  Batalkan Transaksi  ", _batal,
        bg=C["border_dark"], fg=C["text_body"], w=22).pack()


def show_history():
    outer = page_wrap("Riwayat Transaksi", "Histori seluruh transaksi penjualan")

    o, i = card_frame(outer, title="Semua Transaksi", padx=0, pady=0)
    o.pack(fill="both", expand=True)

    cols = ("ID", "Tanggal & Waktu", "Total")
    tree = ttk.Treeview(i, columns=cols, show="headings",
                        style="App.Treeview")
    tree.heading("ID",              text="ID")
    tree.heading("Tanggal & Waktu", text="Tanggal & Waktu")
    tree.heading("Total",           text="Total")
    tree.column("ID",              width=60,  anchor="center")
    tree.column("Tanggal & Waktu", width=280)
    tree.column("Total",           width=180, anchor="e")

    sc = ttk.Scrollbar(i, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sc.set)
    tree.pack(side="left", fill="both", expand=True,
              padx=(16, 0), pady=(8, 0))
    sc.pack(side="right", fill="y", pady=(8, 0), padx=(0, 8))

    semua = transaction_service.get_semua_transaksi()
    idx = 0
    while idx < len(semua):
        t = semua[idx]
        tree.insert("", tk.END,
                    values=(t.id, t.tanggal, fmt_rp(t.total)))
        idx += 1

    # Summary footer
    if semua:
        grand = sum(t.total for t in semua)
        footer = tk.Frame(i, bg=C["accent_light"], pady=10, padx=16)
        footer.pack(fill="x", pady=(10, 12), padx=16)
        tk.Label(footer,
                 text=f"{len(semua)} transaksi   |   Grand Total: {fmt_rp(grand)}",
                 font=("Segoe UI", 10, "bold"),
                 fg=C["accent"], bg=C["accent_light"]).pack(side="right")


# ================================================================
# BUILD SIDEBAR
# ================================================================

tk.Label(sidebar, text="MENU", font=("Segoe UI", 8, "bold"),
         fg=C["sidebar_text"], bg=C["bg_sidebar"]).pack(
         anchor="w", padx=22, pady=(8, 6))

nav_defs = [
    ("◈", "Dashboard",  show_dashboard),
    ("⊞", "Produk",     show_produk),
    ("⊙", "Transaksi",  show_transaksi),
    ("≡", "Riwayat",    show_history),
]

activators = []
for icon, label_text, cmd in nav_defs:
    act = make_nav_btn(icon, label_text, cmd)
    activators.append(act)

# Sidebar footer
tk.Frame(sidebar, bg=C["bg_sidebar"]).pack(fill="both", expand=True)
tk.Frame(sidebar, bg=C["sidebar_hover"], height=1).pack(fill="x")
tk.Label(sidebar, text="v2.0  Sistem Kasir",
         font=("Segoe UI", 8),
         fg=C["sidebar_text"], bg=C["bg_sidebar"]).pack(pady=10)


# ================================================================
# START
# ================================================================

activators[0]()  # Buka Dashboard
root.mainloop()