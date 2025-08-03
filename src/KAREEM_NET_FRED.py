#!/usr/bin/env python3
import time
import requests
import uuid
import os
import subprocess
from stem import Signal
from stem.control import Controller
import json
from datetime import datetime
import getpass
from collections import OrderedDict
import re
import random

# Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Default configuration
TOR_SOCKS_PROXY = "socks5h://127.0.0.1:9050"
TOR_CONTROL_PORT = 9051

# Telegram Configuration
TELEGRAM_BOT_TOKEN = None
TELEGRAM_CHAT_ID = None
TELEGRAM_ENABLED = False

# Logging Configuration
LOG_ENABLED = False
LOG_FILE = "KAREEM_NET_FRED.log"

# MAC Address Configuration
MAC_CHANGE_ENABLED = False
MAC_CHANGE_METHOD = None  # 'random', 'specific'
NEW_MAC = None
DEFAULT_INTERFACE = "eth0"

# Session tracking
visited_countries = OrderedDict()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_requirements():
    """Check system requirements and attempt to install missing ones"""
    requirements = {
        'tor': {'installed': False, 'name': 'Tor Service'},
        'stem': {'installed': False, 'name': 'Stem Package'},
        'requests': {'installed': False, 'name': 'Requests Package'},
        'python-telegram-bot': {'installed': False, 'name': 'Python-Telegram-Bot'},
        'macchanger': {'installed': False, 'name': 'Macchanger Tool'}
    }
    
    print(f"\n{YELLOW}[*] Checking system requirements:{RESET}\n")
    
    # Check Tor service
    try:
        subprocess.check_output(['which', 'tor'], stderr=subprocess.STDOUT)
        requirements['tor']['installed'] = True
        print(f"{GREEN}[✓] {requirements['tor']['name']} is installed{RESET}")
    except:
        print(f"{RED}[✗] {requirements['tor']['name']} is not installed{RESET}")
    
    # Check Python packages
    try:
        import stem
        requirements['stem']['installed'] = True
        print(f"{GREEN}[✓] {requirements['stem']['name']} is installed{RESET}")
    except:
        print(f"{RED}[✗] {requirements['stem']['name']} is not installed{RESET}")
    
    try:
        import requests
        requirements['requests']['installed'] = True
        print(f"{GREEN}[✓] {requirements['requests']['name']} is installed{RESET}")
    except:
        print(f"{RED}[✗] {requirements['requests']['name']} is not installed{RESET}")
    
    try:
        import telegram
        requirements['python-telegram-bot']['installed'] = True
        print(f"{GREEN}[✓] {requirements['python-telegram-bot']['name']} is installed{RESET}")
    except:
        print(f"{RED}[✗] {requirements['python-telegram-bot']['name']} is not installed{RESET}")
    
    # Check macchanger
    try:
        subprocess.check_output(['which', 'macchanger'], stderr=subprocess.STDOUT)
        requirements['macchanger']['installed'] = True
        print(f"{GREEN}[✓] {requirements['macchanger']['name']} is installed{RESET}")
    except:
        print(f"{RED}[✗] {requirements['macchanger']['name']} is not installed{RESET}")
    
    # Install missing requirements
    if not all([req['installed'] for req in requirements.values()]):
        print(f"\n{YELLOW}[*] Attempting to install missing requirements...{RESET}\n")
        
        if not requirements['tor']['installed']:
            print(f"{YELLOW}[*] Installing Tor...{RESET}")
            try:
                if os.path.exists('/etc/debian_version'):
                    subprocess.run(['sudo', 'apt', 'update'], check=True)
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], check=True)
                elif os.path.exists('/etc/redhat-release'):
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'tor'], check=True)
                elif os.path.exists('/etc/arch-release'):
                    subprocess.run(['sudo', 'pacman', '-Sy', '--noconfirm', 'tor'], check=True)
                else:
                    print(f"{RED}[!] Could not detect package manager to install Tor{RESET}")
                    print(f"{YELLOW}[!] Please install Tor manually{RESET}")
                    return False
                
                # Start Tor service
                subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
                subprocess.run(['sudo', 'systemctl', 'enable', 'tor'], check=True)
                requirements['tor']['installed'] = True
                print(f"{GREEN}[✓] Tor installed and started successfully{RESET}")
            except Exception as e:
                print(f"{RED}[!] Failed to install Tor: {str(e)}{RESET}")
                print(f"{YELLOW}[!] Please install Tor manually{RESET}")
        
        if not requirements['macchanger']['installed']:
            print(f"{YELLOW}[*] Installing macchanger...{RESET}")
            try:
                if os.path.exists('/etc/debian_version'):
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'macchanger'], check=True)
                elif os.path.exists('/etc/redhat-release'):
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'macchanger'], check=True)
                elif os.path.exists('/etc/arch-release'):
                    subprocess.run(['sudo', 'pacman', '-Sy', '--noconfirm', 'macchanger'], check=True)
                else:
                    print(f"{RED}[!] Could not detect package manager to install macchanger{RESET}")
                    print(f"{YELLOW}[!] Please install macchanger manually{RESET}")
                
                requirements['macchanger']['installed'] = True
                print(f"{GREEN}[✓] Macchanger installed successfully{RESET}")
            except Exception as e:
                print(f"{RED}[!] Failed to install macchanger: {str(e)}{RESET}")
                print(f"{YELLOW}[!] Please install macchanger manually{RESET}")
        
        # Install Python packages
        missing_packages = []
        if not requirements['stem']['installed']:
            missing_packages.append('stem')
        if not requirements['requests']['installed']:
            missing_packages.append('requests')
        if not requirements['python-telegram-bot']['installed']:
            missing_packages.append('python-telegram-bot')
        
        if missing_packages:
            print(f"{YELLOW}[*] Installing Python packages: {', '.join(missing_packages)}{RESET}")
            try:
                subprocess.run(['pip3', 'install'] + missing_packages, check=True)
                for pkg in missing_packages:
                    if pkg == 'stem':
                        requirements['stem']['installed'] = True
                    elif pkg == 'requests':
                        requirements['requests']['installed'] = True
                    elif pkg == 'python-telegram-bot':
                        requirements['python-telegram-bot']['installed'] = True
                print(f"{GREEN}[✓] Python packages installed successfully{RESET}")
            except Exception as e:
                print(f"{RED}[!] Failed to install Python packages: {str(e)}{RESET}")
                print(f"{YELLOW}[!] Please install them manually with: pip3 install {' '.join(missing_packages)}{RESET}")
    
    # Final check
    if all([req['installed'] for req in requirements.values()]):
        print(f"\n{GREEN}[✓] All requirements are installed!{RESET}")
        time.sleep(2)
        return True
    else:
        print(f"\n{RED}[!] Some requirements are still missing{RESET}")
        print(f"{YELLOW}[!] Please install them manually before continuing{RESET}")
        time.sleep(3)
        return False

def detect_tor_ports():
    """Detect Tor ports from torrc configuration file"""
    socks_port = 9050  # Default
    control_port = 9051  # Default
    
    torrc_paths = [
        '/etc/tor/torrc',
        '/usr/local/etc/tor/torrc',
        '/etc/torrc',
        os.path.expanduser('~/.torrc')
    ]
    
    for path in torrc_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('SocksPort') and not line.startswith('#'):
                            parts = line.split()
                            if len(parts) >= 2:
                                socks_port = int(parts[1])
                        elif line.startswith('ControlPort') and not line.startswith('#'):
                            parts = line.split()
                            if len(parts) >= 2:
                                control_port = int(parts[1])
            except:
                continue
    
    return socks_port, control_port

def configure_tor_ports():
    """Allow user to configure Tor ports manually"""
    global TOR_SOCKS_PROXY, TOR_CONTROL_PORT
    
    socks_port, control_port = detect_tor_ports()
    
    print(f"\n{YELLOW}[*] Current Tor Port Configuration:{RESET}")
    print(f"{GREEN}[+] SOCKS Proxy Port: {BLUE}{socks_port}{RESET}")
    print(f"{GREEN}[+] Control Port: {BLUE}{control_port}{RESET}")
    
    while True:
        choice = input(f"\n{YELLOW}[*] Do you want to change these ports? (y/n): {RESET}").strip().lower()
        
        if choice == 'n':
            TOR_SOCKS_PROXY = f"socks5h://127.0.0.1:{socks_port}"
            TOR_CONTROL_PORT = control_port
            print(f"{GREEN}[✓] Using detected ports{RESET}")
            time.sleep(2)
            return
        
        elif choice == 'y':
            try:
                new_socks = input(f"{YELLOW}[*] Enter new SOCKS port (current {socks_port}): {RESET}").strip()
                new_control = input(f"{YELLOW}[*] Enter new Control port (current {control_port}): {RESET}").strip()
                
                if new_socks:
                    socks_port = int(new_socks)
                if new_control:
                    control_port = int(new_control)
                
                TOR_SOCKS_PROXY = f"socks5h://127.0.0.1:{socks_port}"
                TOR_CONTROL_PORT = control_port
                
                print(f"{GREEN}[✓] Ports updated successfully{RESET}")
                print(f"{GREEN}[+] New SOCKS Proxy: {BLUE}{TOR_SOCKS_PROXY}{RESET}")
                print(f"{GREEN}[+] New Control Port: {BLUE}{TOR_CONTROL_PORT}{RESET}")
                time.sleep(3)
                return
            except ValueError:
                print(f"{RED}[!] Invalid port number. Please enter a valid integer{RESET}")
        else:
            print(f"{RED}[!] Invalid choice. Please enter 'y' or 'n'{RESET}")

def send_telegram_notification(message):
    """Send notification to Telegram bot"""
    if not TELEGRAM_ENABLED:
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code != 200:
            print(f"{RED}[!] Failed to send Telegram notification{RESET}")
    except Exception as e:
        print(f"{RED}[!] Telegram notification error: {str(e)}{RESET}")

def get_ip():
    """Fetch current IP through Tor"""
    proxies = {"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}
    urls = [
        "https://check.torproject.org/api/ip",
        "https://httpbin.org/ip",
        "https://api.ipify.org?format=json"
    ]
    for url in urls:
        try:
            r = requests.get(url, proxies=proxies, timeout=10)
            data = r.json()
            if "IP" in data:
                return data["IP"]
            if "origin" in data:
                return data["origin"]
            if "ip" in data:
                return data["ip"]
        except Exception:
            continue
    return None

def get_location_for_ip(ip):
    """Get country and city for a given IP"""
    if not ip:
        return "Not Defined", "Not Defined"

    try:
        r_country = requests.get(f"https://ipapi.co/{ip}/country_name/", timeout=10)
        r_city = requests.get(f"https://ipapi.co/{ip}/city/", timeout=10)
        if r_country.status_code == 200 and r_city.status_code == 200:
            country = r_country.text.strip()
            city = r_city.text.strip()

            # Track visited countries
            if country != "Not Defined":
                if country not in visited_countries:
                    visited_countries[country] = {
                        'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'last_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'cities': set([city])
                    }
                else:
                    visited_countries[country]['last_seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    visited_countries[country]['cities'].add(city)

            return country, city
    except:
        pass

    try:
        r = requests.get(f"https://ipwhois.app/json/{ip}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            country = data.get("country", "Not Defined")
            city = data.get("city", "Not Defined")

            # Track visited countries
            if country != "Not Defined":
                if country not in visited_countries:
                    visited_countries[country] = {
                        'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'last_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'cities': set([city])
                    }
                else:
                    visited_countries[country]['last_seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    visited_countries[country]['cities'].add(city)

            return country, city
    except:
        pass

    return "Not Defined", "Not Defined"

def change_tor_ip():
    """Send NEWNYM signal to Tor to get new IP"""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
    except Exception as e:
        print(f"{RED}[!] Error changing Tor IP: {str(e)}{RESET}")
        print(f"{YELLOW}[*] Trying to restart Tor service...{RESET}")
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'tor'], check=True)
            time.sleep(5)  # Give Tor time to restart
        except Exception as e:
            print(f"{RED}[!] Failed to restart Tor: {str(e)}{RESET}")

def get_real_ip():
    """Get real IP (not via Tor)"""
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10)
        return r.json()["ip"]
    except:
        return "Not Defined"

def get_current_mac(interface=DEFAULT_INTERFACE):
    """Get current MAC address of specified interface"""
    try:
        result = subprocess.check_output(['ifconfig', interface], stderr=subprocess.STDOUT)
        result = result.decode('utf-8')
        mac_match = re.search(r'ether\s+([0-9a-fA-F:]{17})', result)
        if mac_match:
            return mac_match.group(1)
    except Exception as e:
        print(f"{RED}[!] Error getting MAC address from ifconfig: {str(e)}{RESET}")
    
    # Fallback method 1 - ip link
    try:
        result = subprocess.check_output(['ip', 'link', 'show', interface], stderr=subprocess.STDOUT)
        result = result.decode('utf-8')
        mac_match = re.search(r'link/ether\s+([0-9a-fA-F:]{17})', result)
        if mac_match:
            return mac_match.group(1)
    except Exception as e:
        print(f"{RED}[!] Error getting MAC address from ip link: {str(e)}{RESET}")
    
    # Fallback method 2 - System UUID
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0, 12, 2)])
    except:
        return "Not Defined"

def generate_random_mac():
    """Generate a random MAC address"""
    # The first byte should be even (unicast) and not locally administered
    first_byte = random.randint(0x00, 0x7F) * 2
    mac = [first_byte] + [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join(f"{x:02x}" for x in mac)

def change_mac_address(interface=DEFAULT_INTERFACE):
    """Change MAC address using multiple methods with fallback"""
    global MAC_CHANGE_METHOD, NEW_MAC
    
    original_mac = get_current_mac(interface)
    if original_mac == "Not Defined":
        print(f"{RED}[!] Could not determine current MAC address{RESET}")
        return False
    
    print(f"\n{YELLOW}[*] Current MAC: {BLUE}{original_mac}{RESET}")
    
    methods = [
        ('macchanger', ['sudo', 'macchanger', '-r', interface]),
        ('ifconfig down/up', [
            'sudo', 'ifconfig', interface, 'down',
            '&&', 'sudo', 'ifconfig', interface, 'hw', 'ether', generate_random_mac(),
            '&&', 'sudo', 'ifconfig', interface, 'up'
        ]),
        ('ip link set', [
            'sudo', 'ip', 'link', 'set', interface, 'down',
            '&&', 'sudo', 'ip', 'link', 'set', interface, 'address', generate_random_mac(),
            '&&', 'sudo', 'ip', 'link', 'set', interface, 'up'
        ])
    ]
    
    if MAC_CHANGE_METHOD == 'specific' and NEW_MAC:
        methods.insert(0, ('specific mac', [
            'sudo', 'ifconfig', interface, 'down',
            '&&', 'sudo', 'ifconfig', interface, 'hw', 'ether', NEW_MAC,
            '&&', 'sudo', 'ifconfig', interface, 'up'
        ]))
    
    success = False
    for method_name, cmd in methods:
        try:
            print(f"{YELLOW}[*] Trying method: {method_name}{RESET} \n")
            
            if '&&' in cmd:
                # Handle multiple commands
                full_cmd = ' '.join(cmd)
                subprocess.run(full_cmd, shell=True, check=True)
            else:
                subprocess.run(cmd, check=True)
            
            time.sleep(2)  # Give interface time to reset
            
            new_mac = get_current_mac(interface)
            if new_mac != original_mac and new_mac != "Not Defined":
                print(f"\n{GREEN}[✓] MAC changed successfully using {method_name}{RESET}")
                print(f"{GREEN}[+] New MAC: {BLUE}{new_mac}{RESET}")
                success = True
                break
        except Exception as e:
            print(f"{RED}[!] Failed with {method_name}: {str(e)}{RESET}")
            continue
    
    if not success:
        print(f"{RED}[!] All MAC change methods failed{RESET}")
        return False
    
    return True

def print_banner():
    print(rf"""{BLUE}
     ██╗  ██╗ █████╗ ██████╗ ███████╗███████╗███╗   ███╗    ███╗   ██╗███████╗████████╗
     ██║ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝████╗ ████║    ████╗  ██║██╔════╝╚══██╔══╝
     █████╔╝ ███████║██████╔╝█████╗  █████╗  ██╔████╔██║    ██╔██╗ ██║█████╗     ██║   
     ██╔═██╗ ██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██║╚██╔╝██║    ██║╚██╗██║██╔══╝     ██║   
     ██║  ██╗██║  ██║██║  ██║███████╗███████╗██║ ╚═╝ ██║    ██║ ╚████║███████╗   ██║   
     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝   
     {RESET}
          {YELLOW}
          ███████╗██████╗ ███████╗██████╗ 
          ██╔════╝██╔══██╗██╔════╝██╔══██╗
          █████╗  ██████╔╝█████╗  ██║  ██║
          ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║
          ██║     ██║  ██║███████╗██████╔╝
          ╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝  {GREEN} Freedom Through Anonymity{RESET}

     {YELLOW}[+] IP Changer with Country & City Lookup
     [+] Coded by: Kareem Abdelmuttalib
     [+] Freedom Through Anonymity
     [+] Stay Hidden, Stay Safe{RESET}
     """)

def print_country_chain():
    """Display visited countries chain in a box"""
    if not visited_countries:
        return
    
    countries = list(visited_countries.keys())
    arrow = f"{MAGENTA}→{RESET}"
    country_chain = f" {arrow} ".join(countries)
    
    print(f"\n{YELLOW}┌─────────────────────────────────────────────────────────────────────────────────────────┐")
    print(f"{YELLOW}│ {CYAN}{country_chain}{RESET}")
    print(f"{YELLOW}└─────────────────────────────────────────────────────────────────────────────────────────┘{RESET}")

def setup_telegram():
    """Configure Telegram notifications"""
    global TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
    
    while True:
        enable = input(f"\n{YELLOW}[+] Enable Telegram notifications? (y/n/b for back): {RESET}").strip().lower()
        
        if enable == 'b':
            return 'back'
        elif enable != 'y':
            return
        
        try:
            # Use getpass for secure token input
            TELEGRAM_BOT_TOKEN = getpass.getpass(f"{YELLOW}[+] Enter Telegram bot token (hidden input): {RESET}").strip()
            if not TELEGRAM_BOT_TOKEN:
                print(f"{RED}[!] Token cannot be empty{RESET}")
                continue
                
            TELEGRAM_CHAT_ID = input(f"{YELLOW}[+] Enter Telegram chat ID (or 'b' to go back): {RESET}").strip()
            if TELEGRAM_CHAT_ID.lower() == 'b':
                continue
            
            # Test the connection
            print(f"{YELLOW}[*] Testing Telegram connection...{RESET}")
            test_message = "🔔 <b> IP Changer Notification Test</b>\nThis is a test message to verify Telegram notifications are working."
            send_telegram_notification(test_message)
            
            TELEGRAM_ENABLED = True
            print(f"{GREEN}[✓] Telegram notifications enabled{RESET}")
            time.sleep(2)
            return
        except Exception as e:
            print(f"{RED}[!] Telegram setup failed: {str(e)}{RESET}")
            TELEGRAM_ENABLED = False

def setup_logging():
    """Configure logging of IP changes"""
    global LOG_ENABLED, LOG_FILE
    
    while True:
        enable = input(f"\n{YELLOW}[+] Do you want to log all IP changes to a file? (y/n): {RESET}").strip().lower()
        
        if enable == 'n':
            LOG_ENABLED = False
            print(f"{YELLOW}[*] Logging disabled{RESET}")
            time.sleep(2)
            return
        elif enable == 'y':
            LOG_ENABLED = True
            custom_name = input(f"{YELLOW}[+] Enter log file name (default: KAREEM_NET_FRED.log): {RESET}").strip()
            if custom_name:
                LOG_FILE = custom_name
            print(f"{GREEN}[✓] Logging enabled to file: {BLUE}{LOG_FILE}{RESET}")
            time.sleep(2)
            return
        else:
            print(f"{RED}[!] Invalid choice. Please enter 'y' or 'n'{RESET}")

def setup_mac_changer():
    """Configure MAC address changing options"""
    global MAC_CHANGE_ENABLED, MAC_CHANGE_METHOD, NEW_MAC
    
    while True:
        print(f"\n{YELLOW}[*] MAC Address Changing Options:{RESET}")
        print(f"{GREEN}[1]{RESET} Enable random MAC changing")
        print(f"{GREEN}[2]{RESET} Set specific MAC address       {YELLOW}( {RED}Advanced {YELLOW}){RESET}")
        print(f"{GREEN}[3]{RESET} Disable MAC changing")
        print(f"{GREEN}[4]{RESET} Back to main menu")
        
        choice = input(f"\n{YELLOW}Enter your choice (1-4): {RESET}").strip()
        
        if choice == "1":
            MAC_CHANGE_ENABLED = True
            MAC_CHANGE_METHOD = 'random'
            NEW_MAC = None
            print(f"{GREEN}[✓] Random MAC changing enabled{RESET}")
            time.sleep(2)
            return
        elif choice == "2":
            MAC_CHANGE_ENABLED = True
            MAC_CHANGE_METHOD = 'specific'
            while True:
                NEW_MAC = input(f"{YELLOW}Enter MAC address (format XX:XX:XX:XX:XX:XX): {RESET}").strip()
                if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', NEW_MAC):
                    print(f"{GREEN}[✓] Specific MAC address set: {BLUE}{NEW_MAC}{RESET}")
                    time.sleep(2)
                    return
                else:
                    print(f"{RED}[!] Invalid MAC address format{RESET}")
        elif choice == "3":
            MAC_CHANGE_ENABLED = False
            MAC_CHANGE_METHOD = None
            NEW_MAC = None
            print(f"{YELLOW}[*] MAC changing disabled{RESET}")
            time.sleep(2)
            return
        elif choice == "4":
            return 'back'
        else:
            print(f"{RED}[!] Invalid choice{RESET}")
            time.sleep(1)

def log_ip_change(old_ip, old_country, old_city, new_ip, new_country, new_city, old_mac=None, new_mac=None):
    """Log IP change to file"""
    if not LOG_ENABLED:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "old_ip": old_ip,
        "old_country": old_country,
        "old_city": old_city,
        "new_ip": new_ip,
        "new_country": new_country,
        "new_city": new_city
    }
    
    if old_mac and new_mac:
        log_entry.update({
            "old_mac": old_mac,
            "new_mac": new_mac
        })
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"{RED}[!] Failed to write to log file: {str(e)}{RESET}")

def change_ip_loop():
    """Main loop for changing IP addresses"""
    try:
        interval = input(f"{YELLOW}[*] Enter interval in seconds (default {GREEN}30{YELLOW}, 'b' to go back): {RESET}").strip()
        if interval.lower() == 'b':
            return 'back'
        interval = int(interval) if interval else 30
    except:
        interval = 30

    print(f"\n{GREEN}[+] Starting with interval: {YELLOW}{interval} seconds{RESET}\n")

    while True:
        # Get current state
        old_ip = get_ip()
        old_country, old_city = get_location_for_ip(old_ip)
        old_mac = get_current_mac() if MAC_CHANGE_ENABLED else None
        
        # Change IP
        change_tor_ip()
        time.sleep(10)  # Wait for IP to change
        
        # Change MAC if enabled
        new_mac = None
        if MAC_CHANGE_ENABLED:
            if change_mac_address():
                new_mac = get_current_mac()
            else:
                print(f"{RED}[!] MAC address change failed, continuing with IP change only{RESET}")
        
        # Get new state
        new_ip = get_ip()
        new_country, new_city = get_location_for_ip(new_ip)
        
        # Log the change
        log_ip_change(old_ip, old_country, old_city, new_ip, new_country, new_city, old_mac, new_mac)

        # Prepare messages
        screen_msg = f"""
{GREEN}[+] {GREEN}Identity Changed Successfully!{RESET}
{GREEN}[+]{RESET} Old IP: {BLUE}{old_ip}{RESET} — Country: {BLUE}{old_country}{RESET} — City: {BLUE}{old_city}{RESET}
{GREEN}[+]{RESET} New IP: {BLUE}{new_ip}{RESET} — Country: {BLUE}{new_country}{RESET} — City: {BLUE}{new_city}{RESET}
"""

        if MAC_CHANGE_ENABLED and old_mac and new_mac:
            screen_msg += f"""
{GREEN}[+]{RESET} Old MAC: {BLUE}{old_mac}{RESET}
{GREEN}[+]{RESET} New MAC: {BLUE}{new_mac}{RESET}
"""

        telegram_msg = f"""
🔔 <b>YOUR IDENTITY CHANGED SUCCESSFULLY!</b>

<b>Old IP:</b> <code>{old_ip}</code>
<b>Country:</b> {old_country}
<b>City:</b> {old_city}

<b>New IP:</b> <code>{new_ip}</code>
<b>Country:</b> {new_country}
<b>City:</b> {new_city}
"""

        if MAC_CHANGE_ENABLED and old_mac and new_mac:
            telegram_msg += f"""
<b>Old MAC:</b> <code>{old_mac}</code>
<b>New MAC:</b> <code>{new_mac}</code>
"""

        telegram_msg += f"""
<i>Next change in {interval} seconds...</i>
"""

        # Display on screen
        clear_screen()
        print_banner()
        
        # Display country chain in box
        print_country_chain()
        
        # Display IP details
        print("\n" + screen_msg)
        
        print(f"\n{YELLOW}[*] Next change in {interval} seconds (Ctrl+C to stop){RESET}")
        
        # Send to Telegram
        send_telegram_notification(telegram_msg)
        
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{RED}[!] Stopping IP changer...{RESET}")
            time.sleep(2)
            return

def show_darkweb_links():
    """Display dark web links"""
    print(f"\n{GREEN}[+] Dark Web Links:{RESET}")
    print(f"\n{YELLOW}The Hidden Wiki:")
    print(f"{BLUE}http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page{RESET}")
    print(f"\n{YELLOW}Note: You need to be connected to Tor network to access these links.{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def main_menu():
    """Display the main menu and handle user choices"""
    global MAC_CHANGE_ENABLED, MAC_CHANGE_METHOD, NEW_MAC
    while True:
        clear_screen()
        print_banner()
        
        # Verify Tor is running
        try:
            subprocess.check_output(['systemctl', 'is-active', '--quiet', 'tor'])
        except:
            print(f"\n{YELLOW}[*] Starting Tor service...{RESET}")
            try:
                subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
                time.sleep(3)  # Give Tor time to start
            except Exception as e:
                print(f"{RED}[!] Failed to start Tor: {str(e)}{RESET}")
                input(f"{YELLOW}Press Enter to continue...{RESET}")
                continue

        real_ip = get_real_ip()
        real_mac = get_current_mac()

        print(f"\n{GREEN}[+] Your Real IP: {BLUE}{real_ip}{RESET}")
        print(f"{GREEN}[+] Your MAC: {BLUE}{real_mac}{RESET}")
        print(f"{GREEN}[+] Tor SOCKS Proxy: {BLUE}{TOR_SOCKS_PROXY}{RESET}")
        print(f"{GREEN}[+] Tor Control Port: {BLUE}{TOR_CONTROL_PORT}{RESET}")
        print(f"{GREEN}[+] MAC Changing: {BLUE}{'Enabled' if MAC_CHANGE_ENABLED else 'Disabled'}{RESET}\n")

        print(f"{YELLOW}Menu Options:")
        print(f"{GREEN}[1]{RESET} Change IP")
        print(f"{GREEN}[2]{RESET} Change MAC")
        print(f"{GREEN}[3]{RESET} Change Both IP & MAC")
        print(f"{GREEN}[4]{RESET} Dark Web Links")
        print(f"{GREEN}[5]{RESET} Telegram Notifications     {YELLOW}({GREEN} Now Is Available {YELLOW}){RESET}")
        print(f"{GREEN}[6]{RESET} Configure Tor Ports        {YELLOW}({RED} Advanced {YELLOW}){RESET}")
        print(f"{GREEN}[7]{RESET} Configure MAC Changer      {YELLOW}({RED} Advanced {YELLOW}){RESET} ")
        print(f"{GREEN}[8]{RESET} Exit")

        choice = input(f"\n{YELLOW}[*] Enter your choice (1-8): {RESET}").strip()

        if choice == "1":
            # Temporarily disable MAC changing if enabled
            original_mac_setting = MAC_CHANGE_ENABLED
            MAC_CHANGE_ENABLED = False
            
            result = change_ip_loop()
            if result == 'back':
                MAC_CHANGE_ENABLED = original_mac_setting
                continue
            MAC_CHANGE_ENABLED = original_mac_setting
        elif choice == "2":
            # Change MAC only
            if change_mac_address():
                new_mac = get_current_mac()
                print(f"\n{GREEN}[✓] MAC address changed successfully{RESET}")
                print(f"{GREEN}[+] New MAC: {BLUE}{new_mac}{RESET}")
                input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice == "3":
            # Change both IP and MAC
            result = change_ip_loop()
            if result == 'back':
                continue
        elif choice == "4":
            show_darkweb_links()
        elif choice == "5":
            result = setup_telegram()
            if result == 'back':
                continue
        elif choice == "6":
            configure_tor_ports()
        elif choice == "7":
            result = setup_mac_changer()
            if result == 'back':
                continue
        elif choice == "8":
            print(f"\n{GREEN}[+] Thank you for using KAREEM NET FRED{RESET}")
            break
        else:
            print(f"{RED}[!] Invalid choice{RESET}")
            time.sleep(2)

def main():
    # Initialize global variables
    global MAC_CHANGE_ENABLED, MAC_CHANGE_METHOD, NEW_MAC
    
    # Check requirements
    clear_screen()
    print_banner()
    if not check_requirements():
        print(f"\n{RED}[!] Missing requirements{RESET}")
        input(f"{YELLOW}Press Enter to exit...{RESET}")
        return
    
    # Configure Tor ports
    configure_tor_ports()
    
    # Ask about logging
    setup_logging()
    
    # Start main menu
    main_menu()

if __name__ == "__main__":
    main()
