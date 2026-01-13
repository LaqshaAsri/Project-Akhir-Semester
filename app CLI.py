import os

def tranpose(ns):
    return [list(row) for row in zip(*ns)]

def print_table(table: list[list[str]]):
    # sama ratakan tiap str pada table
    for i, ns in enumerate(table):
        ns_ns = [len(x) for x in ns]
        ns_max = max(ns_ns)
        ns_ns = [ns_max - x for x in ns_ns]

        table[i] = [string + ' ' * ns_ns[j] for j, string in enumerate(table[i])]

    # print table
    table = tranpose(table)
    line_len = 0
    for i in table[0]:
        line_len += len(i) + 3
    line = "=" * (line_len + 1)

    head = table.pop(0)

    print(line)
    print("| ", end="")
    for i in head:
        print(i, end= " | ")
    print()
    print(line)

    for i in table:
        print("| ", end="")
        for j in i:
            print(j, end=" | ")
        print()
    print(line)

# Deklarasi Produk
class Produk:
    def __init__(self, id, nama, harga, deskripsi, qty, toko):
        self.id = id
        self.nama = nama
        self.harga = harga
        self.deskripsi = deskripsi
        self.qty = qty
        self.toko= toko

    def info(self):
        harga_str = f"Rp {self.harga:,}".replace(",", ".")
        return f"{str(self.id):<4} | {self.nama:<12} | {harga_str:>12} | {str(self.qty):<4} | {self.toko:<10} |"

# Fitur-fitur Admin
class ProdukAdmin:
    def __init__(self):
        self.daftarProduk = []

    def tambahProduk(self, produk):
            self.daftarProduk.append(produk)
        

    def hapusProduk(self, idProduk):
        for p in self.daftarProduk:
            if p.id == idProduk:
                self.daftarProduk.remove(p)
                return True
        return False


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
        table = [['Id'], ['Nama'], ['Harga'], ['Stock'], ['Toko']]
        if not self.daftarProduk:
            print('Tidak ada daftar produk')
            return None

        for p in self.daftarProduk:
            table[0].append(f'{p.id}')
            table[1].append(f'{p.nama}')
            table[2].append(f'{p.harga:,}'.replace(',', '.'))
            table[3].append(f'{p.qty}')
            table[4].append(f'{p.toko}')

        print("=== Daftar Produk ===\n")

        return print_table(table)
        

# Keranjang User
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
        table = [['id'],['nama'],['qty'], ['subtotal'], ['toko']]
        for item in self.items.values():
            p = item["produk"]
            qty = item["qty"]
            table[0].append(f'{p.id}')
            table[1].append(f'{p.nama}')
            table[2].append(f'{qty}')
            table[3].append(f'Rp{p.harga * qty:,}'.replace(',', '.'))
            table[4].append(f'{p.toko}')
        print_table(table)

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
    def hapusSemua(self):
        self.items.clear()
        print("Semua item di keranjang telah dihapus")

class WishCart:
    def __init__(self):
        self.items = {}

    def tambah(self, produk, qty):
        if produk.id not in self.items:
            self.items[produk.id] = {"produk": produk, "qty": qty}
        else:
            self.items[produk.id]["qty"] += qty
        print("Produk ditambahkan ke WishList")

    def tampilkan(self):
        if not self.items:
            print("WishList Kosong")
            return
        print("=== Isi WishList ===")
        table = [['id'],['nama'],['qty'], ['subtotal'], ['toko']]
        for item in self.items.values():
            p = item["produk"]
            qty = item["qty"]
            table[0].append(f'{p.id}')
            table[1].append(f'{p.nama}')
            table[2].append(f'{qty}')
            table[3].append(f'Rp{p.harga * qty:,}'.replace(',', '.'))
            table[4].append(f'{p.toko}')
        print_table(table)

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

# Pengecekan Alamat User untuk mendapatkan Ongkir
class Checkout:
    ongkirPulau = {
            "sumatera":{'aceh': 60000, 'medan': 55000, 'riau': 50000, 'jambi': 50000, 'bengkulu': 60000, 'lampung': 45000},
            "jawa": {'jakarta': 45000, 'bandung': 45000, 'surabaya': 45000, 'yogyakarta': 40000, 'semarang': 40000, 'malang': 40000},
            "kalimantan": {'banjarbaru': 50000, 'pontianak': 50000, 'samarinda': 50000, 'palangkaraya': 55000, 'tarakan': 55000},
            "sulawesi": {'manado': 60000, 'makassar': 60000, 'palu': 65000, 'kendari': 65000, 'gorontalo': 60000},
            "papua": { 'jayapura': 80000, 'merauke': 85000, 'biak': 80000, 'timika': 85000, 'sorong': 80000},
            "bali & nusa tenggara": {'denpasar': 55000, 'mataram': 60000, 'kupang': 65000, 'labuan bajo': 60000, 'sumbawa': 65000}
        }
    
    def __init__(self, cart):
        self.cart = cart

    def proses(self, target_id=None):
        if not self.cart.items:
            print("Keranjang kosong, tidak bisa checkout")
            return
        
        print("\n--- Opsi Checkout ---")
        print("1. Checkout Semua Barang")
        print("2. Checkout ID Tertentu")
        pilihan = input("Pilih (1/2): ")
        
        items_to_process = {}
        
        if pilihan == "2":
            print("\nID Produk dalam keranjang:")
            for pid in self.cart.items.keys():
                print(f"- {pid}")
            
            target_id = input("Masukkan ID Produk yang ingin di-checkout: ")
            
            if target_id in self.cart.items:
                items_to_process[target_id] = self.cart.items[target_id]
            else:
                print("ID tidak ditemukan di keranjang!")
                return
        else:
            items_to_process = self.cart.items.copy()
    
        subTotal = sum(item['produk'].harga * item['qty'] for item in items_to_process.values())
        if subTotal > 200000:
            persen = 0.20
        elif subTotal > 50000:
            persen = 0.10
        else:
            persen = 0
            
        diskon = min(subTotal * persen, 50000)

        alamat = input("Masukkan alamat tujuan: ").lower()

        ongkir = 0

        if  subTotal > 150000:
            potongan_ongkir = 20000
            ongkir = max(0, ongkir - potongan_ongkir)
            print(f"Promo: Potongan ongkir Rp {potongan_ongkir} aktif!")

        for pulau, harga in self.ongkirPulau.items():
            for kota, hargaKota in harga.items():
                if kota in alamat:
                    ongkir = hargaKota
                    break

        if ongkir == 0:
            print("\nAlamat tidak tersedia ongkir, akan dikenakan biaya default sebesar Rp70.000")
            ongkir = 70000

        total = subTotal - diskon + ongkir
        #Struk Checkout
        print("=== Checkout ===")
        print(f"Subtotal : Rp {subTotal:,}".replace(",", "."))
        print(f"Diskon : Rp {diskon:,}".replace(",", "."))
        print(f"Ongkir : Rp {ongkir:,}".replace(",", "."))
        print(f"Total : Rp {total:,}".replace(",", "."))
        print("\nTerima Kasih sudah berbelanja")

        for pid, item in items_to_process.items():
            produk = item["produk"]
            qtyBeli = item["qty"]

            produk.qty -= qtyBeli
            if produk.qty < 0:
                produk.qty = 0

            del self.cart.items[pid]

        print("\nStok Produk berhasil diperbarui setelah checkout")

# Data User dan Admin untuk login
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
        if username not in self.users:
            return False
        
        if self.users[username] != password:
            return False
        
        return True
    
    def cekAdmin(self, username, password):
        if username not in self.admins:
            return False
        
        if self.admins[username] != password:
            return False
        
        return True
    
    def registerUser(self, username, password):
        if username in self.users or username in self.admins:
            return False
        self.users[username] = password
        return True

# Jalankan Fungsi
Produk_Admin = ProdukAdmin()
cart = Cart()
wish_cart = WishCart()

# Dummy produk, bisa ditambahkan melalui menu admin juga
Produk_Admin.tambahProduk(Produk("P001", "Keyboard", 150000, "Keyboard gaming", 10, "GamingStore"))
Produk_Admin.tambahProduk(Produk("P002", "Mouse", 80000, "Mouse wireles", 10, "GamingStore"))
Produk_Admin.tambahProduk(Produk("P003", "Headset", 250000, "Headset bass", 5, "GamingStore"))
Produk_Admin.tambahProduk(Produk("P004", "Monitor", 1250000, "Monitor 24 inch", 3, "TechWorld"))
Produk_Admin.tambahProduk(Produk("P005", "Laptop", 5500000, "Laptop gaming", 2, "TechWorld"))
Produk_Admin.tambahProduk(Produk("P006", "Smartphone", 3000000, "Smartphone terbaru", 7, "GadgetHub"))


userManager = UserManager() 

# Tampilan ketika login atau register
def menuLogin():
    while True:
        os.system('cls')
        print("=== Login ===")
        print('1. Login')
        print('2. Register')
        print('3. Keluar')

        menu = input("Pilih menu 1-3: ").strip()

        if menu == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            print("1. Login Sebagai User")
            print("2. Login Sebagai Admin")
            print("3. Keluar")

            pilihan = input("Pilih menu (1-3): ").strip()

            if pilihan == '1':
                if userManager.cekUser(username, password):
                    print("\nLogin User Berhasil!")
                    input("Enter untuk masuk...")
                    return "user"
                else:
                    print('\nUsername atau password user salah!')
                    input('Enter untuk ulang...')
            if pilihan == "2":
                if userManager.cekAdmin(username, password):
                    print("\nLogin Admin Berhasil!")
                    input("Enter untuk masuk...")
                    return "admin"
                else:
                    print('\nUsername atau password admin salah!')
                    input('Enter untuk ulang...')
            elif pilihan == '3':
                print("Keluar program...")
                exit()
            else:
                print("Pilihan tidak valid!")
                input("Enter untuk ulang...")

            print("\n1. Coba Login Lagi")
            print("2. Register Akun")
            pilih = input("pilih 1-2: ").strip()

            if pilih == '2':
                menu = '2'
            else:
                continue
        
        elif menu == '2':
            os.system('cls')
            print("=== Register ===")
            username = input("Username Baru: ").strip()
            password = input('Password Baru: ').strip()

            if userManager.registerUser(username, password):
                print("\nRegister berhasil! Silahkan Login.")
            else:
                print("\nUsername sudah digunakan!")
            
            input("Enter untuk kembali ke menu login...")

        elif menu == '3':
            exit()

        else:
            print('Pilihan tidak valid!')
            input("Enter untuk ulang...")

# Tampilan menu admin
def menuAdmin():
    while True:
        os.system('cls')
        print("=== Menu Admin ===")
        print("1. Lihat Semua Produk")
        print("2. Tambah Produk")
        print("3. Hapus Produk")
        print("4. Edit Produk")
        print("5. Kembali ke Login")

        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            os.system('cls')
            Produk_Admin.tampilkanProduk()
            input("Enter untuk kembali...")
        
        elif pilihan == "2":
            os.system('cls')
            print("=== Tambah Produk ===")
            print("Tekan Enter tanpa input untuk membatalkan\n")
            idp = input("ID Produk: ").strip()

            if not idp:
                continue
            
            nama = input("Nama: ").strip()
            if not nama:
                continue
            
            hargaInput = input("Harga: ").strip()
            if not hargaInput:
                continue
            
            try:
                harga = int(hargaInput)
            except:
                print("Harga harus angka!")
                input("Enter untuk kembali...")
                continue
            
            desk = input("Deskripsi: ").strip()
            if not desk:
                continue
            
            qtyInput = input("Qty: ").strip()
            if not qtyInput:
                continue
            
            try:
                qty = int(qtyInput)
            except:
                print("Qty harus angka!")
                input("Enter untuk kembali...")
                continue
            
            toko = input("Toko: ").strip()
            if not toko:
                continue

            if Produk_Admin.cariProduk(idp):
                print("ID produk sudah ada!")
                input("Enter untuk kembali...")
                continue
            Produk_Admin.tambahProduk(Produk(idp, nama, harga, desk, qty, toko))
            print("Produk berhasil ditambah!")
            input("Enter untuk kembali...")

        elif pilihan == "3":
            os.system('cls')
            print("=== Hapus Produk ===")
            print("Tekan Enter tanpa input untuk membatalkan\n")

            pid = input("Masukkan ID produk yg ingin dihapus: ").strip()

            if not pid:
                continue

            success = Produk_Admin.hapusProduk(pid)

            if success:
                print("Produk berhasil dihapus!")
            else:
                print("Produk tidak ditemukan!")
            
            input("Enter untuk kembali...")

        elif pilihan == "4":
            while True:
                os.system("cls")
                print("=== Edit Produk ===")
                print("Tekan Enter tanpa input untuk membatalkan\n")

                pid = input("Masukkan ID produk yang ingin diedit: ").strip()

                if not pid:
                    break

                produk = Produk_Admin.cariProduk(pid)

                if not produk:
                    print("Produk tidak ditemukan!")
                    input("Enter untuk coba lagi...")
                    continue

                Produk_Admin.editProduk(pid)
                input("Enter untuk kembali...")
            
        elif pilihan == "5":
            return
        
        else: 
            print("Pilihan tidak valid!")
            input("Enter untuk ulang...")

# Tampilan Menu user dan juga pengecekan jika user masuk sebagai user atau admin
while True:
    role = menuLogin()

    if role == "admin":
        menuAdmin()
    
    elif role == "user":
        while True:
            os.system('cls')
            print('\n=== Tampilan User ===')
            print('1. Lihat Produk')
            print('2. Tambah ke Keranjang')
            print('3. Lihat Keranjang')
            print('4. Tambah ke WishList')
            print('5. Lihat WishList')
            print('6. Checkout')
            print('7. Keluar')
            choice = input('Pilih menu (1-7): ').strip()
            if choice == '1':
                os.system('cls')
                Produk_Admin.tampilkanProduk()
                input("\nTekan Enter untuk kembali...")
            elif choice == '2':
                os.system('cls')
                Produk_Admin.tampilkanProduk()
                tambah_lagi = input("\nApakah Anda ingin menambah produk ke keranjang? (y/n): ").lower()
                if tambah_lagi == 'y':
                    pid = input("\nMasukkan ID produk yang ingin dibeli: ")
                    qty = int(input("Jumlah: "))
                    produk = Produk_Admin.cariProduk(pid)
                    if produk:
                        cart.tambah(produk, qty)
                    else:
                        print("Produk tidak ditemukan")

                else:
                    print("Kembali ke menu utama.")

                input("Tekan Enter untuk kembali...")

            elif choice == '3':
                os.system('cls')
                cart.tampilkan()
                print("=== Keranjang ===")
                print("1. Sesuaikan qty item")
                print("2. Hapus item berdasarkan ID")
                print("3. Hapus item berdasarkan toko")
                print("4. Hapus semua item di keranjang")
                print("5. Kembali")
               
                pilih = input("Pilih menuh 1-5: ").strip()
 
                if pilih == '1':
                    if not cart.items:
                        print("Keranjang kosong")
                        input("Tekan Enter untuk lanjut...")
                        continue
                   
                    pid = input("Masukkan ID produk yang ingin disesuaikan qty-nya: ")
                    if pid not in cart.items:
                        print("Produk tidak ditemukan di keranjang.")
                        input("Tekan Enter untuk lanjut...")
                        continue
 
                    item = cart.items[pid]
                    p = item["produk"]
                    qtySaatIni = item["qty"]
 
                    print(f"\nProduk: {p.nama}")
                    print(f"Qty di keranjang: {qtySaatIni}")
 
                    try:
                        qtyBaru = int(input("Masukkan jumlah qty baru: "))
                    except:
                        print("input tidak valid")
                        input("Tekan Enter untuk lanjut...")
                        continue
                   
                    if qtyBaru <= 0:
                        print("Qty tidak boleh kurang dari 1")
                        input("Tekan Enter untuk lanjut...")
                        continue
                   
                    if qtyBaru > p.qty:
                        print("Stok tidak mencukupi!")
                        input("Tekan Enter untuk lanjut...")
                        continue
 
                    item["qty"] = qtyBaru
                    print(f"Qty produk {p.nama} berhasil diperbarui menjadi {qtyBaru}")
                    input("Tekan Enter untuk lanjut...")
                   
               
                elif pilih == "2":
                    pid = input("Masukkan ID produk yang ingin dihapus: ")
                    cart.hapusById(pid)
                    input("Tekan Enter untuk lanjut...")
                elif pilih == "3":
                    toko = input("Masukkan nama toko: ")
                    cart.hapusByToko(toko)
                    input("Tekan Enter untuk lanjut...")
                elif pilih == "4":
                    cart.hapusSemua()
                    input("Tekan Enter untuk lanjut...")
                elif pilih == "5":
                    continue
                else:
                    print("Pilihan tidak valid")
                    print('Tekan Enter untuk lanjut')

            elif choice == '4':
                os.system('cls')
                Produk_Admin.tampilkanProduk()
                tambah_lagi = input("\nApakah Anda ingin menambah produk ke wishlist? (y/n): ").lower()
                if tambah_lagi == 'y':
                    pid = input("\nMasukkan ID produk yang ingin ditambahkan: ")
                    qty = int(input("Jumlah: "))
                    produk = Produk_Admin.cariProduk(pid)
                    if produk:
                        wish_cart.tambah(produk, qty)
                    else:
                        print("Produk tidak ditemukan")

                else:
                    print("Kembali ke menu utama.")

                input("Tekan Enter untuk kembali...")

            elif choice == '5':
                os.system('cls')
                wish_cart.tampilkan()
                print("=== WishList ===")
                print("1. Hapus item berdasarkan ID")
                print("2. Hapus item berdasarkan toko")
                print("3. Kosongkan")
                print("4. Kembali")

                pilih = input("Pilih menuh 1-4: ").strip()

                if pilih == '1':
                    pid = input("Masukkan ID produk yang ingin dihapus: ")
                    wish_cart.hapusById(pid)
                    input("Tekan Enter untuk lanjut...")
                elif pilih == "2":
                    toko = input("Masukkan nama toko: ")
                    wish_cart.hapusByToko(toko)
                    input("Tekan Enter untuk lanjut...")
                elif pilih == "3":
                    wish_cart.items = {}
                    input("Tekan Enter untuk lanjut")
                elif pilih == "4":
                    continue
                else:
                    print("Pilihan tidak valid")
                    print('Tekan Enter untuk lanjut')

            elif choice == '6':
                os.system('cls')
                cart.tampilkan()
                lanjut = input("\nLanjutkan checkout? (y/n): ").lower()
                if lanjut == "y":
                    Checkout(cart).proses()
                input("\nTekan Enter untuk kembali...")
            elif choice == '7':
                print('Sampai jumpa — keluar program.')
                break
            else:
                print()
                print('Pilihan tidak valid.')
                print()
                input('Tekan Enter untuk kembali')

# Why is everything so heavy?
# Holding on
# To so much more than i can carry
# I rather live, die, than live forever
# Im so happy if i could die right now
# Im so happy if i could die right now
# Someone kill meeeeeeeeeeeeeeeeeeeeee!