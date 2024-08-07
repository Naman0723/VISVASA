import os
import sys

def ping_message(host, message):
    for char in message:
        ttl = ord(char)
        os.system(f'ping -t {ttl} {host} -n 1')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sender.py <host> <message>")
        sys.exit(1)

    host = sys.argv[1]
    message = sys.argv[2]

    ping_message(host, message)
    import subprocess
import re

def listen_for_ping():
    host = "your_host_ip"
    cmd = f'ping -t 255 {host}'
    proc =   subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    try:
        while True:
            line = proc.stdout.readline()
            if not line:
                break

            match = re.search(r'TTL=(\d+)', line.decode())
            if match:
                ttl = int(match.group(1))
                if 32 <= ttl <= 126:  # Printable ASCII range
                    char = chr(ttl)
                    print(char, end='', flush=True)

    except KeyboardInterrupt:
        proc.kill()

if __name__ == "__main__":
    listen_for_ping()