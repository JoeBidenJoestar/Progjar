import socket
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json
import base64
from file_protocol import FileProtocol
import argparse
import multiprocessing

fp = FileProtocol()

def process_data_in_process(data_str):
    return fp.proses_string(data_str)

def recv_until(conn, terminator=b"\r\n\r\n"):
    data = b""
    while terminator not in data:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet
    return data

def handle_client(conn, addr):
    logging.warning(f"Handling client {addr} in thread {threading.current_thread().name}")
    try:
        data_bytes = recv_until(conn, b"\r\n\r\n")
        if data_bytes:
            data_str = data_bytes.decode().rstrip("\r\n")
            parts = data_str.split(' ', 2)
            cmd = parts[0].upper()
            if cmd == 'DOWNLOAD':
                if len(parts) < 2:
                    response = json.dumps({'status': 'ERROR', 'data': 'Missing filename for DOWNLOAD'})
                else:
                    filename = parts[1]
                    try:
                        with open(filename, 'rb') as f:
                            content = f.read()
                        b64_content = base64.b64encode(content).decode()
                        response = json.dumps({'status': 'OK', 'data': b64_content})
                    except Exception as e:
                        response = json.dumps({'status': 'ERROR', 'data': str(e)})
                conn.sendall((response + "\r\n\r\n").encode())
            elif cmd == 'UPLOAD':
                if len(parts) < 3:
                    response = json.dumps({'status': 'ERROR', 'data': 'Missing parameters for UPLOAD'})
                else:
                    filename = parts[1]
                    b64_data = parts[2]
                    try:
                        content = base64.b64decode(b64_data.encode())
                        with open(filename, 'wb') as f:
                            f.write(content)
                        response = json.dumps({'status': 'OK', 'data': f'Uploaded {filename}'})
                    except Exception as e:
                        response = json.dumps({'status': 'ERROR', 'data': str(e)})
                conn.sendall((response + "\r\n\r\n").encode())
            else:
                result = fp.proses_string(data_str)
                conn.sendall((result + "\r\n\r\n").encode())
    except Exception as e:
        logging.error(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def multithreading_server(ip='0.0.0.0', port=6666, server_workers=50):
    logging.warning(f"Multithreading Server starting on {(ip, port)} with {server_workers} threads")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    thread_pool = ThreadPoolExecutor(max_workers=server_workers)

    try:
        while True:
            conn, addr = server_socket.accept()
            logging.warning(f"Accepted connection from {addr}")
            thread_pool.submit(handle_client, conn, addr)
    except KeyboardInterrupt:
        logging.warning("Server stopped by user")
    finally:
        server_socket.close()
        thread_pool.shutdown(wait=True)

def multiprocessing_server(ip='0.0.0.0', port=6666, server_workers=50):
    logging.warning(f"Multiprocessing Server starting on {(ip, port)} with {server_workers} processes")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    def worker(sock):
        while True:
            conn, addr = sock.accept()
            handle_client(conn, addr)

    workers = []
    try:
        for _ in range(server_workers):
            p = multiprocessing.Process(target=worker, args=(server_socket,))
            p.start()
            workers.append(p)

        for p in workers:
            p.join()
    except KeyboardInterrupt:
        logging.warning("Server stopped by user")
    finally:
        server_socket.close()
        for p in workers:
            p.terminate()
        for p in workers:
            p.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hybrid File Server with Multi-threading or Multi-processing')
    parser.add_argument('--multithreading-server-workers', type=int, help='Jumlah thread workers untuk server multithreading')
    parser.add_argument('--multiprocessing-server-workers', type=int, help='Jumlah process workers untuk server multiprocessing')
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

    if args.multithreading_server_workers:
        multithreading_server(server_workers=args.multithreading_server_workers)
    elif args.multiprocessing_server_workers:
        multiprocessing_server(server_workers=args.multiprocessing_server_workers)
    else:
        print("Gunakan salah satu: --multithreading-server-workers atau --multiprocessing-server-workers")
