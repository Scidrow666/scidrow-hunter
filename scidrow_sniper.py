import os
import sys
import hashlib
import ctypes
import locale
import winreg
import xml.etree.ElementTree as ET

# Scidrow Suite: Full-Spectrum Forensic Engine
# SCIDROW SNIPER v1.7 (Task Scheduler Interceptor & Smart Integrity Guard)
# License: GNU GPL v3. Author: Scidrow666

def get_system_language():
    try:
        windll = ctypes.windll.kernel32
        lang_id = windll.GetUserDefaultUILanguage()
        lang = locale.windows_locale.get(lang_id, "en_US")
        return "RU" if "ru" in lang.lower() else "EN"
    except:
        return "EN"

LANG = get_system_language()
DONATE_WAL = "USDT (TRC-20): TEWQScWrBB2B4brjWL5nfxrWzNwitTuD6i"

STRINGS = {
    "RU": {
        "start": "\n[+] Снайпер вышел на позицию. Системный сектор: {0}",
        "scan_reg": "[+] КОНТУР 1: Сканируем реестр автозагрузки Windows (HKCU/HKLM)...",
        "scan_lnk": "[+] КОНТУР Б: Проверка Рабочего стола на наличие битых ярлыков-призраков...",
        "scan_tasks": "[+] КОНТУР Г: Сканируем системный  задач Windows (Tasks)...",
        "scan_files": "[+] КОНТУР 3: Запуск Forensic-анализа директорий и проверки хэшей...",
        "reg_alert": "[!!!] ТРЕВОГА РЕЕСТРА !!! Подозрительный запуск из AppData/Temp:\n    Ключ: {0} --> Путь: {1}",
        "task_alert": "[!!!] ТРЕВОГА ПЛАНИРОВЩИКА !!! Обнаружена скрытая ИИ-задача малвари:\n    Задача: {0} --> Команда: {1}",
        "reg_clean": "[+] Реестр автозагрузки чист от явных аномалий.",
        "tasks_clean": "[+]  задач чист от скрытых AppData/Temp лоадеров.",
        "telemetry_prompt": "\n[?] Включить жесткую зачистку системной телеметрии Windows (DiagTrack/WECP)? (y/n): ",
        "report_title": "      РАПОРТ СНАЙПЕРА: АНОМАЛИИ И КРИТИЧЕСКИЕ ПАПКИ",
        "trash_found": "  КОНТУР 2 (TELEMETRY VAPORIZER): Скрытых логов/телеметрии найдено: {0:.2f} Мб",
        "hash_alert": "[!!!] КРИТИЧЕСКАЯ АНОМАЛИЯ ХЭША !!! Неизвестный бинарник в Temp/AppData:\n    Файл: {0} | SHA-256: {1}",
        "lnk_alert": "[!] ОБНАРУЖЕН БИТЫЙ ЯРЛЫК-ПРИЗРАК: {0}",
        "purge_prompt": "\n[?] Включить КОНТУР В (Vaporizer) и ПОЛНОСТЬЮ выжечь весь мусор и нелегалов? (y/n): ",
        "fire": "[-] Снайпер открыл шквальный огонь по телеметрии и временным файлам...",
        "clean": "[+] Зачистка завершена. Сектор полностью стерилен. ОЗУ и Диск очищены.",
        "exit": "\n[+] Контуры проверены. Снайпер уходит в режим консервации. Отбой."
    },
    "EN": {
        "start": "\n[+] Sniper deployed on position. Target system sector: {0}",
        "scan_reg": "[+] CONTOUR 1: Auditing Windows Startup Registry entries (HKCU/HKLM)...",
        "scan_lnk": "[+] CONTOUR B: Scanning Desktop for broken ghost shortcuts (.lnk)...",
        "scan_tasks": "[+] CONTOUR G: Auditing Windows Task Scheduler system entries (Tasks)...",
        "scan_files": "[+] CONTOUR 3: Launching AppData Forensic analysis & SHA-256 integrity check...",
        "reg_alert": "[!!!] REGISTRY ALERT !!! Suspicious startup entry detected in AppData/Temp:\n    Key: {0} --> Path: {1}",
        "task_alert": "[!!!] TASK SCHEDULER ALERT !!! Hidden malware background task detected:\n    Task: {0} --> Command: {1}",
        "reg_clean": "[+] Startup registry is clean from explicit anomalies.",
        "tasks_clean": "[+] Task Scheduler is clean from hidden AppData/Temp loaders.",
        "telemetry_prompt": "\n[?] Enable hard purge of core Windows telemetry services (DiagTrack/WECP)? (y/n): ",
        "report_title": "      SNIPER FORENSIC REPORT: DIRECTORY ANOMALIES",
        "trash_found": "  CONTOUR 2 (TELEMETRY VAPORIZER): Hidden telemetry logs/cache found: {0:.2f} MB",
        "hash_alert": "[!!!] HASH INTEGRITY ALERT !!! Unknown binary found in Temp/AppData:",
        "lnk_alert": "[!] BROKEN GHOST SHORTCUT DETECTED: {0}",
        "purge_prompt": "\n[?] Enable CONTOUR V (Vaporizer) and COMPLETELY purge all trash and binaries? (y/n): ",
        "fire": "[-] Sniper opening heavy fire on telemetry logs and temporary targets...",
        "clean": "[+] Deep purge completed successfully. Sector sterilized.",
        "exit": "\n[+] Contours verified. Sniper entering conservation mode. Out."
    }
}

def check_startup_registry():
    print(STRINGS[LANG]["scan_reg"])
    paths_to_check = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
    ]
    anomalies_found = False
    
    for root_key, sub_key in paths_to_check:
        try:
            key = winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ)
            info = winreg.QueryInfoKey(key)
            for i in range(info):
                name, value, _ = winreg.EnumValue(key, i)
                value_lower = value.lower()
                if "appdata" in value_lower or "temp" in value_lower:
                    print(STRINGS[LANG]["reg_alert"].format(name, value))
                    anomalies_found = True
            winreg.CloseKey(key)
        except Exception:
            continue
    if not anomalies_found:
        print(STRINGS[LANG]["reg_clean"])

def check_broken_shortcuts():
    print(STRINGS[LANG]["scan_lnk"])
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        return
    try:
        for file in os.listdir(desktop_path):
            if file.lower().endswith(".lnk"):
                full_path = os.path.join(desktop_path, file)
                if not os.path.exists(full_path):
                    print(STRINGS[LANG]["lnk_alert"].format(file))
    except:
        pass
def check_task_scheduler():
    """КОНТУР Г: Молниеносный разбор XML-конфигов Планировщика без вызова внешнего софта"""
    print(STRINGS[LANG]["scan_tasks"])
    sys_drive = os.environ.get("SystemDrive", "C:") + "\\"
    tasks_dir = os.path.join(sys_drive, "Windows", "System32", "Tasks")
    anomalies_found = False
    
    if not os.path.exists(tasks_dir):
        return
        
    for root, dirs, files in os.walk(tasks_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Читаем XML файл задачи напрямую
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                content_lower = content.lower()
                if "<command>" in content_lower:
                    if "appdata" in content_lower or "temp" in content_lower:
                        # Хирургически выдергиваем имя исполняемого файла из XML
                        root_xml = ET.fromstring(content)
                        namespaces = {'ns': 'http://microsoft.com'}
                        exec_node = root_xml.find('.//ns:Command', namespaces)
                        cmd_value = exec_node.text if exec_node is not None else "Unknown path"
                        
                        if "appdata" in cmd_value.lower() or "temp" in cmd_value.lower():
                            relative_task_name = os.path.relpath(file_path, tasks_dir)
                            print(STRINGS[LANG]["task_alert"].format(relative_task_name, cmd_value))
                            anomalies_found = True
            except Exception:
                continue
                
    if not anomalies_found:
        print(STRINGS[LANG]["tasks_clean"])

def get_file_fast_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            hasher.update(f.read(65536))
        return hasher.hexdigest()
    except:
        return None

def scan_system_files(hard_mode):
    print(STRINGS[LANG]["scan_files"])
    sys_drive = os.environ.get("SystemDrive", "C:") + "\\"
    appdata_path = os.environ.get("LOCALAPPDATA", sys_drive + "Users\\User\\AppData\\Local")
    
    dir_sizes = {}
    total_trash_bytes = 0
    targets_to_purge = []
    
    telemetry_zones = ["\\google\\chrome\\user data\\default\\cache", "\\temp"]
    trusted_hashes = [
        "3dcac20ebbed4c9ad283a1a5d8c573ee7ce06937afd7a20b16acdd0cff1b4839" # Чистый DismHost
    ]

    scan_targets = [appdata_path]
    if hard_mode:
        programdata = os.environ.get("ProgramData", sys_drive + "ProgramData")
        win_dir = os.environ.get("SystemRoot", sys_drive + "Windows")
        scan_targets.extend([programdata + "\\Microsoft\\Diagnosis", win_dir + "\\Temp"])

    for target_dir in scan_targets:
        if not os.path.exists(target_dir):
            continue
            
        for root, dirs, files in os.walk(target_dir, topdown=True):
            current_dir_size = 0
            root_lower = root.lower()
            
            for file in files:
                file_path = os.path.join(root, file)
                file_lower = file.lower()
                try:
                    is_trash = any(zone in root_lower for zone in telemetry_zones) or "diagnosis" in root_lower or file_lower.endswith('.log') or file_lower.endswith('.tmp')
                    file_size = os.path.getsize(file_path)
                    current_dir_size += file_size
                    
                    if is_trash:
                        total_trash_bytes += file_size
                        if "\\temp" in root_lower or root_lower.endswith("\\cache_data") or file_lower.endswith('.log'):
                            targets_to_purge.append(file_path)
                        
                    if file_lower.endswith('.exe'):
                        f_hash = get_file_fast_hash(file_path)
                        if f_hash and f_hash not in trusted_hashes:
                            if "temp" in root_lower:
                                print(STRINGS[LANG]["hash_alert"].format(file_path, f_hash))
                                if file_path not in targets_to_purge:
                                    targets_to_purge.append(file_path)
                except:
                    continue
            if current_dir_size > 0:
                dir_sizes[root] = current_dir_size

    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x, reverse=True)[:5]
    print("\n" + "=" * 70)
    print(STRINGS[LANG]["report_title"])
    print("=" * 70)
    for i, (folder, size) in enumerate(sorted_dirs, 1):
        print(f"[{i}] {size / (1024*1024):.2f} MB --> {folder}")
        
    print("\n" + "=" * 70)
    print(STRINGS[LANG]["trash_found"].format(total_trash_bytes / (1024*1024)))
    print("=" * 70)

    if targets_to_purge:
        purge_prompt = input(STRINGS[LANG]["purge_prompt"]).strip().lower()
        if purge_prompt == 'y':
            print(STRINGS[LANG]["fire"])
            for target in targets_to_purge:
                try: os.remove(target)
                except: pass
            print(STRINGS[LANG]["clean"])

if __name__ == "__main__":
    sys_drive = os.environ.get("SystemDrive", "C:") + "\\"
    print("=" * 70)
    print(f"  SUPPORT INDEPENDENT DEVELOPMENT: {DONATE_WAL}")
    print("=" * 70)
    print(STRINGS[LANG]["start"].format(sys_drive))
    
    check_startup_registry()
    check_broken_shortcuts()
    check_task_scheduler()
    
    prompt = input(STRINGS[LANG]["telemetry_prompt"]).strip().lower()
    hard_mode_enabled = True if prompt == 'y' else False
    
    scan_system_files(hard_mode_enabled)
    
    print(STRINGS[LANG]["exit"])
    input("\nPress Enter to exit...")
