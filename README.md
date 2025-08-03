#KAREEM NET FRED – Advanced Anonymity Toolkit

KAREEM NET FRED is an advanced Python framework for online anonymity, created for cybersecurity researchers and privacy professionals. It provides a complete toolkit for rotating IP addresses through Tor, spoofing MAC addresses, sending secure Telegram notifications, and keeping detailed logs — all through an organized command‑line interface.



span style="color:#1E90FF; font-size:30px;">Core Features</span>
<span style="color:#1E90FF; font-size:24px;">Tor IP Rotation</span>

    Automatic IP rotation using Tor’s NEWNYM signal via the ControlPort (default: 9051).

    Multiple IP verification sources (Tor Project, ipify, ipwhois).

    Automatic Tor service restart if rotation fails.

    Configurable SOCKS5 proxy ports (default: 9050).


    <span style="color:#1E90FF; font-size:24px;">MAC Address Spoofing</span>

    Three fallback methods for MAC spoofing: macchanger, ifconfig, and ip link.

    Random MAC generation with proper unicast formatting.

    Option to set a specific MAC address with format validation.

    Default interface detection (eth0) with manual override support.



    <span style="color:#1E90FF; font-size:24px;">Geolocation Intelligence</span>

    Country and city lookup through dual APIs (ipapi.co and ipwhois).

    Tracks visited countries and cities with first and last seen timestamps.

    Maintains a full transition chain of IP routes.



    <span style="color:#1E90FF; font-size:24px;">Security Systems</span>

    Secure Telegram token entry using getpass, ensuring it is never printed to screen.

    No sensitive credentials stored in plaintext.

    Automatic detection if the MAC reverts to its original hardware address.



    <span style="color:#1E90FF; font-size:24px;">Notification Systems</span>

    Telegram alerts formatted in HTML for clear, structured messages.

    Logging of every change in JSONL format for analysis.

    Color‑coded terminal messages for real‑time feedback.



    <span style="color:#1E90FF; font-size:30px;">Advanced Functionality</span>

    Automatic dependency handling for multiple Linux distributions (Debian, RHEL, Arch).

    Automatic installation of required Python packages (stem, requests, python‑telegram‑bot).

    Real IP detection (bypassing Tor) and multi‑method MAC verification.

    Persistent session tracking with detailed movement history.



    <span style="color:#1E90FF; font-size:30px;">Installation</span>

    # Debian/Ubuntu
sudo apt install tor macchanger python3-pip
sudo systemctl enable --now tor

# RHEL/Fedora
sudo yum install tor macchanger python3-pip
sudo systemctl enable --now tor

# Python dependencies
pip install -r requirements.txt




If you don’t have a requirements.txt file, you can install the needed packages manually:

pip install stem requests python-telegram-bot



<span style="color:#1E90FF; font-size:30px;">Usage</span>

python3 KAREEM_NET_FRED.py


The tool will:

    Verify and install missing dependencies.

    Detect and configure Tor ports (or allow you to set them manually).

    Ask whether to enable logging.

    Display the main menu with the following options:

        Change IP

        Change MAC

        Change both IP and MAC

        Access Dark Web links

        Configure Telegram notifications

        Configure Tor ports

        Configure MAC changer settings

        Exit



        <span style="color:#1E90FF; font-size:30px;">Security Notes</span>

        sudo systemctl start tor



    Changing the MAC address may temporarily interrupt the network connection.

    Telegram credentials are never displayed or stored in plaintext.



<span style="color:#1E90FF; font-size:30px;">Code Structure Overview</span>


check_requirements() – Checks for system and Python dependencies.

detect_tor_ports() – Reads torrc configuration to detect ports.

get_ip() – Retrieves the current Tor IP.

change_tor_ip() – Sends the NEWNYM signal to Tor.

get_location_for_ip() – Finds the country and city of the current IP.

change_mac_address() – Changes MAC address with fallback methods.

send_telegram_notification() – Sends updates via Telegram.

log_ip_change() – Logs all IP and MAC changes.

main_menu() – Provides the CLI interface for all functions.
