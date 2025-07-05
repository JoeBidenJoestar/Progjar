# Tugas 4 Pemrograman Jaringan


File server_thread_pool_http dan server_process_pool_http mendapatkan update kode bagian def ProcessTheClient supaya bisa mendapatkan content file yang diupload oleh client karena kode awalnya file hanya bisa baca sampai \r\n, setelah diupdate file bisa baca sampai \r\n\r\n (akhir header HTTP dan awal body).  
Tak hanya itu, file http.py juga diubah untuk mendukung operasi seperti list, upload, dan delete. Perubahan dilakukan di http_get dan http_post. Hal ini dilakukan untuk mengikuti persyaratan tugas. Untuk file client tidak ada perubahan signifikan.

![image](https://github.com/user-attachments/assets/37772429-0f7e-4c17-8af0-7cb60a9c7074)  
Pada screenshot ini, client mencoba mendapatkan list dari server thread pool, client menggunakan curl -v 172.16.16.101:8885/list di port 8885. Server merespons dengan mengirimkan list saat ini yang satu directory dengan server thread pool.  

![image](https://github.com/user-attachments/assets/56681ab0-61d5-444b-9783-fcb0f433b950)  
Pada screenshot ini, client mencoba mengupload file ke server thread pool, client menggunakan curl -v 172.16.16.101:8885/upload dengan konten file berisikan “Hello” di port 8885. Server merespons dengan mengirimkan pesan “Uploaded as …txt” untuk menunjukkan bahwa upload berhasil.  

![image](https://github.com/user-attachments/assets/4a8bfed3-31fb-4911-9299-3e41443455b4)  
Pada screenshot ini, client mencoba mendelete file dari server thread pool, client menggunakan curl -v 172.16.16.101:8885/delete/<nama file> di port 8885. Server merespons dengan mendelete file tersebut dan mengirim notifikasi ke client.

![image](https://github.com/user-attachments/assets/8d5ede15-87b6-40d8-8be4-19bf165c194a)  
Pada screenshot ini, client mencoba mengupload file ke server process pool, client menggunakan curl -v 172.16.16.101:8889/upload dengan konten file berisikan “Hello” di port 8885. Server merespons dengan mengirimkan pesan “Uploaded as …txt” untuk menunjukkan bahwa upload berhasil.  

![image](https://github.com/user-attachments/assets/15d76185-39f5-43b7-91da-9a4ffe3f9db3)  
Pada screenshot ini, client mencoba mendapatkan list dari server process pool, client menggunakan curl -v 172.16.16.101:8889/list di port 8889. Server merespons dengan mengirimkan list saat ini yang satu directory dengan server thread pool.  

![image](https://github.com/user-attachments/assets/985548de-75c5-4d58-ab7c-b716b1cd396d)  
Pada screenshot ini, client mencoba mendelete file dari server thread pool, client menggunakan curl -v 172.16.16.101:8889/delete/<nama file> di port 8889. Server merespons dengan mendelete file tersebut dan mengirim notifikasi ke client.

