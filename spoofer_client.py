import sys  # Provides system-specific functions and parameters
import os  # Used for interacting with the operating system
import subprocess  # Allows running system commands
import requests  # Handles HTTP requests to validate activation keys
import hashlib  # Provides hashing algorithms for integrity checks
import winreg  # Enables interaction with the Windows registry
import random  # Generates random values
import string  # Provides string manipulation functions
import uuid  # Generates universally unique identifiers (UUIDs)
import logging  # Import logging module
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, \
    QVBoxLayout, QWidget, QComboBox, QTextEdit, QInputDialog, QMessageBox  # Imports PyQt6 UI components
from PyQt6.QtCore import Qt  # Provides core Qt functionality

# Set up logging
log_file = os.path.join(os.path.dirname(sys.executable), "spoofer_client.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --Anti-Debugging Check ---
# This detects if a debugger is attached to the process. If detected, the program exits.
if sys.gettrace() is not None:
    logging.error("Debugger detected! Exiting.")  # Log a warning message
    sys.exit(1)  # Exit the program to prevent debugging

# --- Self-Integrity Check ---
# Ensures the script hasn't been modified by comparing its SHA-256 hash to a known value.
def check_integrity():
    current_file = __file__  # Get the current script's filename
    with open(current_file, "rb") as f:  # Open the script in binary mode
        content = f.read()  # Read the entire content of the script
    current_hash = hashlib.sha256(content).hexdigest()  # Compute the SHA-256 hash
    EXPECTED_HASH = "85f29e214d3915ce8c97d8c42d86a3288b0d6ee36bd2ab00500e9ebfd5cc9c7b"  # Placeholder for the expected hash value
    if current_hash != EXPECTED_HASH:  # Compare the calculated hash with the expected hash
        logging.error("Integrity check failed! Exiting.")  # Log an error message if hashes do not match
        sys.exit(1)  # Exit the program

# --- Fake Reverse Engineering Trap ---
# This function is designed to mislead reverse engineers.
def fake_reverse_engineering_trap():
    dummy = 0  # Initialize a dummy variable
    for i in range(1000):  # Perform a meaningless computation
        dummy += i  # Increment the dummy variable
    logging.info("Fake reverse-engineering trap executed.")  # Log a misleading message

# --- Generate Random Spoofing Values ---
def generate_random_serial():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))  # Generate a random 15-character alphanumeric string

def generate_random_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])  # Generate a random MAC address

def generate_random_uuid():
    return str(uuid.uuid4())  # Generate a random UUID

# --- Spoof Motherboard Serial ---
def spoof_motherboard_serial():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS", 0, winreg.KEY_WRITE)  # Open the BIOS registry key with write access
        new_serial = generate_random_serial()  # Generate a new random serial
        winreg.SetValueEx(key, "SystemSerialNumber", 0, winreg.REG_SZ, new_serial)  # Set the new serial number in the registry
        winreg.CloseKey(key)  # Close the registry key
        logging.info(f"Motherboard Serial spoofed to: {new_serial}")  # Log confirmation
        return True  # Return success
    except Exception as e:
        logging.error(f"Error spoofing Motherboard Serial: {e}")  # Log an error message if an exception occurs
        return False  # Return failure

# --- Spoof Disk Drive ID ---
def spoof_disk_drive_id():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\SCSI", 0, winreg.KEY_WRITE)  # Open the registry key for disk drives
        new_disk_id = generate_random_serial()  # Generate a new random disk ID
        winreg.SetValueEx(key, "Identifier", 0, winreg.REG_SZ, new_disk_id)  # Set the new disk ID
        winreg.CloseKey(key)  # Close the registry key
        logging.info(f"Disk Drive ID spoofed to: {new_disk_id}")  # Log confirmation
        return True  # Return success
    except Exception as e:
        logging.error(f"Error spoofing Disk Drive ID: {e}")  # Log an error message if an exception occurs
        return False  # Return failure

# --- Spoof MAC Address ---
def spoof_mac_address():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\0001", 0, winreg.KEY_WRITE)  # Open the registry key for network adapters
        new_mac = generate_random_mac().replace(':', '-')  # Generate a new MAC address and format it for Windows
        winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)  # Set the new MAC address
        winreg.CloseKey(key)  # Close the registry key
        logging.info(f"MAC Address spoofed to: {new_mac}")  # Log confirmation
        return True  # Return success
    except Exception as e:
        logging.error(f"Error spoofing MAC Address: {e}")  # Log an error message if an exception occurs
        return False  # Return failure

# --- Modify Registry Keys ---
def modify_registry_keys():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\IDConfigDB", 0, winreg.KEY_WRITE)  # Open the registry key for hardware identifiers
        new_hardware_id = generate_random_uuid()  # Generate a new random UUID
        winreg.SetValueEx(key, "HardwareID", 0, winreg.REG_SZ, new_hardware_id)  # Set the new Hardware ID
        winreg.CloseKey(key)  # Close the registry key
        logging.info(f"Registry keys modified to: {new_hardware_id}")  # Log confirmation
        return True  # Return success
    except Exception as e:
        logging.error(f"Error modifying registry keys: {e}")  # Log an error message if an exception occurs
        return False  # Return failure

def main():
    check_integrity()
    fake_reverse_engineering_trap()
    spoof_motherboard_serial()
    spoof_disk_drive_id()
    spoof_mac_address()
    modify_registry_keys()
    
    # Add other initialization logic here
    logging.info("Spoofer client started.")

if __name__ == "__main__":
    main()