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
