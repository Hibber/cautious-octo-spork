# Mobile Forensic and Security Lockout Bypass Tool

A comprehensive mobile forensic tool for Android and iOS devices designed for authorized security testing and forensic analysis.

## ⚠️ Legal Notice

**THIS TOOL IS FOR AUTHORIZED USE ONLY.** Unauthorized access to mobile devices is illegal and may result in criminal prosecution. Only use this tool on devices you own or have explicit written permission to test.

## Features

### Android Support
- **Device Detection**: Automatically detect and list connected Android devices via ADB
- **Device Information**: Extract comprehensive device information including model, manufacturer, Android version, and serial number
- **Lockscreen Bypass**: Multiple bypass methods including:
  - Unlock status verification
  - Lock file removal (requires root)
  - ADB input commands for gesture simulation
- **Data Extraction**: Extract device properties, installed packages, and system logs

### iOS Support
- **Device Detection**: Automatically detect and list connected iOS devices
- **Device Information**: Extract device name, model, iOS version, and unique identifiers
- **Lockscreen Bypass**: Multiple bypass methods including:
  - Device pairing status verification
  - Backup extraction capabilities
  - Emergency interface analysis
- **Data Extraction**: Extract device information, installed applications, and system logs

## Prerequisites

### For Android Devices
- **Android Debug Bridge (ADB)**: Install from Android SDK Platform Tools
  - Download: https://developer.android.com/studio/releases/platform-tools
  - Installation: Add to PATH environment variable

### For iOS Devices
- **libimobiledevice**: Open-source library for iOS device communication
  - macOS: `brew install libimobiledevice`
  - Linux: `sudo apt-get install libimobiledevice-tools` (Ubuntu/Debian)
  - Windows: Download pre-built binaries or use WSL

### Python Requirements
- Python 3.7 or higher
- No additional Python packages required (uses only standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hibber/cautious-octo-spork.git
cd cautious-octo-spork
```

2. Make the tool executable:
```bash
chmod +x mobile_forensic_tool.py
```

3. Verify dependencies:
```bash
# Check Android dependencies
python mobile_forensic_tool.py --platform android --check-deps

# Check iOS dependencies
python mobile_forensic_tool.py --platform ios --check-deps
```

## Usage

### Basic Commands

#### List Connected Devices
```bash
# List Android devices
python mobile_forensic_tool.py --platform android --action list

# List iOS devices
python mobile_forensic_tool.py --platform ios --action list
```

#### Get Device Information
```bash
# Android device info
python mobile_forensic_tool.py --platform android --action info --device <DEVICE_ID>

# iOS device info
python mobile_forensic_tool.py --platform ios --action info --device <DEVICE_ID>
```

#### Attempt Lockscreen Bypass
```bash
# Android bypass
python mobile_forensic_tool.py --platform android --action bypass --device <DEVICE_ID>

# iOS bypass
python mobile_forensic_tool.py --platform ios --action bypass --device <DEVICE_ID>
```

#### Extract Forensic Data
```bash
# Extract Android data
python mobile_forensic_tool.py --platform android --action extract --device <DEVICE_ID> --output ./android_data

# Extract iOS data
python mobile_forensic_tool.py --platform ios --action extract --device <DEVICE_ID> --output ./ios_data
```

### Advanced Usage

#### Complete Forensic Workflow
```bash
# 1. List devices
python mobile_forensic_tool.py --platform android --action list

# 2. Get device information
python mobile_forensic_tool.py --platform android --action info --device ABC123

# 3. Attempt bypass (if needed)
python mobile_forensic_tool.py --platform android --action bypass --device ABC123

# 4. Extract data
python mobile_forensic_tool.py --platform android --action extract --device ABC123 --output ./evidence
```

## Command Reference

### Arguments

| Argument | Required | Values | Description |
|----------|----------|--------|-------------|
| `--platform` | Yes | `android`, `ios` | Target mobile platform |
| `--action` | Yes | `list`, `info`, `bypass`, `extract` | Action to perform |
| `--device` | Conditional | Device ID string | Device identifier (required for info, bypass, extract) |
| `--output` | No | Directory path | Output directory for extracted data (default: ./forensic_output) |
| `--check-deps` | No | Flag | Check if required dependencies are installed |

### Actions

- **list**: Scan and list all connected devices
- **info**: Get detailed device information
- **bypass**: Attempt various lockscreen bypass techniques
- **extract**: Extract forensic data from device

## Output Structure

Extracted data is organized as follows:
```
forensic_output/
├── device_info.txt          # Device properties and information
├── installed_packages.txt   # List of installed applications (Android)
├── installed_apps.txt       # List of installed applications (iOS)
├── logcat.txt              # System logs (Android)
└── syslog.txt              # System logs (iOS)
```

## Bypass Methods

### Android Bypass Techniques
1. **Unlock Status Check**: Verifies if device is already unlocked
2. **Lock File Removal**: Removes lock screen database files (requires root access)
3. **ADB Input Commands**: Sends wake and swipe gestures to device

### iOS Bypass Techniques
1. **Pair Status Validation**: Checks if device is paired with computer
2. **Backup Extraction**: Attempts to extract device backup
3. **Emergency Interface**: Analyzes emergency call interface for vulnerabilities

## Security Considerations

- Always obtain proper authorization before using this tool
- Keep audit logs of all forensic activities
- Follow your organization's security and privacy policies
- Store extracted data securely and encrypted
- Dispose of forensic data according to data retention policies

## Limitations

- **Android**: Root access required for some bypass methods
- **iOS**: Device must be paired for most operations
- **Both**: Newer security features may prevent some bypass techniques
- Success rate varies based on device model, OS version, and security configuration

## Troubleshooting

### Android Issues
- **No devices found**: Enable USB debugging on device
- **Unauthorized**: Accept USB debugging authorization on device
- **Permission denied**: Check USB cable and drivers

### iOS Issues
- **Device not detected**: Trust the computer on iOS device
- **Pairing failed**: Use iTunes/Finder to pair device first
- **Access denied**: Device must be unlocked for some operations

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request with clear description

## License

This tool is provided for educational and authorized security testing purposes only. Users are responsible for compliance with all applicable laws and regulations.

## Disclaimer

The authors and contributors are not responsible for any misuse of this tool. This software is provided "as is" without warranty of any kind. Use at your own risk and only on devices you are authorized to test.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Review existing documentation
- Check troubleshooting section

## Version History

- **1.0.0** (2025-10-30): Initial release
  - Android device support
  - iOS device support
  - Multiple bypass methods
  - Forensic data extraction
  - CLI interface