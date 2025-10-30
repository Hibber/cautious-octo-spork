# Quick Start Guide

## Prerequisites Check

```bash
# Check if dependencies are installed
python3 mobile_forensic_tool.py --platform android --check-deps
python3 mobile_forensic_tool.py --platform ios --check-deps
```

## Installing Dependencies

### Android (ADB)
- **macOS**: `brew install android-platform-tools`
- **Ubuntu/Debian**: `sudo apt-get install android-tools-adb`
- **Windows**: Download from https://developer.android.com/studio/releases/platform-tools

### iOS (libimobiledevice)
- **macOS**: `brew install libimobiledevice`
- **Ubuntu/Debian**: `sudo apt-get install libimobiledevice-tools`
- **Windows**: Use WSL or download pre-built binaries

## Basic Workflow

### 1. List Devices
```bash
python3 mobile_forensic_tool.py --platform android --action list
```

### 2. Get Device Info
```bash
python3 mobile_forensic_tool.py --platform android --action info --device <DEVICE_ID>
```

### 3. Bypass Lockscreen (If Needed)
```bash
python3 mobile_forensic_tool.py --platform android --action bypass --device <DEVICE_ID>
```

### 4. Extract Forensic Data
```bash
python3 mobile_forensic_tool.py --platform android --action extract --device <DEVICE_ID> --output ./evidence
```

## Common Issues

### Device Not Detected (Android)
1. Enable USB debugging: Settings → Developer Options → USB Debugging
2. Accept USB debugging authorization on device
3. Verify with: `adb devices`

### Device Not Detected (iOS)
1. Trust the computer on iOS device
2. Pair device with iTunes/Finder first
3. Verify with: `idevice_id -l`

### Permission Denied
- Android: Check USB cable and drivers
- iOS: Re-establish trust relationship
- Both: Try different USB port

## Output Files

After extraction, find data in the output directory:
- `device_info.txt` - Device properties
- `installed_packages.txt` or `installed_apps.txt` - App list
- `logcat.txt` or `syslog.txt` - System logs

## Legal Reminder

**⚠️ IMPORTANT**: Only use this tool on devices you own or have written authorization to test. Unauthorized device access is illegal.

## Support

For detailed documentation, see [README.md](README.md)
