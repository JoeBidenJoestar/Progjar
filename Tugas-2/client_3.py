import sys
import socket
import logging
import threading
import time

SERVER_ADDR = ('172.16.16.101', 45000)

def kirim_waktu(nomor):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning(f"[Client{nomor}] membuka socket ke {SERVER_ADDR}")
    sock.connect(SERVER_ADDR)

    try:
        # Send waktu
        logging.warning(f"[Client{nomor}] sending TIME")
        sock.sendall(b"TIME\r\n")
        #Look for the response
        data = sock.recv(64).decode().strip()
        logging.warning(f"[Client{nomor}] Received '{data}'")
        #Quit
        logging.warning(f"[Client{nomor}] sending QUIT")
        sock.sendall(b"QUIT\r\n")

    finally:
        logging.warning(f"[Client{nomor}] closing socket")
        sock.close()

if __name__ == '__main__':
    threads = []

    for i in range(1, 10):
        thr = threading.Thread(target=kirim_waktu, args=(i,))
        thr.start()
        threads.append(thr)
        time.sleep(1)  

    for thr in threads:
        thr.join()
      
