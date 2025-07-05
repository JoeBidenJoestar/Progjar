# Tugas 3 Pemrograman Jaringan

**Link Git:** [https://github.com/JoeBidenJoestar/Progjar/tree/Tugas-3](https://github.com/JoeBidenJoestar/Progjar/tree/Tugas-3)

---
![image](https://github.com/user-attachments/assets/aa96c80a-01d6-46c6-83bd-3a32ee9ca59b)

File `server` dan `client` telah dimodifikasi untuk menangani request **LIST**, **GET**, **UPLOAD**, dan **DELETE**. Sistem ini juga mencakup mekanisme penanganan error, di mana jika suatu request tidak dikenali, server akan membalas dengan status `ERROR` disertai pesan yang sesuai. Client dapat memilih operasi mana yang mau dilakukan hanya dengan input angka.

### Fitur:

- **LIST**: memungkinkan client melihat daftar file yang tersedia di server.
- **GET**: digunakan untuk mengambil isi file tertentu yang sudah didecode dari base64.
- **UPLOAD**: client dapat menambahkan file ke server dengan menyertakan nama dan isi file dalam encoding base64.
- **DELETE**: digunakan untuk menghapus file yang ada di server.

Semua proses ini dilakukan melalui koneksi **socket**, di mana client mengirimkan string sesuai format protokol, dan server merespons status keberhasilan atau kegagalan permintaan tersebut.

---
### LIST

![image](https://github.com/user-attachments/assets/4bd2176d-65f5-4af5-bf3d-d03c6018623b)

---
### UPLOAD

![image](https://github.com/user-attachments/assets/8586aea3-a645-4d64-86df-8601a5fe102e)


Pada fitur `UPLOAD`, client memilih operasi nomor 3 lalu akan diminta mengisi nama file. Kemudian client akan mengisi kontennya menggunakan format base64. Server menerima permintaan dan melakukan operasi `UPLOAD`, dan file tersebut akan muncul di daftar file (`LIST`).

---
### DELETE

![image](https://github.com/user-attachments/assets/b624d1f6-f64d-40d8-9050-a701ac7e8596)

Client juga bisa menghapus file dengan memilih angka operasi 4 dan memasukkan nama file yang diinginkan. Jika file tidak ditemukan, maka akan muncul pesan:

```
Gagal menghapus file …
```

Jika file ditemukan, maka server akan menerima operasi `DELETE` dan menghapus file tersebut.
