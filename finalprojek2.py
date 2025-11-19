# ======================================================
#   VIRUS DEFENSE 
# ======================================================
#team FLOW

# -----------------------------
# RANDOM GENERATOR TANPA IMPORT
# -----------------------------
seed = 1234567
def my_random(min_val, max_val):
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return min_val + (seed % (max_val - min_val + 1))

# -----------------------------
# CLEAR & DELAY TANPA IMPORT
# -----------------------------
def clear():
    print("\n" * 40)

def delay(ms):
    for _ in range(ms * 50000):
        pass

# -----------------------------
# HEADER GAME
# -----------------------------
def print_header(level, score, lives, energy):
    print("=" * 60)
    print(f" 💻 VIRUS DEFENSE  | Level: {level} | Skor: {score} | Nyawa: {lives} | 🔋Energi: {energy}")
    print("=" * 60)

def show_columns():
    print("\n[1] [2] [3] [4] [5]\n")

def virus_visual(positions):
    counts = [positions.count(i) for i in range(1, 6)]
    line = ""
    for c in counts:
        if c == 0:
            line += "·   "
        elif c == 1:
            line += "🦠  "
        else:
            line += "🦠x" + str(c) + " "
    print(line + "\n")

# -----------------------------
# MENU UPGRADE
# -----------------------------
def upgrade_menu(lives, energy):
    print("\n⚙️  UPGRADE SISTEM TERSEDIA!")
    print("1. Tambah 1 nyawa ❤️")
    print("2. Tambah 20 energi 🔋")
    print("3. Tingkatkan damage senjata 💥")

    choice = input("Pilih upgrade (1-3): ")

    if choice == "1":
        lives += 1
    elif choice == "2":
        energy += 20
    elif choice == "3":
        global weapon_damage
        weapon_damage += 1
        print("💥 Senjata ditingkatkan!")
    else:
        print("Pilihan tidak valid.")

    return lives, energy

# ======================================================
#                        GAME DIMULAI
# ======================================================
clear()
print("=== SELAMAT DATANG DI VIRUS DEFENSE ===")
print("Gunakan angka 1-5 (bisa banyak, pisahkan dengan spasi) untuk menembak.")
print("Ketik 'help' kapan saja untuk melihat cara bermain.\n")
input("Tekan ENTER untuk mulai...")

# ------------------------------------------------------
# PENGERTIAN GAME + CARA BERMAIN
# ------------------------------------------------------
clear()
print("=== PENGERTIAN GAME & CARA BERMAIN ===\n")
print("1. Setiap ronde, virus akan muncul di kolom 1–5.")
print("2. Pemain menembak virus dengan mengetik nomor kolom, misalnya: 2   atau   1 3 5")
print("3. Setiap tembakan mengurangi 5 energi.")
print("4. Jika tembakan tepat, virus hancur dan skor bertambah.")
print("5. Jika meleset, virus menyerang balik dan nyawa berkurang. ")
print("6. Ketika skor tertentu tercapai, pemain naik level dan dapat memilih upgrade.")
print("7. Game berakhir jika nyawa habis.")
print("8. Ketik 'help' kapan saja di dalam game untuk melihat panduan ini kembali.")
input()

# ------------------------------------------------------
# VARIABLE DASAR GAME
# ------------------------------------------------------
score = 0
lives = 3
level = 1
energy = 1000    # 🔥 Energi awal sudah diubah dari 100 → 1000
weapon_damage = 1

virus_memory = [0, 0, 0, 0, 0]
fail_memory = [0, 0, 0, 0, 0]

# ======================================================
#                 GAMEPLAY LOOP UTAMA
# ======================================================
while lives > 0:
    clear()
    print_header(level, score, lives, energy)
    show_columns()

    if energy <= 0:
        print("⚠️ Energi habis! Sistem recharge...")
        delay(50)
        energy += 30
        continue

    virus_count = 3 + level

    # AI adaptif membaca pola pemain
    weights = []
    for i in range(5):
        w = max(1, 10 - virus_memory[i] + fail_memory[i])
        weights.append(w)

    # Generate posisi virus berdasarkan bobot AI
    virus_positions = []
    total_weight = sum(weights)
    for _ in range(virus_count):
        r = my_random(1, total_weight)
        cumulative = 0
        for i in range(5):
            cumulative += weights[i]
            if r <= cumulative:
                virus_positions.append(i + 1)
                break

    print("\n⚠️ Virus menyerang...\n")
    delay(30)
    virus_visual(virus_positions)

    # --------------------------------------
    # INPUT TEMBAKAN + FITUR HELP
    # --------------------------------------
    shots_in = input("Kolom tembak (contoh: 1 3 5): ")

    if shots_in.lower() == "help":
        clear()
        print("=== CARA BERMAIN ===\n")
        print("1. Virus muncul di kolom 1–5.")
        print("2. Tembak dengan mengetik angka kolom, contoh: 1 3 5.")
        print("3. Tiap tembakan = -5 energi.")
        print("4. Jika tepat: virus hancur. Jika meleset: nyawa berkurang.")
        print("5. Saat naik level, pilih upgrade.")
        print("6. Menembak banyak virus = pisahkan dengan spasi.")
        print("7. Jika ada tanda 2x, berarti ada lebih dari satu virus.")
        print("8. Masukkan angka kolom beberapa kali untuk menghancurkan semuanya.")
        print("9. Ketik 'help' kapan saja untuk membuka menu ini lagi.\n")
        input("Tekan ENTER untuk kembali...")
        continue

    # --------------------------------------
    # PROSES TEMBAKAN NORMAL
    # --------------------------------------
    try:
        shots = [int(x) for x in shots_in.split() if x.isdigit()]
    except:
        print("Input tidak valid.")
        delay(50)
        continue

    shots = [s for s in shots if 1 <= s <= 5]
    if not shots:
        print("Tidak ada kolom valid.")
        delay(30)
        continue

    cost = len(shots) * 5
    if energy < cost:
        print("⚠️ Energi tidak cukup!")
        delay(40)
        continue

    energy -= cost

    # Proses tembakan
    for shot in shots:
        virus_memory[shot - 1] += 1

        if shot in virus_positions:
            kena = virus_positions.count(shot)
            hancur = min(kena, weapon_damage)

            for _ in range(hancur):
                virus_positions.remove(shot)

            print(f"🎯 Kolom {shot}: Menghancurkan {hancur} virus!")
            score += 10 * hancur

            if kena > hancur:
                print(f"⚠️ Masih ada {kena - hancur} virus tersisa di kolom {shot}")
        else:
            print(f"❌ Kolom {shot}: Tidak ada virus!")
            fail_memory[shot - 1] += 1
            lives -= 1
            print(f"💀 Virus menyerang balik! Nyawa: {lives}")

    # Serangan balik virus tersisa
    if len(virus_positions) > 0:
        serang = len(virus_positions) // 3
        if serang > 0:
            lives -= serang
            print(f"🔥 {len(virus_positions)} virus menyerang balik! -{serang} nyawa!")

    # LEVEL UP
    if score >= level * 80:
        level += 1
        print(f"\n⚡ LEVEL UP! Sekarang level {level} ⚡")
        lives, energy = upgrade_menu(lives, energy)

    delay(60)

# ======================================================
#                       GAME OVER
# ======================================================
clear()
print("=" * 60)
print("💀 GAME OVER 💀")
print(f"Skor akhir: {score}")
print(f"Level tertinggi: {level}")
print("=" * 60)
print("\n🧠 Catatan AI:")
print("- Sistem menggunakan AI adaptif tanpa import apa pun!")
print("- Random custom dibuat manual!")
print("- Clear screen dan delay dibuat tanpa library!")
