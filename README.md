KAREEM NET FRED
Overview

KAREEM NET FRED is a powerful command-line tool designed to help users maintain anonymity and enhance their digital privacy by automatically changing both their IP address via the Tor network and their MAC address. It is especially useful for security researchers, journalists, activists, and privacy-conscious individuals operating in sensitive environments.


Key Features

    Automatically change your IP address through the Tor network.

    Change MAC address randomly or set a specific one.

    Option to enable or disable MAC address changing.

    Send real-time notifications to a Telegram bot.

    Log all IP and MAC changes locally in a structured format.

    Display geolocation details (country and city) for each new IP address.

    Easy-to-use interactive terminal interface.

    Dark web resource access links provided (requires Tor).


    
Who Is This Tool For?

This tool is intended for:

    Cybersecurity professionals and penetration testers

    Journalists and whistleblowers who need to stay anonymous

    Activists and researchers working under surveillance-heavy conditions

    Anyone concerned about digital privacy and online tracking


    How It Works

    Tor Integration: The tool connects to the Tor service and sends a signal to request a new identity (new circuit), which results in a new external IP address.

    MAC Address Spoofing: The tool uses standard Linux commands (ifconfig, ip, or macchanger) to reset and spoof the MAC address of the selected network interface.

    Geolocation Lookup: It queries external services to detect the geolocation of both old and new IPs.

    Telegram Notifications: When enabled, a notification with full IP and MAC change details is sent to your Telegram bot using your provided credentials.

    Logging: All changes are stored in a log file as structured JSON entries including timestamp, IP, location, and MAC details (if applicable).



    Usage Instructions

    Run the Script
    Make sure the script has executable permissions, and then run it using Python 3:

python3 kareem_net_fred.py

Initial Setup

    The tool will check for dependencies and start the Tor service if it’s not running.

    You will be prompted to configure:

        Tor ports

        MAC address change settings

        IP logging

        Telegram notifications (optional)

Main Menu Options

    Change IP only

    Change MAC only

    Change both IP and MAC

    Access hidden web resources

    Configure Telegram

    Configure MAC changer

    Exit

Change Loop Mode

    Set an interval (e.g. every 30 seconds) to change your identity continuously.

    You can stop the loop at any time with Ctrl+C.



    Requirements

    Linux-based system (recommended: Debian/Ubuntu)

    Python 3

    Tor service (sudo apt install tor)

    macchanger (if using MAC spoofing)

    Internet connection

Notes

    This tool requires root privileges to change network configurations.

    You must be connected to the Tor network to access .onion links.

    Always use responsibly and in accordance with the laws and regulations in your country.

Disclaimer

KAREEM NET FRED is intended for educational and ethical use only. The developer is not responsible for any misuse of this tool.
