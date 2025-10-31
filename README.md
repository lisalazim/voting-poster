E-Voting Poster Terfavorit

Aplikasi E-Voting Poster Terfavorit ini dibuat menggunakan Flask dan SQLite. Sistem memungkinkan peserta memilih poster favorit secara digital, dan admin dapat mengelola poster, status voting, serta kode voting.

📝 Fitur

Halaman voting untuk peserta (SMP, SMA, Guru)

Admin bisa:

Menambah, mengedit, dan menghapus poster

Membuka/tutup voting

Voting sederhana: pilih poster, muncul pop-up selesai, kembali ke halaman awal

⚙️ Persyaratan

Python 3.10+

Pip

Virtual environment (disarankan)

Dependencies:

Flask

Flask-SQLAlchemy

💻 Instalasi

Clone repository

git clone <url-repo-anda>
cd nama-folder-repo


Buat virtual environment (opsional tapi disarankan)

python -m venv venv


Aktifkan virtual environment

Windows:

venv\Scripts\activate


Linux/macOS:

source venv/bin/activate


Install dependencies

pip install -r requirements.txt


(Jika belum ada requirements.txt, buat dengan isi: Flask, Flask-SQLAlchemy, openpyxl)

Jalankan aplikasi

python app.py


Akses aplikasi

Dari browser: http://127.0.0.1:5000/ untuk peserta

Admin login: http://127.0.0.1:5000/admin/login

Username: admin

Password: admin123

openpyxl

Werkzeug

💻 Instalasi

Clone repository

git clone <url-repo-anda>
cd nama-folder-repo


Buat virtual environment (opsional tapi disarankan)

python -m venv venv


Aktifkan virtual environment

Windows:

venv\Scripts\activate


Linux/macOS:

source venv/bin/activate


Install dependencies

pip install -r requirements.txt


(Jika belum ada requirements.txt, buat dengan isi: Flask, Flask-SQLAlchemy, openpyxl)

Jalankan aplikasi

python app.py


Akses aplikasi

Dari browser: http://127.0.0.1:5000/ untuk peserta

Admin login: http://127.0.0.1:5000/admin/login

Username: admin

Password: admin123


👨‍💻 Penggunaan

Admin

Login → dashboard

Tambah poster → unggah gambar → simpan

Buka voting → peserta bisa mulai memilih

Generate kode voting → download Excel (opsional)

Peserta

Buka halaman voting → pilih poster favorit → klik pilih → muncul pop-up selesai → kembali ke halaman awal

Hasil Voting

Admin atau peserta bisa melihat hasil voting melalui halaman /results

⚡ Tips & Catatan

Pastikan folder static/uploads ada dan writable untuk menyimpan poster

Voting otomatis bisa berjalan meski peserta menggunakan perangkat yang sama, karena sistem tidak membatasi satu device

Jika menambahkan poster baru, database akan otomatis menyimpan jumlah vote default 0
