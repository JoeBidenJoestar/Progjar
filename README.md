1. Pada tahap ini, skrip socket_info.py hanya memanggil fungsi getaddrinfo() untuk domain[ www.its.ac.id](http://www.its.ac.id/). Tidak ada paket TCP handshake karena skrip tidak memanggil connect() atau send(). Analisis menunjukkan bahwa getaddrinfo() memicu komunikasi DNS di port 53, dan tidak menghasilkan koneksi TCP lebih lanjut, sehingga hanya dua frame DNS yang muncul. Wireshark mencatat waktu, ID transaksi, serta details query dan response secara lengkap.
  
  Mesin1 dan analisis:  
![image](https://github.com/user-attachments/assets/fe8bddb7-de1f-432e-9c27-47c40187a2c7)
![image](https://github.com/user-attachments/assets/f43dda6b-df23-43f5-974f-1a733721a19a)
  
  Mesin2 dan analysis:  
![image](https://github.com/user-attachments/assets/091c41a1-0ec7-462b-889a-55f26968352a)

   
2. Di soal ini, server di mesin1 mendengarkan di 0.0.0.0:10000, sedangkan client di mesin2 menghubungkan ke 172.18.0.3:10000 (ip addr mesin1 172.18.0.3). Setelah dijalankan, client mengirimkan string data “INI ADALAH DATA …” ke server, yang langsung di-echo balik oleh server. Pada wireshark dapat diamati urutan paket: pertama paket TCP SYN dari client ke server, dilanjutkan SYN-ACK dari server ke client, diikuti paket ACK final untuk menyelesaikan handshake. Selanjutnya muncul tiga paket bertanda PSH, ACK yang membawa payload data terfragmentasi (karena ukuran buffer 16 byte), lalu server mengirimkan kembali paket PSH, ACK berisi data yang sama.
![image](https://github.com/user-attachments/assets/abc06710-8985-4c04-86c6-8befee876de0)
![image](https://github.com/user-attachments/assets/01ef8fb3-f7b4-4aa7-9da7-05b296925c0e)
![image](https://github.com/user-attachments/assets/fa9f0ea9-6cd9-4a4a-8eee-0cc0ca9433b0)

  
3. Pada soal ini, server.py (mesin1) dan client.py (mesin2) diubah agar menggunakan port **32444** alih-alih port default 10000. Server di mesin1 mendengarkan pada 0.0.0.0:32444, sedangkan client di mesin2 menghubungkan ke 172.18.0.3:32444. Dari analisis wireshark bisa diambil kesimpulan bahwa penggantian port hanya memindahkan komunikasi ke port lain tanpa mengubah mekanisme TCP; transfer data tercatat lengkap.
![image](https://github.com/user-attachments/assets/c324b014-1eb8-481b-9e72-f7795e954940)
![image](https://github.com/user-attachments/assets/5b3685c1-6954-478c-8892-7f92b69b25c8)
![image](https://github.com/user-attachments/assets/9ba33a6b-d162-4517-99f6-73b50a11c109)

  
4. Pada eksperimen simultan ini, kedua client (mesin2 dengan IP 172.18.0.4 dan mesin3 dengan IP 172.18.0.5) sama-sama mencoba terhubung ke server di mesin1 (172.18.0.3) pada port 32444 secara bersamaan. Di sisi server, program memanggil listen(1), sehingga backlog hanya satu koneksi pending, sedangkan koneksi kedua akan menunggu dalam antrean. Wireshark memperlihatkan dua handshake TCP yang berjalan hampir bersamaan: SYN dari mesin-2 dan SYN dari mesin3 memasuki antrean; server merespons kedua SYN dengan SYN-ACK sesuai urutan.
  
Gambar 1: Analisis Mesin2 Client  
![image](https://github.com/user-attachments/assets/5323c3b2-69cf-4ad9-8039-6efff237720c)  
  
Gambar 2: Analisis Mesin3 Client  
![image](https://github.com/user-attachments/assets/d5967854-4a93-4787-b9aa-45f04f0fd8e4)
