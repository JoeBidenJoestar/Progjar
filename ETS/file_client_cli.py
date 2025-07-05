import base64
import socket
import argparse
import time
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError

DEFAULT_SERVER_IP = '172.16.16.101'
DEFAULT_SERVER_PORT = 6666
TIMEOUT_LIMIT = 180  # seconds per test combo

# Predefined volumes
VOLUMES = {'10MB':10*1024*1024, '50MB':50*1024*1024, '100MB':100*1024*1024}


def send_command(cmd_str, server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        s.sendall((cmd_str + '\r\n\r\n').encode())
        data = b""
        while not data.endswith(b'\r\n\r\n'):
            part = s.recv(4096)
            if not part:
                break
            data += part
    try:
        return json.loads(data.decode().rstrip('\r\n'))
    except Exception:
        return {'status':'ERROR','data':'Invalid response'}


def stress_test_worker(op, filename, b64_data, server_ip, server_port):
    start = time.time()
    success = False
    size = 0
    try:
        if op == 'download':
            res = send_command(f'DOWNLOAD {filename}', server_ip, server_port)
            if res.get('status') == 'OK':
                data = base64.b64decode(res.get('data','').encode())
                size = len(data)
                success = True
        else:  # upload
            res = send_command(f'UPLOAD {filename} {b64_data}', server_ip, server_port)
            if res.get('status') == 'OK':
                size = len(b64_data.encode())
                success = True
    except Exception:
        success = False
    elapsed = time.time() - start
    return success, elapsed, size


def run_single_test(op, size_label, client_workers, server_ip, server_port):
    # Prepare dummy data for upload
    b64_data = base64.b64encode(b'a' * VOLUMES[size_label]).decode()
    # If download test, ensure sample file exists on server
    if op == 'download':
        fname = f'stress_{size_label}_sample.dat'
        send_command(f'UPLOAD {fname} {b64_data}', server_ip, server_port)
    successes = 0
    failures = 0
    total_elapsed = 0.0
    total_bytes = 0
    start_combo = time.time()

    with ThreadPoolExecutor(max_workers=client_workers) as executor:
        futures = []
        for i in range(client_workers):
            if time.time() - start_combo > TIMEOUT_LIMIT:
                break
            if op == 'download':
                filename = f'stress_{size_label}_sample.dat'
            else:
                filename = f'stress_{size_label}_{i}.dat'
            futures.append(executor.submit(
                stress_test_worker, op, filename, b64_data if op=='upload' else None, server_ip, server_port))
        for f in futures:
            remaining = TIMEOUT_LIMIT - (time.time() - start_combo)
            if remaining <= 0:
                failures += len(futures) - (successes + failures)
                break
            try:
                ok, elapsed, sz = f.result(timeout=remaining)
                if ok:
                    successes +=1
                    total_elapsed += elapsed
                    total_bytes += sz
                else:
                    failures +=1
            except TimeoutError:
                failures +=1
    wall_clock = time.time() - start_combo
    avg_time = total_elapsed / successes if successes else 0
    throughput = total_bytes / total_elapsed if total_elapsed else 0
    print(f"Results for {op.upper()} size={size_label} cw={client_workers}")
    print(f"Success: {successes}, Failures: {failures}")
    print(f"Avg time/client: {avg_time:.2f}s")
    print(f"Throughput/client: {throughput:.2f} bytes/s")
    if wall_clock > TIMEOUT_LIMIT:
        print(f"Test exceeded {TIMEOUT_LIMIT}s (wall-clock {wall_clock:.2f}s)")


def main():
    p = argparse.ArgumentParser(description='Stress Test Client Single Combo')
    p.add_argument('--op', choices=['download','upload'], required=True, help='Operation')
    p.add_argument('--size', choices=list(VOLUMES.keys()), required=True, help='File size label')
    p.add_argument('--workers', type=int, required=True, help='Number of client workers')
    p.add_argument('--server-ip', default=DEFAULT_SERVER_IP)
    p.add_argument('--server-port', type=int, default=DEFAULT_SERVER_PORT)
    args = p.parse_args()
    run_single_test(args.op, args.size, args.workers, args.server_ip, args.server_port)

if __name__ == '__main__':
    main()
