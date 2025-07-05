Link repository ETS : https://github.com/JoeBidenJoestar/Progjar/tree/ETS
# Tugas ETS Multithreading dan Multiprocessing
## Penjelasan Arsitektur
Arsitektur stress test ini terdiri dari dua komponen utama: 
(1) file_server.py, yang dapat dijalankan dalam mode multithreading (ThreadPoolExecutor) atau multiproses (multiprocessing.Process) dengan jumlah “server workers” yang bisa dikonfigurasi, sehingga setiap koneksi client dilayani secara paralel sampai batas worker; dan 
(2) file_client_cli.py, yang kini menyediakan mode “single combo” di mana pengguna menentukan operasi (upload/download), ukuran file (10 MB/50 MB/100 MB), dan jumlah client worker via argumen (--op, --size, --workers). 

Client dapat melakukan operasi upload maupun download dengan argumen contoh:  
`python3 file_client_cli2.py --op upload --size 10MB --workers 50`    
N thread client paralel memanggil API upload atau download, mengukur waktu dan ukuran tiap permintaan, dan menghentikan eksekusi jika melewati timeout 180 detik. 
Hasil stress test—jumlah berhasil dan gagal, rata‐rata waktu per worker, serta throughput per worker—dicetak ke konsol, memungkinkan evaluasi kinerja server pada berbagai kombinasi jumlah worker, volume data, dan mode threading vs. multiproses.  

## Pengerjaan
![image](https://github.com/user-attachments/assets/252f345e-2606-4cc8-9d64-e4e59bd5687e)  
Di atas adalah tampilan sisi server ketika dinyalakan, menggunakan argumen yang disesuaikan test uji yang diinginkan. Kemudian server menerima input dari client, akan diproses berdasarkan jumlah server dan client workernya.
![image](https://github.com/user-attachments/assets/309a585b-44ad-4ce7-9bf1-73883c89369d)  
Di atas adalah tampilan sisi client ketika program `file_client_cli.py` dinyalakan (dalam gambar saya merename file tersebut). Client menjalankan program dan juga memasukan argumen yang diinginkan.

## Tabel Hasil
![image](https://github.com/user-attachments/assets/723ffebe-3c77-4153-8641-4479971a69fd)
Di atas adalah screenshot sebagian tabel yang mencatat ketika server menggunakan multiprocessing. Untuk tabel lengkapnya (termasuk juga tabel multithreading) bisa diakses di [https://github.com/JoeBidenJoestar/Progjar/blob/ETS/ETS_Progjar.xlsx](url).  
Pada tabel tercatat jumlah server worker, client worker, ukuran file, time/client, throughput/client, jumlah sukses dan gagal. Ada pula yang isinya >180 dan `null`. Hal ini disebabkan karena program dibuat untuk menghentikan eksekusi jika melewati timeout 180 detik. Saat program dijalankan, jika melebihi waktu 180 detik maka output untuk time/client dan throughput/client menjadi nilai 0. Hal ini bertujuan supaya tidak memakan waktu yang lama.

## Kesimpulan Percobaan
Multiprocessing lebih cocok ketika terdapat lebih dari satu client worker (dan lebih dari satu server worker) ketimbang multithreading, hal ini bisa dilihat pada tabel:  
![image](https://github.com/user-attachments/assets/f17aed69-18fa-4faf-abaa-1bd5c182b163)  
Tabel Multiprocessing (1)
![image](https://github.com/user-attachments/assets/1aad761b-8e2d-42c1-8e17-5b624a35b1f1)  
Tabel Multiprocessing (2)
![image](https://github.com/user-attachments/assets/35be9d3f-5aed-4840-9888-59f7047c41c5)  
Tabel Multithreading (1)
![image](https://github.com/user-attachments/assets/80bb3a9d-96f9-475e-b2ad-ffd15f045417)  
Tabel Multithreading (2)  
Pada beberapa kesempatan, multiprocessing menggungguli multithread dalam hal kecepatan waktu walaupun kasus lain hanya memiliki selisih beberapa detik yang kemungkinan karena masalah internal atau eksternal saat pengujian.






