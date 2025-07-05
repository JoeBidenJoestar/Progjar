# Laporan Tugas 2 Pemrograman Jaringan

**Link repo:** [https://github.com/JoeBidenJoestar/Progjar/tree/main/Tugas2](https://github.com/JoeBidenJoestar/Progjar/tree/main/Tugas2)

---
![image](https://github.com/user-attachments/assets/aec1b43d-0de3-41d5-8735-4cc9afa4798b)

Di atas adalah screenshot dari server_thread_time.py yang telah saya modifikasi. 
Pada fungsi `proses_string()` di `server_thread_time.py`, saya memodifikasi pemanggilan:

```python
strftime("%d-%m-%Y %H:%M:%S")
```

menjadi:

```python
strftime("%H:%M:%S")
```

Perubahan ini menghilangkan bagian tanggal (`%d-%m-%Y`), sehingga hanya jam, menit, dan detik yang dikirim. Dengan format ini, server memenuhi persyaratan soal nomor 1 bagian d. Selain itu, tidak ada perubahan lainnya.

---
![image](https://github.com/user-attachments/assets/1006b055-c5e2-4aa6-a3f9-1f1a01dc4f06)


Pada versi original `client_1.py`, fungsi `kirim_data()` bekerja dengan membuka socket, mengirim string panjang, lalu menunggu balasan sebelum menutup koneksi.

Untuk protokol `TIME` pada server, saya ubah fungsi tersebut menjadi `kirim_waktu(nomor)`.

Fungsi baru:
- mengirim `b"TIME
"`
- hanya satu kali `recv(64)` untuk mengambil balasan seperti `"JAM hh:mm:ss
"`
- mengirim `b"QUIT
"` setelah itu

Loop lama seperti:
```python
while amount_received < amount_expected
```
dihilangkan.

Di bagian `__main__`, saya mengganti pemanggilan fungsi menjadi menggunakan `threading`. Thread akan memanggil `kirim_waktu(i)` secara paralel dalam 9 thread, lalu `join()` untuk memastikan client-client berjalan bersamaan. Tujuannya adalah menguji kemampuan concurrency server sesuai soal nomor 1b.

Saya menamai modifikasi ini sebagai `client_3.py`.

---
![image](https://github.com/user-attachments/assets/1469d72d-ecdb-4ecc-b5d6-9f40de3da10a)


Dijalankanlah server di **mesin 1**, dan client di **mesin 2** dan **mesin 3**.

Di sisi server, setiap kali ada koneksi baru dari client, server mencetak:

```
connection from (<IP>, <port>)
```

Karena mesin 2 dan 3 masing-masing meluncurkan beberapa thread client, server menerima banyak koneksi masuk hampir bersamaan.

Log menunjukkan server menerima permintaan dari dua alamat berbeda (`172.16.16.102` dan `172.16.16.103`), dan koneksi kedua dan ketiga muncul pula dengan port yang berubah.

Ini membuktikan bahwa server multi-thread membuat satu thread penanganan untuk setiap koneksi, dan memprosesnya secara tumpang tindih tanpa harus menunggu satu sama lain selesai.

---
![image](https://github.com/user-attachments/assets/15093bb2-0638-4f50-b3a5-b676c89297ff)


Di sisi client (mesin 2 dan 3), client mencetak langkah-langkah berikut secara berurutan untuk setiap thread:

- membuka socket  
- mengirim `TIME`  
- menunggu balasan  
- mengirim `QUIT`  

Log akan berulang untuk setiap client karena client di mesin 2 dan 3 memulai thread dengan jeda satu detik. Setiap thread mencatat timestamp yang bergeser satu detik.

Hal ini menunjukkan bahwa di mesin 2 dan 3, client bekerja normal: setiap thread berhasil berkomunikasi dengan server secara concurrent, menerima hasil, dan menutup koneksi sesuai urutan yang dikodekan.
