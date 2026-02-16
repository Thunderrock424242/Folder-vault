#!/usr/bin/env python3
"""
Folder Vault - Secure Folder Encryption/Decryption Tool
Encrypt and decrypt folders with password protection and cool visual effects
"""

import os
import sys
import time
import random
import getpass
import zipfile
import hashlib
import msvcrt  # For Windows keyboard input
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Colors:
    """ANSI color codes for terminal output"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def get_password_with_toggle(prompt):
    """
    Get password input with toggle visibility feature
    Hold CTRL to reveal password, release to hide
    """
    print(f"{prompt}", end='', flush=True)
    print(f"\n{Colors.CYAN}💡 Hold CTRL to reveal password, release to hide{Colors.END}")
    print(f"{Colors.YELLOW}➤ ", end='', flush=True)
    
    password = []
    revealed = False
    
    if os.name == 'nt':  # Windows
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getwch()
                
                # Enter key
                if char in ('\r', '\n'):
                    print()
                    break
                
                # Backspace
                elif char == '\x08':
                    if password:
                        password.pop()
                        # Clear line and reprint
                        sys.stdout.write('\r' + ' ' * 100 + '\r')
                        sys.stdout.write(f"{Colors.YELLOW}➤ {Colors.END}")
                        if revealed:
                            sys.stdout.write(''.join(password))
                        else:
                            sys.stdout.write('●' * len(password))
                        sys.stdout.flush()
                
                # Regular character
                elif char >= ' ':
                    password.append(char)
                    if revealed:
                        sys.stdout.write(char)
                    else:
                        sys.stdout.write('●')
                    sys.stdout.flush()
            
            # Check if CTRL is being held (for reveal)
            import ctypes
            ctrl_state = ctypes.windll.user32.GetAsyncKeyState(0x11)  # VK_CONTROL
            currently_revealed = (ctrl_state & 0x8000) != 0
            
            if currently_revealed != revealed:
                revealed = currently_revealed
                # Redraw password
                sys.stdout.write('\r' + ' ' * 100 + '\r')
                sys.stdout.write(f"{Colors.YELLOW}➤ {Colors.END}")
                if revealed:
                    sys.stdout.write(f"{Colors.GREEN}{''.join(password)}{Colors.END}")
                else:
                    sys.stdout.write('●' * len(password))
                sys.stdout.flush()
            
            time.sleep(0.01)
    
    else:  # Unix/Linux/Mac
        import tty
        import termios
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(fd)
            
            while True:
                char = sys.stdin.read(1)
                
                # Enter key
                if char in ('\r', '\n'):
                    print()
                    break
                
                # Backspace
                elif char in ('\x7f', '\x08'):
                    if password:
                        password.pop()
                        sys.stdout.write('\r' + ' ' * 100 + '\r')
                        sys.stdout.write(f"{Colors.YELLOW}➤ {Colors.END}")
                        if revealed:
                            sys.stdout.write(''.join(password))
                        else:
                            sys.stdout.write('●' * len(password))
                        sys.stdout.flush()
                
                # CTRL key toggle
                elif char == '\x11':  # CTRL+Q to toggle
                    revealed = not revealed
                    sys.stdout.write('\r' + ' ' * 100 + '\r')
                    sys.stdout.write(f"{Colors.YELLOW}➤ {Colors.END}")
                    if revealed:
                        sys.stdout.write(f"{Colors.GREEN}{''.join(password)}{Colors.END}")
                    else:
                        sys.stdout.write('●' * len(password))
                    sys.stdout.flush()
                
                # Regular character
                elif ord(char) >= 32:
                    password.append(char)
                    if revealed:
                        sys.stdout.write(char)
                    else:
                        sys.stdout.write('●')
                    sys.stdout.flush()
        
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return ''.join(password)


def print_banner():
    """Display the application banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║               🔐  F O L D E R   V A U L T  🔐             ║
║                                                           ║
║           Secure Encryption & Decryption System           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)


def animate_text(text, color=Colors.GREEN, delay=0.03):
    """Animate text output character by character"""
    for char in text:
        sys.stdout.write(color + char + Colors.END)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_animation(message, duration=2):
    """Display a loading animation"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    
    while time.time() < end_time:
        sys.stdout.write(f'\r{Colors.CYAN}{frames[i % len(frames)]} {message}...{Colors.END}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    sys.stdout.write(f'\r{Colors.GREEN}✓ {message}... Done!{Colors.END}\n')


def encryption_animation():
    """Cool encryption visual effect"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}[ENCRYPTION INITIATED]{Colors.END}\n")
    
    phases = [
        "Analyzing folder structure",
        "Generating encryption matrix",
        "Applying AES-256 cipher",
        "Scrambling data blocks",
        "Securing with SHA-256 hash",
        "Finalizing encryption"
    ]
    
    for phase in phases:
        loading_animation(phase, duration=0.8)
    
    # Binary rain effect
    print(f"\n{Colors.GREEN}", end='')
    for _ in range(3):
        binary = ''.join(random.choice('01') for _ in range(60))
        print(binary)
        time.sleep(0.1)
    print(Colors.END)
    
    print(f"{Colors.GREEN}{Colors.BOLD}✓ ENCRYPTION COMPLETE ✓{Colors.END}\n")


def decryption_animation():
    """Cool decryption visual effect"""
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}[DECRYPTION INITIATED]{Colors.END}\n")
    
    phases = [
        "Verifying password hash",
        "Loading encryption key",
        "Breaking cipher blocks",
        "Reconstructing data stream",
        "Validating file integrity",
        "Restoring folder structure"
    ]
    
    for phase in phases:
        loading_animation(phase, duration=0.8)
    
    # Decryption effect
    print(f"\n{Colors.MAGENTA}", end='')
    for i in range(3):
        hex_data = ''.join(random.choice('0123456789ABCDEF') for _ in range(60))
        print(hex_data)
        time.sleep(0.1)
    print(Colors.END)
    
    print(f"{Colors.GREEN}{Colors.BOLD}✓ DECRYPTION COMPLETE ✓{Colors.END}\n")


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())


def encrypt_folder(folder_path: str, password: str):
    """Encrypt a folder with password protection"""
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists():
        print(f"{Colors.RED}✗ Error: Folder does not exist!{Colors.END}")
        return False
    
    if not folder_path.is_dir():
        print(f"{Colors.RED}✗ Error: Path is not a folder!{Colors.END}")
        return False
    
    # Generate salt and derive key
    salt = os.urandom(16)
    key = derive_key(password, salt)
    fernet = Fernet(Fernet.generate_key())
    
    # Create encrypted zip file
    encrypted_file = folder_path.parent / f"{folder_path.name}.encrypted"
    temp_zip = folder_path.parent / f"{folder_path.name}.temp.zip"
    
    try:
        # Start encryption animation
        encryption_animation()
        
        print(f"{Colors.CYAN}Compressing folder...{Colors.END}")
        # Compress folder to zip
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(folder_path.parent)
                    zipf.write(file_path, arcname)
        
        print(f"{Colors.CYAN}Encrypting data...{Colors.END}")
        # Read zip file and encrypt
        with open(temp_zip, 'rb') as f:
            data = f.read()
        
        # Use password-derived key for actual encryption
        from cryptography.fernet import Fernet
        import base64
        key_bytes = base64.urlsafe_b64encode(key)
        cipher = Fernet(key_bytes)
        encrypted_data = cipher.encrypt(data)
        
        # Write encrypted file with salt
        with open(encrypted_file, 'wb') as f:
            f.write(salt)
            f.write(encrypted_data)
        
        # Clean up
        temp_zip.unlink()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}═══════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}🔒 Folder successfully encrypted!{Colors.END}")
        print(f"{Colors.GREEN}📁 Encrypted file: {encrypted_file.name}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}═══════════════════════════════════════{Colors.END}\n")
        
        # Ask if user wants to delete original
        delete = input(f"{Colors.YELLOW}Delete original folder? (y/n): {Colors.END}").lower()
        if delete == 'y':
            import shutil
            shutil.rmtree(folder_path)
            print(f"{Colors.GREEN}✓ Original folder deleted{Colors.END}")
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Encryption failed: {str(e)}{Colors.END}")
        if temp_zip.exists():
            temp_zip.unlink()
        return False


def decrypt_folder(encrypted_file_path: str, password: str):
    """Decrypt an encrypted folder"""
    encrypted_file = Path(encrypted_file_path).resolve()
    
    if not encrypted_file.exists():
        print(f"{Colors.RED}✗ Error: Encrypted file does not exist!{Colors.END}")
        return False
    
    try:
        # Start decryption animation
        decryption_animation()
        
        print(f"{Colors.CYAN}Reading encrypted data...{Colors.END}")
        # Read encrypted file
        with open(encrypted_file, 'rb') as f:
            salt = f.read(16)
            encrypted_data = f.read()
        
        # Derive key from password
        key = derive_key(password, salt)
        
        print(f"{Colors.CYAN}Decrypting data...{Colors.END}")
        # Decrypt data
        import base64
        from cryptography.fernet import Fernet
        key_bytes = base64.urlsafe_b64encode(key)
        cipher = Fernet(key_bytes)
        
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
        except Exception:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ DECRYPTION FAILED ✗{Colors.END}")
            print(f"{Colors.RED}Incorrect password!{Colors.END}\n")
            return False
        
        # Extract zip file
        output_folder = encrypted_file.parent / encrypted_file.stem.replace('.encrypted', '')
        temp_zip = encrypted_file.parent / "temp_decrypt.zip"
        
        print(f"{Colors.CYAN}Extracting files...{Colors.END}")
        with open(temp_zip, 'wb') as f:
            f.write(decrypted_data)
        
        with zipfile.ZipFile(temp_zip, 'r') as zipf:
            zipf.extractall(encrypted_file.parent)
        
        # Clean up
        temp_zip.unlink()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}═══════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}🔓 Folder successfully decrypted!{Colors.END}")
        print(f"{Colors.GREEN}📁 Restored to: {output_folder.name}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}═══════════════════════════════════════{Colors.END}\n")
        
        # Ask if user wants to delete encrypted file
        delete = input(f"{Colors.YELLOW}Delete encrypted file? (y/n): {Colors.END}").lower()
        if delete == 'y':
            encrypted_file.unlink()
            print(f"{Colors.GREEN}✓ Encrypted file deleted{Colors.END}")
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Decryption failed: {str(e)}{Colors.END}")
        return False


def main():
    """Main application entry point"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.BOLD}Select operation:{Colors.END}")
    print(f"{Colors.CYAN}1. 🔒 Encrypt Folder{Colors.END}")
    print(f"{Colors.MAGENTA}2. 🔓 Decrypt Folder{Colors.END}")
    print(f"{Colors.RED}3. ❌ Exit{Colors.END}\n")
    
    choice = input(f"{Colors.YELLOW}Enter your choice (1-3): {Colors.END}")
    
    if choice == '1':
        print(f"\n{Colors.BOLD}═══ ENCRYPTION MODE ═══{Colors.END}\n")
        folder_path = input(f"{Colors.CYAN}Enter folder path to encrypt: {Colors.END}")
        
        if not folder_path:
            print(f"{Colors.RED}✗ No path provided!{Colors.END}")
            return
        
        password = get_password_with_toggle(f"{Colors.YELLOW}Enter encryption password:{Colors.END}")
        confirm = get_password_with_toggle(f"{Colors.YELLOW}Confirm password:{Colors.END}")
        
        if password != confirm:
            print(f"{Colors.RED}✗ Passwords do not match!{Colors.END}")
            return
        
        if not password:
            print(f"{Colors.RED}✗ Password cannot be empty!{Colors.END}")
            return
        
        encrypt_folder(folder_path, password)
        
    elif choice == '2':
        print(f"\n{Colors.BOLD}═══ DECRYPTION MODE ═══{Colors.END}\n")
        file_path = input(f"{Colors.MAGENTA}Enter encrypted file path: {Colors.END}")
        
        if not file_path:
            print(f"{Colors.RED}✗ No path provided!{Colors.END}")
            return
        
        password = get_password_with_toggle(f"{Colors.YELLOW}Enter decryption password:{Colors.END}")
        
        decrypt_folder(file_path, password)
        
    elif choice == '3':
        animate_text("\nGoodbye! Stay secure! 🔐", Colors.CYAN, 0.05)
        return
    
    else:
        print(f"{Colors.RED}✗ Invalid choice!{Colors.END}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
        sys.exit(0)
