import socket
import json
import base64
import logging

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False


def remote_upload(nama_file, b64_string):
    command_str = f"UPLOAD {nama_file} {b64_string}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("File berhasil diupload ke server.")
        return True
    else:
        print("Gagal mengupload file.")
        return False


def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"File '{filename}' berhasil dihapus.")
        return True
    else:
        print(f"Gagal menghapus file: {hasil['data']}")
        return False

if __name__ == '__main__':
    server_address=('172.16.16.101',9090)
    logging.basicConfig(level=logging.WARNING)
    print("=== Remote File Client ===")
    while True:
        print("\nMenu:")
        print("1. List file di server")
        print("2. Download file dari server")
        print("3. Upload file ke server")
        print("4. Hapus file di server")
        print("5. Keluar")
        pilihan = input("Pilih opsi (1-5): ")

        if pilihan == '1':
            remote_list()
        elif pilihan == '2':
            nama_file = input("Masukkan nama file yang ingin didownload: ")
            remote_get(nama_file)
        elif pilihan == '3':
            nama_file = input("Masukkan nama file yang akan disimpan di server (contoh: test.txt): ")
            b64_data = input("Masukkan isi file dalam bentuk base64: ")
            remote_upload(nama_file, b64_data)

        elif pilihan == '4':
            nama_file = input("Masukkan nama file yang ingin dihapus di server: ")
            remote_delete(nama_file)
        elif pilihan == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
