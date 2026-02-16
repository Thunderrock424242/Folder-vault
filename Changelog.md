# Changelog

All notable changes to Folder Vault will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Drag-and-drop GUI interface
- Cloud storage integration (Google Drive, Dropbox)
- Hardware key support (YubiKey)
- Multi-language support

---

## [1.0.0] - 2026-02-16

### Initial Release 🎉

#### Added
- **Core Encryption Features**
  - AES-256 encryption with Fernet
  - PBKDF2-HMAC-SHA256 key derivation
  - Three security levels (Fast, Balanced, Maximum)
  - Salt-based encryption for each file

- **User Interface**
  - Beautiful terminal interface with colors and animations
  - Interactive menu system
  - Real-time progress bars
  - Sound effects for operations (Windows)

- **Password Features**
  - Hold CTRL to reveal/hide password while typing
  - Real-time password strength meter
  - Password strength suggestions
  - Optional encrypted password hints

- **Advanced Features**
  - Batch encryption/decryption
  - Automatic backup before encryption
  - Encrypted file content viewer (no decryption needed)
  - Self-destruct timer for temporary files
  - Compression options (Fast/Balanced/Maximum)
  - JSON operation logs

- **File Management**
  - Before/after file size display
  - Compression ratio statistics
  - File count tracking
  - Automatic quote removal from paths

- **Version System**
  - Version display in banner
  - Automatic update checker
  - Command line version flag (`-v`, `--version`)
  - Version stored in encrypted file metadata
  - About/Version info menu option

- **Documentation**
  - Comprehensive README with installation guide
  - Usage examples and screenshots
  - Security explanations
  - FAQ section
  - Troubleshooting guide

#### Security
- Military-grade AES-256 encryption
- Configurable iterations (50K - 500K)
- No password recovery (by design)
- Each file uses unique salt

#### Platform Support
- Windows (full support with sound effects)
- Linux (full support)
- macOS (full support)

---

## Version History

### Versioning Scheme
We use [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible changes
- **MINOR** version: New features (backwards compatible)
- **PATCH** version: Bug fixes

### How to Update
1. Download the latest release from [GitHub Releases](https://github.com/Thunderrock424242/Folder-vault/releases)
2. Extract and replace the old files
3. Run `pip install -r requirements.txt` to update dependencies
4. Your encrypted files remain compatible across versions

---

## Future Roadmap

### v1.1.0 (Planned)
- [ ] GUI interface option
- [ ] Portable executable builds (no Python required)
- [ ] File integrity verification
- [ ] Cloud backup integration
- [ ] face id reconigtion (windows only)

### v1.2.0 (Planned)
- [ ] Multi-user shared encryption
- [ ] Hardware key support

### v2.0.0 (Planned)
- [ ] Complete GUI rewrite
- [ ] Plugin system
- [ ] Network encryption support

---

## Support

Found a bug? Have a feature request? 
- Open an issue: https://github.com/Thunderrock424242/Folder-vault/issues
- View releases: https://github.com/Thunderrock424242/Folder-vault/releases

---

**Note:** Files encrypted with Folder Vault v1.0.0+ will remain compatible with future versions. We maintain backwards compatibility for decryption.