Link repository ETS : 
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
![Uploading image.png…]()  
Di atas adalah screenshot sebagian tabel yang mencatat ketika server menggunakan multithreading. Untuk



