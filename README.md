# 🔐 Folder Vault

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**Professional-grade folder encryption tool with military-level security and a beautiful terminal interface**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security)

</div>

---

## 📋 Overview

Folder Vault is a powerful, user-friendly encryption tool that secures your folders with **AES-256 encryption**. It features a beautiful terminal interface with real-time progress tracking, password strength analysis, batch operations, and much more!

### Why Folder Vault?

- 🔒 **Military-grade encryption** (AES-256)
- 🎨 **Beautiful terminal UI** with colors and animations
- 📊 **Real-time progress bars** and file statistics
- 💪 **Password strength meter** with suggestions
- 📦 **Batch operations** for multiple folders
- 🛡️ **Auto-backup** before encryption
- 👁️ **Preview encrypted contents** without decrypting
- ⏱️ **Self-destruct timer** for time-sensitive files
- 🔊 **Audio feedback** for operations
- 📄 **Detailed logging** of all operations

---

## ✨ Features

### 🔐 Encryption Features

- **Three Security Levels:**
  - **Fast Mode** - Quick encryption for less sensitive data
  - **Balanced Mode** - Recommended for most use cases (default)
  - **Maximum Security** - Slowest but strongest protection

- **Advanced Security:**
  - AES-256 encryption with Fernet
  - PBKDF2 key derivation with SHA-256
  - Configurable iteration counts (50K - 500K)
  - Salt-based key generation for each file

### 📊 User Experience

- **Password Management:**
  - Hold `CTRL` to reveal password while typing
  - Real-time password strength meter
  - Helpful suggestions for stronger passwords
  - Optional password hints (encrypted with file)

- **Progress Tracking:**
  - Real-time progress bars for compression/extraction
  - File-by-file operation display
  - Before/after file size comparison
  - Compression ratio statistics

### 🎯 Advanced Features

- **Batch Operations:**
  - Encrypt multiple folders at once
  - Decrypt multiple files at once
  - Progress tracking for each item

- **Safety Features:**
  - Automatic backup creation before encryption
  - Encrypted file content viewer (no decryption needed)
  - Self-destruct timer for temporary files
  - Detailed operation logs in JSON format

- **Compression Options:**
  - Fast: No compression (ZIP_STORED)
  - Balanced: Standard compression (ZIP_DEFLATED)
  - Maximum: Best compression (ZIP_BZIP2)

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Download

1. Go to the [Releases](https://github.com/Thunderrock424242/Folder-vault/releases) page
2. Download the latest release (e.g., `folder-vault-v1.0.zip`)
3. Extract the ZIP file to any location on your computer

### Step 2: Install Dependencies

Open a terminal/command prompt in the extracted folder and run:

**Windows (Command Prompt or PowerShell):**
```bash
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
pip3 install -r requirements.txt
```

### Step 3: Run the Program

**Windows:**
```bash
python folder_vault.py
```

**Linux/macOS:**
```bash
python3 folder_vault.py
```

That's it! You're ready to start encrypting! 🎉

---

### Optional: Add to PATH (Advanced)

To run Folder Vault from anywhere on your system:

**Windows:**
1. Copy the folder to `C:\Program Files\FolderVault\`
2. Add to PATH environment variable
3. Run from anywhere with `python folder_vault.py`

**Linux/macOS:**
```bash
# Make executable
chmod +x folder_vault.py

# Move to bin (optional)
sudo cp folder_vault.py /usr/local/bin/folder-vault

# Run from anywhere
folder-vault
```

---

## 📖 Usage

### Quick Start

Run the script:
```bash
python folder_vault.py
```

You'll see a menu with these options:

```
1. 🔒 Encrypt Single Folder
2. 🔓 Decrypt Single File
3. 📦 Batch Encrypt Multiple Folders
4. 📂 Batch Decrypt Multiple Files
5. 👁️  View Encrypted File Contents
6. ℹ️  About / Version Info
7. ❌ Exit
```

### Encrypting a Folder

1. Select option `1`
2. Enter the folder path (quotes optional)
3. Choose encryption strength (1-3)
4. Optionally add a password hint
5. Optionally set self-destruct timer
6. Choose whether to create a backup
7. Enter and confirm your password
8. Watch the encryption magic happen! ✨

**Example:**
```
Enter folder path to encrypt: C:\Users\YourName\Documents\SecretFiles
Select encryption strength: 2 (Balanced)
Add password hint? (y/n): y
Enter hint: My pet's name + birth year
Set self-destruct timer? (y/n): n
Create backup before encryption? (y/n): y
Enter encryption password: ●●●●●●●●
```

### Decrypting a Folder

1. Select option `2`
2. Enter the encrypted file path (`.encrypted` file)
3. Enter your password
4. Files are restored to original location

### Viewing Encrypted Contents

Want to see what's inside without decrypting?

1. Select option `5`
2. Enter the encrypted file path
3. Enter your password
4. View file list, sizes, and metadata

### Batch Operations

Encrypt or decrypt multiple folders/files in one go:

1. Select option `3` (batch encrypt) or `4` (batch decrypt)
2. Enter paths one by one (empty line when done)
3. Enter password (same for all files)
4. Watch the batch operation complete!

---

## 🔒 Security

### How Secure Is It?

Folder Vault uses **industry-standard encryption**:

- **AES-256** - Used by governments and militaries worldwide
- **PBKDF2** - Password-Based Key Derivation Function 2
- **SHA-256** - Cryptographic hash function
- **Fernet** - Symmetric encryption from the Cryptography library

### Security Levels Explained

| Level | Iterations | Use Case | Speed |
|-------|-----------|----------|-------|
| Fast | 50,000 | Quick backups, low-sensitivity data | ⚡ Fastest |
| Balanced | 100,000 | Recommended for most users | ⚖️ Medium |
| Maximum | 500,000 | Highly sensitive data | 🐢 Slowest |

### Important Security Notes

⚠️ **WARNING:** If you forget your password, **your files are PERMANENTLY LOST**. There is no recovery method, backdoor, or "forgot password" option. This is by design for maximum security.

**Best Practices:**
- Use strong, unique passwords (12+ characters)
- Store passwords in a secure password manager
- Use password hints wisely (don't make them too obvious)
- Keep backups of important files before encryption
- Test decryption immediately after encrypting

---

## 📸 What You'll See

### Main Menu
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            🔐  F O L D E R   V A U L T                   ║
║                                                           ║
║        Advanced Encryption & Decryption System            ║
║                  [FULL FEATURED]                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Encryption Progress
```
Compressing |████████████████████████░░░░░░| 78.3% image.png
Encrypting data (this may take a moment)...

✓ ENCRYPTION COMPLETE ✓
═══════════════════════════════════════
🔒 Folder successfully encrypted!
📁 Encrypted file: SecretFiles.encrypted
📊 Original size: 145.67 MB
📊 Encrypted size: 132.45 MB
📉 Compression: 9.1% smaller
═══════════════════════════════════════
```

### Password Strength Meter
```
Enter encryption password:
💡 Hold CTRL to reveal password, release to hide
➤ ●●●●●●●●●●●●

Strength: VERY STRONG ████████████████████
```

---

## 📁 File Structure

After downloading and extracting the release:

```
folder-vault/
├── folder_vault.py              # Main application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
└── LICENSE                      # MIT License
```

### Generated Files

When you use the tool, it creates:

```
your-folder/
├── backups/                     # Auto-created backups
│   └── FolderName_backup_20240216_143022/
├── FolderName.encrypted         # Encrypted file
└── FolderName_log.json          # Operation log
```

---

## 🔧 Advanced Usage

### Command Line Tips

**Windows - Drag and Drop:**
You can drag folders directly into the terminal when prompted for a path!

**Copy Path Quickly:**
- Windows: Shift + Right-click → "Copy as path"
- macOS: Option + Right-click → "Copy as Pathname"
- Linux: Right-click → "Copy Path"

### Understanding the Logs

Each operation creates a JSON log:

```json
{
    "operation": "encryption",
    "timestamp": "2024-02-16T14:30:22",
    "original_folder": "C:\\Users\\...\\SecretFiles",
    "encrypted_file": "C:\\Users\\...\\SecretFiles.encrypted",
    "encryption_level": "Balanced",
    "original_size": 152698234,
    "encrypted_size": 138847593,
    "compression_ratio": "9.07%",
    "backup_created": "C:\\Users\\...\\backups\\SecretFiles_backup_...",
    "self_destruct_days": null
}
```

### Self-Destruct Feature

Set files to auto-delete after a certain period:

```
Set self-destruct timer? (y/n): y
Delete after how many days?: 30
⚠️  File will self-destruct in 30 days!
```

When viewing or decrypting, you'll see:
```
⚠️  Self-Destruct: 15 days remaining
```

After expiration, the file cannot be decrypted and will be deleted.

---

## ❓ FAQ

### Q: Can I encrypt files instead of folders?
**A:** Currently, Folder Vault is designed for folders. To encrypt a single file, place it in a folder first.

### Q: What happens if I lose my password?
**A:** Your files are **permanently inaccessible**. There is no recovery method. Always keep passwords safe!

### Q: Can I use the same password for multiple folders?
**A:** Yes, but it's recommended to use unique passwords for better security.

### Q: Is this safe for sensitive business data?
**A:** Yes! The encryption (AES-256) is the same standard used by governments and Fortune 500 companies. Use "Maximum Security" mode for extra protection.

### Q: Why is Maximum Security so slow?
**A:** It uses 500,000 iterations of key derivation, making brute-force attacks extremely difficult. The extra time is a security feature.

### Q: Can I decrypt on a different computer?
**A:** Yes! Just copy the `.encrypted` file and this script to another computer, and decrypt with the same password.

### Q: Does this work on cloud storage?
**A:** Yes! Encrypt your folders before uploading to Dropbox, Google Drive, etc. for extra security.

### Q: What if the program crashes during encryption?
**A:** If you enabled auto-backup, your original files are safe in the `backups/` folder. The temporary files are cleaned up automatically.

---

## 🔄 Version System

Folder Vault uses [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- Current version is always shown in the banner

### Check Your Version

**In the app:**
- Select option `6` from the main menu for full version info

**From command line:**
```bash
python folder_vault.py --version
```

### Update Checker

Folder Vault automatically checks for updates when you start the program. If a new version is available, you'll see a notification with a download link.

### Backwards Compatibility

Files encrypted with any version of Folder Vault v1.x will remain compatible with all future v1.x versions. We maintain backwards compatibility for decryption.

### Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes in each version.

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'cryptography'"
**Solution:** Install dependencies with `pip install -r requirements.txt`

### Issue: "Error: Folder does not exist!"
**Solution:** 
- Remove quotes from the path, or
- Make sure the path is correct
- Try using forward slashes: `C:/Users/Name/Folder`

### Issue: Password not showing when typing
**Solution:** This is intentional! Hold CTRL to reveal the password temporarily.

### Issue: "Incorrect password!"
**Solution:** 
- Check if CAPS LOCK is on
- Try viewing the password hint (option 5)
- Make sure you're using the exact same password

### Issue: Sound effects not working
**Solution:** This is normal on some systems. The script works fine without sound.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs:** Open an issue with details
2. **Suggest Features:** Share your ideas in issues
3. **Submit Pull Requests:** 
   - Fork the repo
   - Create a feature branch
   - Make your changes
   - Submit a PR

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Test on Windows, Linux, and macOS if possible
- Update README for new features

---

## 📜 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Disclaimer

This software is provided "as is" without warranty. While it uses industry-standard encryption, the authors are not responsible for:
- Lost passwords or inaccessible files
- Data loss from improper use
- Any damages resulting from use of this software

**Always keep backups of important data!**

---

## 🌟 Credits

- **Encryption:** [Cryptography](https://cryptography.io/) library
- **Algorithm:** AES-256, PBKDF2, SHA-256
- **Inspiration:** Making security accessible to everyone

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Thunderrock424242/Folder-vault/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Thunderrock424242/Folder-vault/issues)
- **Releases:** [Download Latest Version](https://github.com/Thunderrock424242/Folder-vault/releases)

---

<div align="center">

**Made with ❤️ for security-conscious users**

⭐ Star this repo if you find it useful!

[Download Latest Release](https://github.com/yourusername/folder-vault/releases) • [Report Bug](https://github.com/Thunderrock424242/Folder-vault/issues) • [Request Feature](https://github.com/Thunderrock424242/Folder-vault/issues)

</div>