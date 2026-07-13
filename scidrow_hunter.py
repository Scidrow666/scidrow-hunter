import psutil
import os
import sys
import time
import webbrowser
import hashlib
import threading

# ГЛОБАЛЬНЫЙ МЕЖДУНАРОДНЫЙ БЕЛЫЙ СПИСОК (Специфический софт, базы и ядра систем)
WHITELIST_PROCESSES = [
    "chrome.exe", "totalcmd.exe", "discord.exe", "eurotrucks2.exe", "gta5.exe",
    "firefox.exe", "opera.exe", "msedge.exe", "brave.exe", "browser.exe", 
    "steam.exe", "epicgameslauncher.exe", "viber.exe", "telegram.exe",
    "far.exe", "explorer.exe", "svchost.exe", "spoolsv.exe", "lsass.exe",
    "mysqld.exe", "postgres.exe", "oracle.exe", "sqlservr.exe", "nginx.exe",
    "services.exe", "wininit.exe", "csrss.exe", "smss.exe", "winlogon.exe",
    "backgroundtaskhost.exe", "msmpeng.exe", "mpdefendercoreservice.exe", 
    "officeclicktorun.exe", "smartscreen.exe", "system", "sidebar.exe", "officec2rclient.exe",
    "msedgewebview2.exe", "microsoftedgeupdate.exe", "updater.exe", "msoia.exe",
    "compattelrunner.exe", "sdxhelper.exe", "windowspackagemanagerserver.exe", "acdseefreeintouch2.exe",
    "radeonsoftware.exe", "amdrsserv.exe", "vulkaninfo.exe",
    "nvcontainer.exe", "nvdisplay.container.exe", "nvidia share.exe", "igfxcuiservice.exe"
]

SYSTEM_TRUSTED_PARENTS = ["services.exe", "explorer.exe", "wininit.exe", "smss.exe", "svchost.exe", "none"]

# Подозрительные внешние порты, которые хакеры часто используют для C2-панелей стилеров
SUSPICIOUS_HACKER_PORTS = [8080, 4444, 2222, 1337, 6667, 9999]

HASH_CACHE = {}

def get_process_hash(file_path):
    """Молниеносное снятие SHA-256 хэша с кэшированием в ОЗУ для Phenom II"""
    if file_path in HASH_CACHE:
        return HASH_CACHE[file_path]
    try:
        if not file_path or not os.path.exists(file_path):
            return None
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()
        HASH_CACHE[file_path] = file_hash
        return file_hash
    except:
        return None

def check_stealer_file_access(process_obj):
    """КОНТУР DPAPI И TDATA: Контролируем попытки левых процессов залезть в Chrome и Telegram"""
    try:
        open_files = process_obj.open_files()
        for f in open_files:
            f_path_lower = f.path.lower()
            # Проверка атаки на Google Chrome
            if "google\\chrome" in f_path_lower and any(m in f_path_lower for m in ["login data", "local state", "cookies"]):
                return "CHROME_ATTACK"
            # Проверка атаки на Telegram Desktop
            if "telegram desktop" in f_path_lower and "tdata" in f_path_lower:
                return "TELEGRAM_ATTACK"
    except:
        pass
    return None
def scan_network_threats():
    found_threats = 0
    
    totalcmd_reference_hash = None
    for p in psutil.process_iter(['name', 'exe']):
        try:
            if p.info['name'] == 'totalcmd.exe' and p.info['exe']:
                totalcmd_reference_hash = get_process_hash(p.info['exe'])
                break
        except:
            continue

    for conn in psutil.net_connections(kind='inet'):
        if conn.status in ['LISTEN', 'ESTABLISHED', 'SYN_SENT']:
            pid = conn.pid
            if pid:
                try:
                    process = psutil.Process(pid)
                    proc_name = process.name().lower()
                    
                    parent_flag = False
                    fake_flag = False
                    stealer_file_compromise = None
                    suspicious_port_flag = False
                    anti_sleep_flag = False
                    parent_name = "none"
                    
                    # 1. КОНТУР РОДОСЛОВНОЙ (Parent PID Checking против Люмы)
                    try:
                        parent_proc = process.parent()
                        if parent_proc:
                            parent_name = parent_proc.name().lower()
                            try: parent_path = parent_proc.exe().lower()
                            except: parent_path = ""
                            
                            if any(zone in parent_path for zone in ["temp", "appdata", "downloads"]):
                                parent_flag = True
                    except:
                        pass

                    # 2. КОНТУР КОНТРОЛЯ ЦЕЛОСТНОСТИ БЕЛОГО СПИСКА
                    if proc_name in WHITELIST_PROCESSES:
                        if proc_name == "totalcmd.exe" and totalcmd_reference_hash:
                            try:
                                current_hash = get_process_hash(process.exe())
                                if current_hash and current_hash != totalcmd_reference_hash:
                                    fake_flag = True
                            except:
                                pass
                        
                        try: exe_path_check = process.exe().lower()
                        except: exe_path_check = ""
                            
                        if "system32" in exe_path_check or "syswow64" in exe_path_check:
                            if parent_name not in SYSTEM_TRUSTED_PARENTS or parent_flag:
                                parent_flag = True
                            else:
                                if not fake_flag: continue
                        else:
                            if not parent_flag and not fake_flag: continue

                    # 3. КОНТУР НАПРАВЛЕННОГО DPAPI И TDATA ПЕРЕХВАТА АТАК
                    if proc_name not in ["chrome.exe", "telegram.exe", "explorer.exe"]:
                        stealer_file_compromise = check_stealer_file_access(process)

                    # 4. КОНТУР CANARY PORTS (Прямой обход DNS на хакерские C2)
                    if conn.raddr and conn.raddr.port in SUSPICIOUS_HACKER_PORTS:
                        if proc_name not in WHITELIST_PROCESSES:
                            suspicious_port_flag = True

                    # 5. КОНТУР ANTI-SLEEP (Вычисляем замороженных во времени шпионов)
                    try:
                        p_time = process.cpu_times()
                        if p_time.user == 0.0 and p_time.system == 0.0:
                            try: p_exe = process.exe().lower()
                            except: p_exe = ""
                            if any(zone in p_exe for zone in ["temp", "appdata", "downloads"]):
                                anti_sleep_flag = True
                    except:
                        pass

                    try: exe_path = process.exe()
                    except: exe_path = "СКРЫТЫЙ СИСТЕМНЫЙ ПРОЦЕСС (Подозрение на Injection!)"

                    exe_path_lower = exe_path.lower()
                    is_suspicious_zone = any(zone in exe_path_lower for zone in ["temp", "appdata", "downloads"])
                    
                    # МОЩНЫЙ СИНТЕЗИРОВАННЫЙ ТРИГГЕР НА ВЫЖИГАНИЕ УГРОЗЫ
                    if (is_suspicious_zone or parent_flag or fake_flag or 
                        stealer_file_compromise or suspicious_port_flag or 
                        anti_sleep_flag or exe_path.startswith("СКРЫТЫЙ")):
                        
                        found_threats += 1
                        print("\n[!!!] ВНИМАНИЕ!!! ОБНАРУЖЕН ПЕРЕХВАЧЕННЫЙ СПУТНИК/СТИЛЕР !!!")
                        print(f"ПРОЦЕСС: {proc_name} | PID: ({pid})")
                        print(f"ФИЗИЧЕСКИЙ ПУТЬ: {exe_path}")
                        
                        if parent_flag:
                            print(f"[!] АНОМАЛИЯ РОДОСЛОВНОЙ: Системная маскировка нарушена! Родитель: {parent_name}")
                        if fake_flag:
                            print("[!] АНОМАЛИЯ ЦЕЛОСТНОСТИ: Обнаружен клон-подделка под оригинальное имя!")
                        if stealer_file_compromise == "CHROME_ATTACK":
                            print("[!] АТАКА НА КРИПТО-ЯДРО: Процесс скрытно читает базу паролей Хрома!")
                        if stealer_file_compromise == "TELEGRAM_ATTACK":
                            print("[!] УГОН СЕССИИ: Процесс тайно копирует файлы tdata Вашего Telegram!")
                        if suspicious_port_flag:
                            print(f"[!] ОБХОД DNS (CANARY PORT): Прямое подключение к хакерскому C2-порту ({conn.raddr.port})!")
                        if anti_sleep_flag:
                            print("[!] АНТИ-ЗАМОРОЗКА: Обнаружен спящий скрытый процесс в режиме ожидания таймера!")
                            
                        print(f"ЛОКАЛЬНЫЙ ПОРТ: ({conn.laddr.port}) | Удаленный: ({conn.raddr.port if conn.raddr else 'Слушает'})")
                        
                        print("[!] МАНЕВР: Scidrow Hunter силой ликвидирует угрозу...")
                        try: process.terminate()
                        except: pass
                        if parent_flag and parent_name != "none":
                            try: parent_proc.terminate()
                            except: pass
                        print("[+] УСПЕХ: Канал утечки данных намертво заблокирован.")
                        continue

                    # 6. КОНТУР НЕИЗВЕСТНЫХ ПРОЦЕССОВ В СЕТИ (Подавление левой активности)
                    if conn.status == 'ESTABLISHED' and not proc_name in WHITELIST_PROCESSES:
                        found_threats += 1
                        print(f"\n[!] КРИТИЧЕСКАЯ ТРЕВОГА !!! Процесс [{proc_name}] (PID: {pid}) активно сливает данные через порт ({conn.laddr.port})")
                        try: process.terminate()
                        except: pass
                        print("[+] УСПЕХ: Подозрительная сетевая активность подавлена.")
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

def background_customs_officer():
    """Наш бессмертный круглосуточный таможенник на границе сетевой карты"""
    while True:
        scan_network_threats()
        time.sleep(5)  # Сканируем каждые 5 секунд — быстро и без очередей в ОЗУ

if __name__ == "__main__":
    print("======================================================================")
    print("                SCIDROW HUNTER v2.3.4 (Rocket Edition)")
    print("      Continuous Behavioral Anti-Stealer | License: GNU GPL v3")
    print("======================================================================")
    print("USDT (TRC-20) Wallet Address: TEWQScWrBB2B4brjWL5nfxrWzNwitTuD6i\n")
    print("[+] Пассивный радар запущен. Таможня работает в фоновом режиме (5 сек)...")
    
    customs_thread = threading.Thread(target=background_customs_officer, daemon=True)
    customs_thread.start()
    
    while True:
        print("\n[КОМАНДНЫЙ ПУНКТ] Системы в норме. Периметр под круглосуточной охраной.")
        print("1. Открыть страницу проекта на GitHub")
        print("2. Полный выход (Закрыть таможню)")
        
        choice = input("\nВыберите маневр (1-2): ")
        if choice == "1":
            webbrowser.open("https://github.com")
        elif choice == "2":
            print("[+] Закрываем таможенный пост. Отбой, Капитан.")
            sys.exit()
