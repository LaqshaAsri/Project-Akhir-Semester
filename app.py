import os
from flask import Flask, render_template, request, redirect, url_for
from flask import session
app = Flask(__name__)
app.secret_key = "secret123"

class Produk:
    def __init__(self, id, nama, harga, deskripsi, qty, toko):
        self.id = id
        self.nama = nama
        self.harga = harga
        self.deskripsi = deskripsi
        self.qty = qty
        self.toko= toko

    def info(self):
        return f"{self.id} | {self.nama} | Rp{self.harga:,}| Stok: {self.qty} | Toko: {self.toko}".replace(",", ".")

class ProdukAdmin:
    def __init__(self):
        self.daftarProduk = []

    def tambahProduk(self, produk):
        self.daftarProduk.append(produk)

    def hapusProduk(self, idProduk):
        self.daftarProduk = [p for p in self.daftarProduk if p.id != idProduk]

    def cariProduk(self, idProduk):
        for p in self.daftarProduk:
            if p.id == idProduk:
                return p
        return None
    
    def editProduk(self, idProduk):
        produk = self.cariProduk(idProduk)
        if not produk:
            print("Produk tidak ditemukan!")
            return
        
        print("\n === Edit Produk ===")
        print("Tekan Enter jika tidak ingin mengubah nilai")

        print(f"Nama lama: {produk.nama}")
        nama_baru = input("Nama Baru: ").strip()
        if nama_baru:
            produk.nama = nama_baru

        print(f"Harga lama: {produk.harga}")
        harga_baru = input("Harga Baru: ").strip()
        if harga_baru:
            try:
                produk.harga = int(harga_baru)
            except:
                print("Input harga tidak valid, diabaikan.")

        print(f"Deskripsi lama: {produk.deskripsi}")
        desk_baru = input("Deskripsi baru: ").strip()
        if desk_baru:
            produk.deskripsi = desk_baru

        print(f"Qty lama: {produk.qty}")
        qty_baru = input("Qty baru: ").strip()
        if qty_baru:
            try:
                produk.qty = int(qty_baru)
            except:
                print("Input qty tidak valid, diabaikan.")
        
        print(f"Toko lama: {produk.toko}")
        toko_baru = input("Toko Baru: ").strip()
        if toko_baru:
            produk.toko = toko_baru

        print("\nProduk berhasil diperbarui!")


    def tampilkanProduk(self):
        if not self.daftarProduk:
            print("Tidak ada produk")
            return
        print("=== Daftar Produk ===")
        for p in self.daftarProduk:
            print(p.info())

class Cart:
    def __init__(self):
        self.items = {}

    def tambah(self, produk, qty):
        if produk.qty < qty:
            print("Stok tidak mencukupi!")
            return
        if produk.id not in self.items:
            self.items[produk.id] = {"produk": produk, "qty": qty}
        else:
            self.items[produk.id]["qty"] += qty
        print("Produk ditambahkan ke keranjang")
    
    def tampilkan(self):
        if not self.items:
            print("Keranjang Kosong")
            return
        print("=== Isi Keranjang ===")
        for item in self.items.values():
            p = item["produk"]
            qty = item["qty"]
            print(f"{p.nama} | {qty} pcs | Subtotal: Rp{p.harga * qty:,}".replace(",", "."))

    def hitungSubtotal(self):
        return sum(item["produk"].harga * item["qty"] for item in self.items.values())
    
    def hapusById(self, idProduk):
        if idProduk not in self.items:
            print("Produk tidak ditemukan di keranjang.")
            return

        item = self.items[idProduk]
        p = item["produk"]
        qtySaatIni = item["qty"]

        print(f"\nProduk: {p.nama}")
        print(f"Qty di keranjang: {qtySaatIni}")

        if qtySaatIni == 1:
            del self.items[idProduk]
            print(f"Produk {idProduk} dihapus dari keranjang.")
            return
        
        try:
            qtyHapus = int(input("Masukkan jumlah qty yang ingin dihapus: "))
        except:
            print("input tidak valid")
            return
        
        if qtyHapus <= 0:
            print("Qty tidak boleh kurang dari 1")
            return
        
        if qtyHapus >= qtySaatIni:
            del self.items[idProduk]
            print("Semua qty produk telah dihapus dari keranjang")
        else:
            item["qty"] -= qtyHapus
            print(f"Berhasil menghapus {qtyHapus} qty dari produk {p.nama}")        

    def hapusByToko(self, namaToko):
        self.items = {pid: it for pid, it in self.items.items() if it["produk"].toko != namaToko}
        print(f"Semua barang dari toko '{namaToko}' telah dihapus")

class Checkout:
    ongkirPulau = {
            "sumatera": 30000,
            "jawa": 45000,
            "kalimantan": 50000,
            "sulawesi": 45000,
            "papua": 70000,
            "timor": 65000
        }
    
    def __init__(self, cart):
        self.cart = cart

    def proses(self):
        if not self.cart.items:
            print("Keranjang kosong, tidak bisa checkout")
            return
        subTotal = self.cart.hitungSubtotal()

        diskon = 0.1 * subTotal if subTotal > 5000000 else 0

        alamat = input("Masukkan alamat tujuan: ").lower()

        ongkir = 0

        for pulau, harga in self.ongkirPulau.items():
            if pulau in alamat:
                ongkir = harga
                break

        if ongkir == 0:
            print("\nAlamat tidak tersedia ongkir, akan dikenakan biaya default sebesar Rp70.000")
            ongkir = 70000

        total = subTotal - diskon + ongkir

        print("=== Checkout ===")
        print(f"Subtotal : Rp{subTotal:,}".replace(",", "."))
        print(f"Diskon : Rp{diskon:,}".replace(",", "."))
        print(f"Ongkir : Rp{ongkir:,}".replace(",", "."))
        print(f"Total : Rp{total:,}".replace(",", "."))
        print("\nTerima Kasih sudah berbelanja")

        for pid, item in list(self.cart.items.items()):
            produk = item["produk"]
            qtyBeli = item["qty"]

            produk.qty -= qtyBeli
            if produk.qty < 0:
                produk.qty = 0

            del self.cart.items[pid]

        print("\nStok Produk berhasil diperbarui setelah checkout")

class UserManager:
    def __init__(self):
        self.users = {
            # username : password
            'users1': 'pass123',
            'users2': 'userxyz'
        }
        self.admins = {
            'admin1': 'admin123',
            "superadmin": 'root'
        }

    def cekUser(self, username, password):
        return username in self.users and self.users[username] == password
    
    def cekAdmin(self, username, password):
        return username in self.admins and self.admins[username] == password
    
    def register(self, username, password, role):
        if username in self.users or username in self.admins:
            return False, 'Username sudah terdaftar'
        
        if role == 'pembeli':
            self.users[username] = password
        elif role == 'penjual':
            self.admins[username] = password
        else:
            return False, "Role tidak valid"
        return True, "Registrasi berhasil"
    
    def resetPassword(self, oldUsername, newUsername, newPassword):
        if oldUsername in self.users:
            if newUsername:
                self.users[newUsername] = newPassword
                del self.users[oldUsername]
            else:
                self.users[oldUsername] = newPassword
            return True
        
        if oldUsername in self.admins:
            if newUsername:
                self.admins[newUsername] = newPassword
                del self.admins[oldUsername]
            else:
                self.admins[oldUsername] = newPassword
            return True
        return False

Produk_Admin = ProdukAdmin()
cart = Cart()
userManager = UserManager()

# Daftar Halaman Start
@app.route("/login", methods = ["GET"])
def halamanLogin():
    return render_template("login.html")

@app.route("/index")
def halamanIndex():
    if "login" not in session:
        return redirect(url_for("halamanLogin"))
    return render_template('index.html')

@app.route("/forgot")
def halamanForgot():
    return render_template('forgot.html')

@app.route("/register", methods = ["GET"])
def halamanRegister():
    return render_template('register.html')
# Daftar Halaman End

# Login Start
@app.route("/login", methods = ["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form['role']

    if role == "user" and userManager.cekUser(username, password):
        session["login"] = True
        session["user"] = "user"
        return render_template(
            "login.html",
            success = "Login berhasil! Klik OK untuk masuk."
        )
    elif role == "admin" and userManager.cekAdmin(username, password):
        session["login"] = True
        session["admin"] = "admin" 
        return render_template(
            "login.html",
            success = "Login berhasil! Tunggu sebentar."
        )
    else:
        return render_template(
            "login.html",
            error = "Username atau Password salah"
        )
# Login End

# Register Start
@app.route("/register", methods = ["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirmPassword"]
    role = request.form["role"]

    if password != confirm:
        return render_template(
            "register.html",
            error = 'Konfirmasi password tidak sama'
        )
    berhasil, pesan = userManager.register(username, password, role)

    if berhasil:
        return render_template(
            'login.html',
            success = "Registrasi berhasil, silahkan login"
        )
    else:
        return render_template(
            "register.html",
            error = pesan
        )
# Register End

# Reset Password Start
@app.route("/resetPassword", methods = ["post"])
def resetPassword():
    oldUsername = request.form["oldUsername"]
    newUsername = request.form["newUsername"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]

    if newPassword != confirmPassword:
        return "Password tidak sama!"
    
    berhasil = userManager.resetPassword(
        oldUsername,
        newUsername,
        newPassword
    )

    if berhasil:
        return render_template(
            "forgot.html",
            success = "Password berhasil diubah. Silahkan Login ulang."
        )
    else:
        return render_template(
            "forgot.html",
            error = "Username tidak ditemukan"
        )
# Reset Password End

Produk_Admin.tambahProduk(Produk("P001", "Keyboard", 150000, "Keyboard gaming", 10, "Toko A"))
Produk_Admin.tambahProduk(Produk("P002", "Mouse", 80000, "Mouse wireles", 10, "Toko B"))
Produk_Admin.tambahProduk(Produk("P003", "Headset", 250000, "Headset bass", 5, "Toko C"))

if __name__ == "__main__":
    app.run(debug=True)