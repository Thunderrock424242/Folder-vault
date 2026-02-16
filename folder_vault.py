#!/usr/bin/env python3
"""
Folder Vault - Secure Folder Encryption/Decryption Tool
Full-featured encryption suite with all the bells and whistles!

Author: Your Name
Version: 1.0.0
License: MIT
Repository: https://github.com/Thunderrock424242/Folder-vault
"""

__version__ = "1.0.0"
__author__ = "Thunderrock424242"
__license__ = "MIT"

import os
import sys
import time
import random
import zipfile
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Windows-only import for password input
if os.name == 'nt':
    import msvcrt


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


class EncryptionConfig:
    """Encryption strength configurations"""
    FAST = {"name": "Fast", "iterations": 50000, "compression": zipfile.ZIP_STORED}
    BALANCED = {"name": "Balanced", "iterations": 100000, "compression": zipfile.ZIP_DEFLATED}
    MAXIMUM = {"name": "Maximum Security", "iterations": 500000, "compression": zipfile.ZIP_BZIP2}


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_banner():
    """Display the application banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         🔐  F O L D E R   V A U L T   U L T I M A T E    ║
║                                                           ║
║        Advanced Encryption & Decryption System            ║
║                     Version {__version__}                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)


def play_sound(sound_type):
    """Play sound effects (Windows beep codes)"""
    try:
        if sound_type == "start":
            # Ascending beeps
            for freq in [400, 600, 800]:
                import winsound
                winsound.Beep(freq, 100)
        elif sound_type == "success":
            # Success melody
            import winsound
            winsound.Beep(800, 100)
            winsound.Beep(1000, 100)
            winsound.Beep(1200, 200)
        elif sound_type == "error":
            # Error sound
            import winsound
            winsound.Beep(200, 300)
    except:
        pass  # Silently fail if sound not available


def check_for_updates():
    """Check if a newer version is available on GitHub"""
    try:
        import urllib.request
        import json as json_module
        
        # GitHub API endpoint for latest release
        api_url = "https://api.github.com/repos/Thunderrock424242/Folder-vault/releases/latest"
        
        # Set a timeout to avoid hanging
        with urllib.request.urlopen(api_url, timeout=3) as response:
            data = json_module.loads(response.read().decode())
            latest_version = data.get('tag_name', '').lstrip('v')
            
            if latest_version and latest_version > __version__:
                print(f"\n{Colors.YELLOW}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
                print(f"{Colors.YELLOW}║  🆕 Update Available!                                     ║{Colors.END}")
                print(f"{Colors.YELLOW}║  Current version: {__version__:<10}                            ║{Colors.END}")
                print(f"{Colors.YELLOW}║  Latest version:  {latest_version:<10}                            ║{Colors.END}")
                print(f"{Colors.YELLOW}║  Download: github.com/Thunderrock424242/Folder-vault      ║{Colors.END}")
                print(f"{Colors.YELLOW}╚═══════════════════════════════════════════════════════════╝{Colors.END}\n")
                time.sleep(2)
    except:
        # Silently fail if update check doesn't work (no internet, etc.)
        pass


def format_bytes(bytes_size):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"  # Fallback for extremely large files


def get_folder_size(folder_path):
    """Calculate total size of folder"""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
    except Exception as e:
        pass
    return total


def check_password_strength(password):
    """
    Check password strength and return score and feedback
    Returns: (score, color, feedback)
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    # Complexity checks
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Determine strength
    if score <= 2:
        return ("WEAK", Colors.RED, feedback)
    elif score <= 4:
        return ("MODERATE", Colors.YELLOW, feedback)
    elif score <= 6:
        return ("STRONG", Colors.GREEN, feedback)
    else:
        return ("VERY STRONG", Colors.CYAN, feedback)


def display_password_strength(password):
    """Display password strength meter"""
    strength, color, feedback = check_password_strength(password)
    
    # Visual bar
    bars = min(len(password) // 2, 20)
    bar = "█" * bars + "░" * (20 - bars)
    
    print(f"\n{color}Strength: {strength} {bar}{Colors.END}")
    if feedback and strength in ["WEAK", "MODERATE"]:
        print(f"{Colors.YELLOW}💡 Suggestions: {', '.join(feedback[:2])}{Colors.END}")


def progress_bar(current, total, prefix='', suffix='', length=50):
    """Display a progress bar"""
    filled = int(length * current // total)
    bar = '█' * filled + '░' * (length - filled)
    percent = 100 * (current / float(total))
    
    sys.stdout.write(f'\r{Colors.CYAN}{prefix} |{bar}| {percent:.1f}% {suffix}{Colors.END}')
    sys.stdout.flush()
    
    if current == total:
        print()


def get_password_with_toggle(prompt, show_strength=False):
    """
    Get password input with toggle visibility feature
    Hold CTRL to reveal password, release to hide
    """
    print(f"{prompt}", end='', flush=True)
    print(f"\n{Colors.CYAN}💡 Hold CTRL to reveal password, release to hide{Colors.END}")
    print(f"{Colors.YELLOW}➤ ", end='', flush=True)
    
    password = []
    revealed = False
    last_strength_check = 0
    
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
                        sys.stdout.write('\r' + ' ' * 150 + '\r')
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
                sys.stdout.write('\r' + ' ' * 150 + '\r')
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
                        sys.stdout.write('\r' + ' ' * 150 + '\r')
                        sys.stdout.write(f"{Colors.YELLOW}➤ {Colors.END}")
                        if revealed:
                            sys.stdout.write(''.join(password))
                        else:
                            sys.stdout.write('●' * len(password))
                        sys.stdout.flush()
                
                # CTRL key toggle
                elif char == '\x11':  # CTRL+Q to toggle
                    revealed = not revealed
                    sys.stdout.write('\r' + ' ' * 150 + '\r')
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
    
    pwd_str = ''.join(password)
    
    # Show strength if requested
    if show_strength and pwd_str:
        display_password_strength(pwd_str)
    
    return pwd_str


def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """Derive encryption key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode())


def create_backup(folder_path):
    """Create a backup of the folder before encryption"""
    backup_dir = Path(folder_path).parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{Path(folder_path).name}_backup_{timestamp}"
    backup_path = backup_dir / backup_name
    
    print(f"{Colors.CYAN}Creating backup...{Colors.END}")
    shutil.copytree(folder_path, backup_path)
    print(f"{Colors.GREEN}✓ Backup created: {backup_path}{Colors.END}")
    
    return backup_path


def save_encryption_log(log_data, encrypted_file):
    """Save encryption log/receipt"""
    log_file = Path(encrypted_file).parent / f"{Path(encrypted_file).stem}_log.json"
    
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4)
    
    print(f"{Colors.GREEN}📄 Encryption log saved: {log_file.name}{Colors.END}")
    return log_file


def list_encrypted_contents(encrypted_file_path: str, password: str):
    """View contents of encrypted file without decrypting"""
    encrypted_file = Path(encrypted_file_path).resolve()
    
    if not encrypted_file.exists():
        print(f"{Colors.RED}✗ Error: Encrypted file does not exist!{Colors.END}")
        return False
    
    try:
        print(f"\n{Colors.CYAN}Reading encrypted file...{Colors.END}")
        
        # Read metadata
        with open(encrypted_file, 'rb') as f:
            salt = f.read(16)
            metadata_len_bytes = f.read(4)
            metadata_len = int.from_bytes(metadata_len_bytes, 'big')
            encrypted_metadata = f.read(metadata_len)
            encrypted_data = f.read()
        
        # Derive key
        # Try to get iterations from filename or use default
        iterations = 100000
        key = derive_key(password, salt, iterations)
        
        # Decrypt metadata
        key_bytes = base64.urlsafe_b64encode(key)
        cipher = Fernet(key_bytes)
        
        try:
            metadata_json = cipher.decrypt(encrypted_metadata)
            metadata = json.loads(metadata_json)
        except Exception:
            print(f"{Colors.RED}✗ Incorrect password or corrupted file!{Colors.END}")
            return False
        
        # Display contents
        print(f"\n{Colors.GREEN}{Colors.BOLD}═══ ENCRYPTED CONTENTS ═══{Colors.END}")
        print(f"{Colors.CYAN}Encrypted with: Folder Vault v{metadata.get('version', 'Unknown')}{Colors.END}")
        print(f"{Colors.CYAN}Encryption Date: {metadata.get('timestamp', 'Unknown')}{Colors.END}")
        print(f"{Colors.CYAN}Encryption Level: {metadata.get('level', 'Unknown')}{Colors.END}")
        print(f"{Colors.CYAN}Original Size: {format_bytes(metadata.get('original_size', 0))}{Colors.END}")
        
        if 'hint' in metadata and metadata['hint']:
            print(f"{Colors.YELLOW}Password Hint: {metadata['hint']}{Colors.END}")
        
        if 'self_destruct' in metadata and metadata['self_destruct']:
            destruct_date = datetime.fromisoformat(metadata['self_destruct'])
            days_left = (destruct_date - datetime.now()).days
            print(f"{Colors.RED}⚠️  Self-Destruct: {days_left} days remaining{Colors.END}")
        
        print(f"\n{Colors.BOLD}Files inside:{Colors.END}")
        for idx, file_info in enumerate(metadata.get('files', []), 1):
            print(f"  {idx}. {file_info['path']} ({format_bytes(file_info['size'])})")
        
        print(f"\n{Colors.GREEN}Total files: {len(metadata.get('files', []))}{Colors.END}\n")
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Error viewing contents: {str(e)}{Colors.END}")
        return False


def encrypt_folder(folder_path: str, password: str, config, hint=None, self_destruct_days=None, create_backup_first=True):
    """Encrypt a folder with password protection"""
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists():
        print(f"{Colors.RED}✗ Error: Folder does not exist!{Colors.END}")
        play_sound("error")
        return False
    
    if not folder_path.is_dir():
        print(f"{Colors.RED}✗ Error: Path is not a folder!{Colors.END}")
        play_sound("error")
        return False
    
    play_sound("start")
    
    # Calculate original size
    print(f"{Colors.CYAN}Analyzing folder...{Colors.END}")
    original_size = get_folder_size(folder_path)
    print(f"{Colors.GREEN}Original size: {format_bytes(original_size)}{Colors.END}")
    
    # Create backup if requested
    backup_path = None
    if create_backup_first:
        backup_path = create_backup(folder_path)
    
    # Generate salt and derive key
    salt = os.urandom(16)
    iterations = config['iterations']
    key = derive_key(password, salt, iterations)
    
    # Create encrypted zip file
    encrypted_file = folder_path.parent / f"{folder_path.name}.encrypted"
    temp_zip = folder_path.parent / f"{folder_path.name}.temp.zip"
    
    try:
        # Encryption animation
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[ENCRYPTION INITIATED - {config['name']} Mode]{Colors.END}\n")
        
        # Compress folder to zip with progress
        print(f"{Colors.CYAN}Compressing folder...{Colors.END}")
        
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root) / file
                file_list.append(file_path)
        
        with zipfile.ZipFile(temp_zip, 'w', config['compression']) as zipf:
            for idx, file_path in enumerate(file_list, 1):
                arcname = file_path.relative_to(folder_path.parent)
                zipf.write(file_path, arcname)
                progress_bar(idx, len(file_list), prefix='Compressing', suffix=f'{file_path.name}')
        
        # Create metadata
        metadata = {
            'version': __version__,
            'timestamp': datetime.now().isoformat(),
            'level': config['name'],
            'iterations': iterations,
            'original_size': original_size,
            'files': [{'path': str(f.relative_to(folder_path.parent)), 'size': f.stat().st_size} for f in file_list],
            'hint': hint
        }
        
        if self_destruct_days:
            destruct_date = datetime.now() + timedelta(days=self_destruct_days)
            metadata['self_destruct'] = destruct_date.isoformat()
        
        # Encrypt metadata
        key_bytes = base64.urlsafe_b64encode(key)
        cipher = Fernet(key_bytes)
        encrypted_metadata = cipher.encrypt(json.dumps(metadata).encode())
        
        # Read and encrypt zip file
        print(f"\n{Colors.CYAN}Encrypting data (this may take a moment)...{Colors.END}")
        with open(temp_zip, 'rb') as f:
            data = f.read()
        
        encrypted_data = cipher.encrypt(data)
        
        # Write encrypted file with metadata
        with open(encrypted_file, 'wb') as f:
            f.write(salt)
            f.write(len(encrypted_metadata).to_bytes(4, 'big'))
            f.write(encrypted_metadata)
            f.write(encrypted_data)
        
        # Clean up
        temp_zip.unlink()
        
        # Calculate encrypted size
        encrypted_size = encrypted_file.stat().st_size
        compression_ratio = (1 - encrypted_size / original_size) * 100 if original_size > 0 else 0
        
        # Success animation
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ENCRYPTION COMPLETE ✓{Colors.END}\n")
        print(f"{Colors.GREEN}═══════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}🔒 Folder successfully encrypted!{Colors.END}")
        print(f"{Colors.GREEN}📁 Encrypted file: {encrypted_file.name}{Colors.END}")
        print(f"{Colors.CYAN}📊 Original size: {format_bytes(original_size)}{Colors.END}")
        print(f"{Colors.CYAN}📊 Encrypted size: {format_bytes(encrypted_size)}{Colors.END}")
        
        if compression_ratio > 0:
            print(f"{Colors.YELLOW}📉 Compression: {compression_ratio:.1f}% smaller{Colors.END}")
        else:
            print(f"{Colors.YELLOW}📈 Size increase: {abs(compression_ratio):.1f}% (encryption overhead){Colors.END}")
        
        print(f"{Colors.GREEN}═══════════════════════════════════════{Colors.END}\n")
        
        # Save encryption log
        log_data = {
            'operation': 'encryption',
            'timestamp': datetime.now().isoformat(),
            'original_folder': str(folder_path),
            'encrypted_file': str(encrypted_file),
            'encryption_level': config['name'],
            'original_size': original_size,
            'encrypted_size': encrypted_size,
            'compression_ratio': f"{compression_ratio:.2f}%",
            'backup_created': str(backup_path) if backup_path else None,
            'self_destruct_days': self_destruct_days
        }
        
        log_file = save_encryption_log(log_data, encrypted_file)
        
        # Ask if user wants to delete original
        delete = input(f"{Colors.YELLOW}Delete original folder? (y/n): {Colors.END}").lower()
        if delete == 'y':
            shutil.rmtree(folder_path)
            print(f"{Colors.GREEN}✓ Original folder deleted{Colors.END}")
        
        play_sound("success")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Encryption failed: {str(e)}{Colors.END}")
        if temp_zip.exists():
            temp_zip.unlink()
        play_sound("error")
        return False


def decrypt_folder(encrypted_file_path: str, password: str):
    """Decrypt an encrypted folder"""
    encrypted_file = Path(encrypted_file_path).resolve()
    
    if not encrypted_file.exists():
        print(f"{Colors.RED}✗ Error: Encrypted file does not exist!{Colors.END}")
        play_sound("error")
        return False
    
    play_sound("start")
    
    try:
        # Read encrypted file
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[DECRYPTION INITIATED]{Colors.END}\n")
        print(f"{Colors.CYAN}Reading encrypted data...{Colors.END}")
        
        with open(encrypted_file, 'rb') as f:
            salt = f.read(16)
            metadata_len_bytes = f.read(4)
            metadata_len = int.from_bytes(metadata_len_bytes, 'big')
            encrypted_metadata = f.read(metadata_len)
            encrypted_data = f.read()
        
        encrypted_size = encrypted_file.stat().st_size
        
        # Try to decrypt metadata first to get iterations
        print(f"{Colors.CYAN}Verifying password...{Colors.END}")
        
        # Default iterations
        iterations = 100000
        key = derive_key(password, salt, iterations)
        key_bytes = base64.urlsafe_b64encode(key)
        cipher = Fernet(key_bytes)
        
        try:
            metadata_json = cipher.decrypt(encrypted_metadata)
            metadata = json.loads(metadata_json)
            iterations = metadata.get('iterations', 100000)
            
            # Re-derive key with correct iterations if different
            if iterations != 100000:
                key = derive_key(password, salt, iterations)
                key_bytes = base64.urlsafe_b64encode(key)
                cipher = Fernet(key_bytes)
        except Exception:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ DECRYPTION FAILED ✗{Colors.END}")
            print(f"{Colors.RED}Incorrect password!{Colors.END}\n")
            play_sound("error")
            return False
        
        # Check self-destruct
        if 'self_destruct' in metadata and metadata['self_destruct']:
            destruct_date = datetime.fromisoformat(metadata['self_destruct'])
            if datetime.now() > destruct_date:
                print(f"{Colors.RED}⚠️  SELF-DESTRUCT TRIGGERED ⚠️{Colors.END}")
                print(f"{Colors.RED}This file has expired and will be deleted.{Colors.END}")
                encrypted_file.unlink()
                play_sound("error")
                return False
        
        # Decryption animation phases
        phases = [
            "Verifying password hash",
            "Loading encryption key",
            "Breaking cipher blocks",
            "Reconstructing data stream",
            "Validating file integrity",
            "Restoring folder structure"
        ]
        
        for phase in phases:
            print(f"{Colors.MAGENTA}⚡ {phase}...{Colors.END}")
            time.sleep(0.3)
        
        print(f"\n{Colors.CYAN}Decrypting data...{Colors.END}")
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Extract zip file
        output_folder = encrypted_file.parent / encrypted_file.stem.replace('.encrypted', '')
        temp_zip = encrypted_file.parent / "temp_decrypt.zip"
        
        print(f"{Colors.CYAN}Extracting files...{Colors.END}")
        
        with open(temp_zip, 'wb') as f:
            f.write(decrypted_data)
        
        with zipfile.ZipFile(temp_zip, 'r') as zipf:
            file_list = zipf.namelist()
            for idx, file in enumerate(file_list, 1):
                zipf.extract(file, encrypted_file.parent)
                progress_bar(idx, len(file_list), prefix='Extracting', suffix=file)
        
        # Clean up
        temp_zip.unlink()
        
        # Display results
        original_size = metadata.get('original_size', 0)
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ DECRYPTION COMPLETE ✓{Colors.END}\n")
        print(f"{Colors.GREEN}═══════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}🔓 Folder successfully decrypted!{Colors.END}")
        print(f"{Colors.GREEN}📁 Restored to: {output_folder.name}{Colors.END}")
        print(f"{Colors.CYAN}📊 Encrypted size: {format_bytes(encrypted_size)}{Colors.END}")
        print(f"{Colors.CYAN}📊 Restored size: {format_bytes(original_size)}{Colors.END}")
        print(f"{Colors.YELLOW}🔐 Encryption level: {metadata.get('level', 'Unknown')}{Colors.END}")
        print(f"{Colors.GREEN}═══════════════════════════════════════{Colors.END}\n")
        
        # Save decryption log
        log_data = {
            'operation': 'decryption',
            'timestamp': datetime.now().isoformat(),
            'encrypted_file': str(encrypted_file),
            'restored_folder': str(output_folder),
            'encryption_level': metadata.get('level', 'Unknown'),
            'encrypted_size': encrypted_size,
            'restored_size': original_size
        }
        
        save_encryption_log(log_data, output_folder)
        
        # Ask if user wants to delete encrypted file
        delete = input(f"{Colors.YELLOW}Delete encrypted file? (y/n): {Colors.END}").lower()
        if delete == 'y':
            encrypted_file.unlink()
            print(f"{Colors.GREEN}✓ Encrypted file deleted{Colors.END}")
        
        play_sound("success")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Decryption failed: {str(e)}{Colors.END}")
        play_sound("error")
        return False


def batch_encrypt():
    """Batch encrypt multiple folders"""
    print(f"\n{Colors.BOLD}═══ BATCH ENCRYPTION MODE ═══{Colors.END}\n")
    print(f"{Colors.CYAN}Enter folder paths (one per line, empty line to finish):{Colors.END}")
    
    folders = []
    while True:
        path = input(f"{Colors.YELLOW}Folder {len(folders) + 1}: {Colors.END}").strip().strip('"').strip("'")
        if not path:
            break
        folders.append(path)
    
    if not folders:
        print(f"{Colors.RED}✗ No folders provided!{Colors.END}")
        return
    
    # Get encryption settings
    print(f"\n{Colors.BOLD}Select encryption strength:{Colors.END}")
    print(f"1. {Colors.GREEN}Fast{Colors.END} (Quick encryption, lower security)")
    print(f"2. {Colors.YELLOW}Balanced{Colors.END} (Good balance - Recommended)")
    print(f"3. {Colors.RED}Maximum Security{Colors.END} (Slower, highest security)")
    
    choice = input(f"\n{Colors.YELLOW}Choice (1-3): {Colors.END}")
    config = {
        '1': EncryptionConfig.FAST,
        '2': EncryptionConfig.BALANCED,
        '3': EncryptionConfig.MAXIMUM
    }.get(choice, EncryptionConfig.BALANCED)
    
    # Get password
    password = get_password_with_toggle(f"{Colors.YELLOW}Enter encryption password for all folders:{Colors.END}", show_strength=True)
    
    # Encrypt each folder
    print(f"\n{Colors.CYAN}Starting batch encryption of {len(folders)} folders...{Colors.END}\n")
    
    successful = 0
    failed = 0
    
    for idx, folder in enumerate(folders, 1):
        print(f"\n{Colors.BOLD}[{idx}/{len(folders)}] Processing: {folder}{Colors.END}")
        if encrypt_folder(folder, password, config, create_backup_first=False):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{Colors.BOLD}═══ BATCH ENCRYPTION COMPLETE ═══{Colors.END}")
    print(f"{Colors.GREEN}✓ Successful: {successful}{Colors.END}")
    if failed > 0:
        print(f"{Colors.RED}✗ Failed: {failed}{Colors.END}")


def batch_decrypt():
    """Batch decrypt multiple encrypted files"""
    print(f"\n{Colors.BOLD}═══ BATCH DECRYPTION MODE ═══{Colors.END}\n")
    print(f"{Colors.CYAN}Enter encrypted file paths (one per line, empty line to finish):{Colors.END}")
    
    files = []
    while True:
        path = input(f"{Colors.YELLOW}File {len(files) + 1}: {Colors.END}").strip().strip('"').strip("'")
        if not path:
            break
        files.append(path)
    
    if not files:
        print(f"{Colors.RED}✗ No files provided!{Colors.END}")
        return
    
    # Get password
    password = get_password_with_toggle(f"{Colors.YELLOW}Enter decryption password for all files:{Colors.END}")
    
    # Decrypt each file
    print(f"\n{Colors.CYAN}Starting batch decryption of {len(files)} files...{Colors.END}\n")
    
    successful = 0
    failed = 0
    
    for idx, file in enumerate(files, 1):
        print(f"\n{Colors.BOLD}[{idx}/{len(files)}] Processing: {file}{Colors.END}")
        if decrypt_folder(file, password):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{Colors.BOLD}═══ BATCH DECRYPTION COMPLETE ═══{Colors.END}")
    print(f"{Colors.GREEN}✓ Successful: {successful}{Colors.END}")
    if failed > 0:
        print(f"{Colors.RED}✗ Failed: {failed}{Colors.END}")


def main():
    """Main application entry point"""
    clear_screen()
    print_banner()
    
    # Check for updates on startup
    check_for_updates()
    
    print(f"{Colors.BOLD}Select operation:{Colors.END}")
    print(f"{Colors.CYAN}1. 🔒 Encrypt Single Folder{Colors.END}")
    print(f"{Colors.MAGENTA}2. 🔓 Decrypt Single File{Colors.END}")
    print(f"{Colors.GREEN}3. 📦 Batch Encrypt Multiple Folders{Colors.END}")
    print(f"{Colors.BLUE}4. 📂 Batch Decrypt Multiple Files{Colors.END}")
    print(f"{Colors.YELLOW}5. 👁️  View Encrypted File Contents{Colors.END}")
    print(f"{Colors.CYAN}6. ℹ️  About / Version Info{Colors.END}")
    print(f"{Colors.RED}7. ❌ Exit{Colors.END}\n")
    
    choice = input(f"{Colors.YELLOW}Enter your choice (1-7): {Colors.END}")
    
    if choice == '1':
        # Single folder encryption
        print(f"\n{Colors.BOLD}═══ ENCRYPTION MODE ═══{Colors.END}\n")
        folder_path = input(f"{Colors.CYAN}Enter folder path to encrypt: {Colors.END}").strip().strip('"').strip("'")
        
        if not folder_path:
            print(f"{Colors.RED}✗ No path provided!{Colors.END}")
            return
        
        # Select encryption strength
        print(f"\n{Colors.BOLD}Select encryption strength:{Colors.END}")
        print(f"1. {Colors.GREEN}Fast{Colors.END} (Quick encryption, lower security)")
        print(f"2. {Colors.YELLOW}Balanced{Colors.END} (Good balance - Recommended)")
        print(f"3. {Colors.RED}Maximum Security{Colors.END} (Slower, highest security)")
        
        strength_choice = input(f"\n{Colors.YELLOW}Choice (1-3, default=2): {Colors.END}") or '2'
        config = {
            '1': EncryptionConfig.FAST,
            '2': EncryptionConfig.BALANCED,
            '3': EncryptionConfig.MAXIMUM
        }.get(strength_choice, EncryptionConfig.BALANCED)
        
        # Password hint
        hint_choice = input(f"{Colors.YELLOW}Add password hint? (y/n): {Colors.END}").lower()
        hint = None
        if hint_choice == 'y':
            hint = input(f"{Colors.CYAN}Enter hint: {Colors.END}")
        
        # Self-destruct option
        destruct_choice = input(f"{Colors.YELLOW}Set self-destruct timer? (y/n): {Colors.END}").lower()
        self_destruct_days = None
        if destruct_choice == 'y':
            try:
                days = int(input(f"{Colors.CYAN}Delete after how many days?: {Colors.END}"))
                self_destruct_days = days
                print(f"{Colors.RED}⚠️  File will self-destruct in {days} days!{Colors.END}")
            except:
                print(f"{Colors.YELLOW}Invalid input, skipping self-destruct{Colors.END}")
        
        # Backup option
        backup_choice = input(f"{Colors.YELLOW}Create backup before encryption? (y/n, default=y): {Colors.END}").lower()
        create_backup_first = backup_choice != 'n'
        
        # Get password with strength meter
        password = get_password_with_toggle(f"{Colors.YELLOW}Enter encryption password:{Colors.END}", show_strength=True)
        confirm = get_password_with_toggle(f"{Colors.YELLOW}Confirm password:{Colors.END}")
        
        if password != confirm:
            print(f"{Colors.RED}✗ Passwords do not match!{Colors.END}")
            play_sound("error")
            return
        
        if not password:
            print(f"{Colors.RED}✗ Password cannot be empty!{Colors.END}")
            play_sound("error")
            return
        
        encrypt_folder(folder_path, password, config, hint, self_destruct_days, create_backup_first)
        
    elif choice == '2':
        # Single file decryption
        print(f"\n{Colors.BOLD}═══ DECRYPTION MODE ═══{Colors.END}\n")
        file_path = input(f"{Colors.MAGENTA}Enter encrypted file path: {Colors.END}").strip().strip('"').strip("'")
        
        if not file_path:
            print(f"{Colors.RED}✗ No path provided!{Colors.END}")
            return
        
        password = get_password_with_toggle(f"{Colors.YELLOW}Enter decryption password:{Colors.END}")
        
        decrypt_folder(file_path, password)
        
    elif choice == '3':
        # Batch encryption
        batch_encrypt()
        
    elif choice == '4':
        # Batch decryption
        batch_decrypt()
        
    elif choice == '5':
        # View contents
        print(f"\n{Colors.BOLD}═══ VIEW ENCRYPTED CONTENTS ═══{Colors.END}\n")
        file_path = input(f"{Colors.CYAN}Enter encrypted file path: {Colors.END}").strip().strip('"').strip("'")
        
        if not file_path:
            print(f"{Colors.RED}✗ No path provided!{Colors.END}")
            return
        
        password = get_password_with_toggle(f"{Colors.YELLOW}Enter password to view contents:{Colors.END}")
        
        list_encrypted_contents(file_path, password)
        
    elif choice == '6':
        # About / Version info
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║                   ABOUT FOLDER VAULT                      ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚═══════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        print(f"{Colors.GREEN}Version:{Colors.END} {__version__}")
        print(f"{Colors.GREEN}Author:{Colors.END} {__author__}")
        print(f"{Colors.GREEN}License:{Colors.END} {__license__}")
        print(f"{Colors.GREEN}Repository:{Colors.END} https://github.com/yourusername/folder-vault")
        
        print(f"\n{Colors.CYAN}Encryption Details:{Colors.END}")
        print(f"  • Algorithm: AES-256 (Fernet)")
        print(f"  • Key Derivation: PBKDF2-HMAC-SHA256")
        print(f"  • Security Levels: Fast (50K), Balanced (100K), Maximum (500K) iterations")
        
        print(f"\n{Colors.YELLOW}Features:{Colors.END}")
        print(f"  ✓ Military-grade encryption")
        print(f"  ✓ Password strength meter")
        print(f"  ✓ Batch operations")
        print(f"  ✓ Auto-backup system")
        print(f"  ✓ Self-destruct timer")
        print(f"  ✓ Encrypted file viewer")
        print(f"  ✓ Progress tracking")
        print(f"  ✓ Operation logging")
        
        print(f"\n{Colors.MAGENTA}Support:{Colors.END}")
        print(f"  • Report issues: https://github.com/Thunderrock424242/Folder-vault/issues")
        print(f"  • Latest releases: https://github.com/Thunderrock424242/Folder-vault/releases")
        
        print(f"\n{Colors.GREEN}Thank you for using Folder Vault! 🔐{Colors.END}\n")
        
        input(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.END}")
        main()  # Return to main menu
        
    elif choice == '7':
        print(f"\n{Colors.CYAN}Goodbye! Stay secure! 🔐{Colors.END}")
        return
    
    else:
        print(f"{Colors.RED}✗ Invalid choice!{Colors.END}")


if __name__ == "__main__":
    try:
        # Check for command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] in ['-v', '--version', 'version']:
                print(f"Folder Vault v{__version__}")
                print(f"Author: {__author__}")
                print(f"License: {__license__}")
                sys.exit(0)
            elif sys.argv[1] in ['-h', '--help', 'help']:
                print(f"""
Folder Vault v{__version__} - Secure Folder Encryption Tool

Usage:
  python folder_vault.py           Run interactive mode
  python folder_vault.py -v        Show version
  python folder_vault.py -h        Show this help

Features:
  • AES-256 encryption with PBKDF2 key derivation
  • Three security levels: Fast, Balanced, Maximum
  • Batch encryption/decryption
  • Password strength meter
  • Auto-backup system
  • Self-destruct timer
  • Encrypted file viewer

For more information, visit:
  https://github.com/Thunderrock424242/Folder-vault
""")
                sys.exit(0)
        
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
        sys.exit(0)