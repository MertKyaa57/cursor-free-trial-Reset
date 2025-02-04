import json
import os
import uuid
import shutil
from datetime import datetime
import platform
import subprocess
import time
import sys
from colorama import init, Fore, Back, Style

# Colorama'yı başlat
init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def print_banner():
    banner = f"""{Fore.BLUE}
    ██████╗██╗   ██╗██████╗ ███████╗ ██████╗ ██████╗     ██████╗ ██████╗  ██████╗ 
    ██╔════╝██║   ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗
    ██║     ██║   ██║██████╔╝███████╗██║   ██║██████╔╝    ██████╔╝██████╔╝██║   ██║
    ██║     ██║   ██║██╔══██╗╚════██║██║   ██║██╔══██╗    ██╔═══╝ ██╔══██╗██║   ██║
    ╚██████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║    ██║     ██║  ██║╚██████╔╝
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                                                                                    
    {Style.BRIGHT}[ Free Trial Sıfırlama Aracı | Geliştirici: @MertKyaa57 ]{Style.RESET_ALL}
    """
    print(banner)

def loading_animation(duration):
    total = 100
    for i in range(total + 1):
        sys.stdout.write('\r')
        bar = f"{Fore.BLUE}[{('■' * i) + ('□' * (total-i))}]{Style.RESET_ALL}"
        sys.stdout.write(f"{bar} {Fore.CYAN}{i}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(duration/total)
    print("\n")

def kill_cursor():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(['taskkill', '/F', '/IM', 'cursor.exe'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        elif system == "Darwin":  # macOS
            subprocess.run(['pkill', '-f', 'Cursor'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}[✓] Cursor kapatıldı. İşlem başlıyor...{Style.RESET_ALL}")
        time.sleep(1)
    except:
        print(f"{Fore.YELLOW}[❗] Cursor zaten kapalı. İşleme devam ediliyor...{Style.RESET_ALL}")

def get_cursor_path():
    system = platform.system()
    if system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Cursor")
    elif system == "Windows":
        return os.path.expandvars("%APPDATA%\\Cursor")
    else:
        raise OSError("Desteklenmeyen işletim sistemi")

def generate_ids():
    return {
        "telemetry.machineId": str(uuid.uuid4()).replace("-", ""),
        "telemetry.devDeviceId": str(uuid.uuid4()),
        "telemetry.macMachineId": str(uuid.uuid4()).replace("-", "") * 2,
        "telemetry.sqmId": ""
    }

def backup_config(cursor_path):
    backup_dir = os.path.join(cursor_path, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    storage_path = os.path.join(cursor_path, "User", "globalStorage", "storage.json")
    if os.path.exists(storage_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"storage_backup_{timestamp}.json")
        shutil.copy2(storage_path, backup_path)
        print(f"{Fore.GREEN}✓ Yedek oluşturuldu: {Style.BRIGHT}{backup_path}{Style.RESET_ALL}")
    
def reset_cursor():
    try:
        print_banner()
        print(f"{Fore.BLUE}{'='*75}{Style.RESET_ALL}")
        
        # Önce Cursor'u kapat
        kill_cursor()
        
        print(f"\n{Fore.CYAN}[⌛] Yedekleme yapılıyor...{Style.RESET_ALL}")
        loading_animation(2)
        
        cursor_path = get_cursor_path()
        storage_path = os.path.join(cursor_path, "User", "globalStorage", "storage.json")
        
        # Yedekleme yap
        backup_config(cursor_path)
        
        print(f"\n{Fore.CYAN}[⚡] Yeni kimlikler oluşturuluyor...{Style.RESET_ALL}")
        loading_animation(2)
        
        # Mevcut yapılandırmayı oku
        if os.path.exists(storage_path):
            with open(storage_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Yeni ID'leri oluştur ve güncelle
        new_ids = generate_ids()
        config.update(new_ids)
        
        print(f"\n{Fore.CYAN}[💾] Değişiklikler kaydediliyor...{Style.RESET_ALL}")
        loading_animation(1)
        
        # Yapılandırmayı kaydet
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        
        print(f"\n{Fore.BLUE}{'='*75}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✅] Cursor başarıyla sıfırlandı!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Yeni ID'ler:{Style.RESET_ALL}")
        for key, value in new_ids.items():
            print(f"{Fore.BLUE}[📌] {key}:{Style.RESET_ALL} {value}")
        
        print(f"\n{Fore.YELLOW}[⚠️] Cursor'u yeniden başlatabilirsiniz!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*75}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}[❌] Hata oluştu: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    reset_cursor()
    input(f"\n{Fore.CYAN}Kapatmak için Enter tuşuna basın...{Style.RESET_ALL}") 