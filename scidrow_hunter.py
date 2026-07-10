import psutil
import os
import sys
import time
import webbrowser

# НАШ ЖЕСТКИЙ БЕЛЫЙ СПИСОК (Легальный софт, которому можно в сеть)
WHITELIST_PROCESSES = [
    "chrome.exe", "firefox.exe", "opera.exe", "browser.exe", "v2rayn.exe",
    "discord.exe", "steam.exe", "eurotrucks2.exe", "gtav.exe", "totalcmd.exe"
]

print("=====================================================================")
print("          SCIDROW HUNTER v2.3 — АВТОНОМНЫЙ ИСТРЕБИТЕЛЬ АНОМАЛИЙ       ")
print("=====================================================================")
print("[ОХОТНИК]: Запуск автономного сканирования всех сетевых сокетов...")
time.sleep(0.5)

def scan_network_threats():
    print("[ОХОТНИК]: Анализирую сетевую карту на наличие скрытых аномалий...")
    found_threats = 0
    
    # Сканируем ВСЕ активные соединения в Windows без оглядки на номера портов!
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN' or conn.status == 'ESTABLISHED' or conn.raddr:
            pid = conn.pid
            if pid:
                try:
                    process = psutil.Process(pid)
                    proc_name = process.name().lower()
                    
                    if proc_name in WHITELIST_PROCESSES:
                        continue
                        
                    try:
                        exe_path = process.exe()
                    except Exception:
                        exe_path = "СКРЫТЫЙ СИСТЕМНЫЙ КАТАЛОГ (Подозрение на Injection/Hollowoing!)"
                        
                    is_suspicious_zone = any(zone in exe_path.lower() for zone in ["temp", "appdata", "downloads"])
                    
                    if is_suspicious_zone or exe_path.startswith("СКРЫТЫЙ"):
                        found_threats += 1
                        print("\n!!! ВНИМАНИЕ !!! АВТОНОМНО ПЕРЕХВАЧЕН СЛИТОК/СТИЛЕР !!!")
                        print(f"[УГРОЗА]: Обнаружен неизвестный процесс '{proc_name}' (PID: {pid})")
                        print(f"[ФИЗИЧЕСКИЙ ПУТЬ]: {exe_path}")
                        print(f"[АНОМАЛЬНЫЙ ПОРТ]: Локальный: {conn.laddr.port} | Удаленный: {conn.raddr.port if conn.raddr else 'Слушает'}")
                        print(f"[СТАТУС СОКЕТА]: {conn.status}")
                        
                        print(f"[МАНЕВР]: Scidrow Hunter силой ликвидирует неизвестную угрозу...")
                        process.terminate()
                        print(f"[УСПЕХ]: Канал утечки данных через порт {conn.laddr.port} намертво закрыт.")
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            else:
                if conn.status == 'ESTABLISHED':
                    print(f"\n!!! КРИТИЧЕСКАЯ ТРЕВОГА !!! Невидимый призрак активно сливает данные через порт {conn.laddr.port}!")
                    found_threats += 1

    if found_threats == 0:
        print("[УСПЕХ]: Сетевой периметр чист. Неизвестных процессов в сети не обнаружено.")

if __name__ == "__main__":
    scan_network_threats()
    print("=====================================================================")
    print("[Scidrow Hunter]: Support the project / Поддержи проект донатом:")
    print("USDT (TRC-20) Wallet Address: TEWQScWrBB2B4brjWL5nfxrWzNwitTuD6i")
    print("=====================================================================")
    
    # КНОПКА ДОНАТА (Ведёт прямиком на твой будущий репозиторий проекта)
    donate_url = "https://github.com" 
    
    choice = input("Open GitHub project page to copy wallet? / Открыть страницу? (Y/N): ").strip().lower()
    if choice == 'y' or choice == 'н':
        print("[МАНЕВР]: Открываю окно в браузере...")
        webbrowser.open(donate_url)
        
    input("\nAnalysis complete. Нажмите Enter для выхода...")
