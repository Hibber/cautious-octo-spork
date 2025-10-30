#!/usr/bin/env python3
"""
Mobile Forensic and Security Lockout Bypass Tool
Supports Android and iOS devices for forensic analysis and security testing
"""

import argparse
import subprocess
import sys
import os
import json
from enum import Enum
from typing import Dict, List, Optional


class Platform(Enum):
    """Supported mobile platforms"""
    ANDROID = "android"
    IOS = "ios"


class MobileForensicTool:
    """Main class for mobile forensic operations"""
    
    def __init__(self, platform: Platform):
        self.platform = platform
        self.device_id = None
        
    def check_dependencies(self) -> bool:
        """Check if required tools are available"""
        if self.platform == Platform.ANDROID:
            return self._check_adb()
        elif self.platform == Platform.IOS:
            return self._check_ios_tools()
        return False
    
    def _check_adb(self) -> bool:
        """Check if ADB is available"""
        try:
            result = subprocess.run(['adb', 'version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _check_ios_tools(self) -> bool:
        """Check if iOS tools are available"""
        try:
            # Check for ideviceinfo (part of libimobiledevice)
            result = subprocess.run(['ideviceinfo', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def list_devices(self) -> List[Dict[str, str]]:
        """List connected devices"""
        if self.platform == Platform.ANDROID:
            return self._list_android_devices()
        elif self.platform == Platform.IOS:
            return self._list_ios_devices()
        return []
    
    def _list_android_devices(self) -> List[Dict[str, str]]:
        """List connected Android devices"""
        devices = []
        try:
            result = subprocess.run(['adb', 'devices', '-l'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip() and 'device' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            devices.append({
                                'id': parts[0],
                                'status': parts[1],
                                'platform': 'Android'
                            })
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return devices
    
    def _list_ios_devices(self) -> List[Dict[str, str]]:
        """List connected iOS devices"""
        devices = []
        try:
            result = subprocess.run(['idevice_id', '-l'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                for device_id in result.stdout.strip().split('\n'):
                    if device_id.strip():
                        devices.append({
                            'id': device_id.strip(),
                            'status': 'connected',
                            'platform': 'iOS'
                        })
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return devices
    
    def get_device_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """Get device information"""
        self.device_id = device_id
        if self.platform == Platform.ANDROID:
            return self._get_android_info(device_id)
        elif self.platform == Platform.IOS:
            return self._get_ios_info(device_id)
        return None
    
    def _get_android_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """Get Android device information"""
        info = {'device_id': device_id, 'platform': 'Android'}
        try:
            # Get device properties
            properties = {
                'model': 'ro.product.model',
                'manufacturer': 'ro.product.manufacturer',
                'android_version': 'ro.build.version.release',
                'sdk_version': 'ro.build.version.sdk',
                'serial': 'ro.serialno'
            }
            
            for key, prop in properties.items():
                result = subprocess.run(
                    ['adb', '-s', device_id, 'shell', 'getprop', prop],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    info[key] = result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return info
    
    def _get_ios_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """Get iOS device information"""
        info = {'device_id': device_id, 'platform': 'iOS'}
        try:
            result = subprocess.run(
                ['ideviceinfo', '-u', device_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in ['DeviceName', 'ProductType', 'ProductVersion', 
                                  'BuildVersion', 'UniqueDeviceID']:
                            info[key.lower()] = value
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return info
    
    def attempt_lockscreen_bypass(self, device_id: str) -> Dict[str, any]:
        """Attempt various lockscreen bypass techniques"""
        self.device_id = device_id
        result = {
            'device_id': device_id,
            'platform': self.platform.value,
            'bypass_attempted': True,
            'methods_tried': [],
            'success': False,
            'notes': []
        }
        
        if self.platform == Platform.ANDROID:
            result['methods_tried'].extend(self._android_bypass_methods(device_id))
        elif self.platform == Platform.IOS:
            result['methods_tried'].extend(self._ios_bypass_methods(device_id))
        
        result['success'] = any(m.get('success', False) for m in result['methods_tried'])
        return result
    
    def _android_bypass_methods(self, device_id: str) -> List[Dict[str, any]]:
        """Android lockscreen bypass methods"""
        methods = []
        
        # Method 1: Check if device is already unlocked
        method1 = {'name': 'Check Unlock Status', 'success': False}
        try:
            result = subprocess.run(
                ['adb', '-s', device_id, 'shell', 'dumpsys', 'window'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and 'mDreamingLockscreen=false' in result.stdout:
                method1['success'] = True
                method1['note'] = 'Device appears to be unlocked'
        except (subprocess.SubprocessError, FileNotFoundError):
            method1['note'] = 'Unable to check lock status'
        methods.append(method1)
        
        # Method 2: Remove lock files (requires root)
        method2 = {'name': 'Lock File Removal', 'success': False}
        try:
            # This requires root access
            lock_files = [
                '/data/system/gesture.key',
                '/data/system/password.key',
                '/data/system/locksettings.db'
            ]
            method2['note'] = 'Requires root access - check device root status'
            method2['files_to_remove'] = lock_files
        except Exception as e:
            method2['note'] = f'Error: {str(e)}'
        methods.append(method2)
        
        # Method 3: ADB input commands
        method3 = {'name': 'ADB Input Commands', 'success': False}
        try:
            # Wake device
            subprocess.run(
                ['adb', '-s', device_id, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'],
                capture_output=True,
                timeout=5
            )
            # Swipe up
            subprocess.run(
                ['adb', '-s', device_id, 'shell', 'input', 'swipe', '300', '1000', '300', '300'],
                capture_output=True,
                timeout=5
            )
            method3['note'] = 'Attempted wake and swipe gestures'
        except (subprocess.SubprocessError, FileNotFoundError):
            method3['note'] = 'ADB input commands failed'
        methods.append(method3)
        
        return methods
    
    def _ios_bypass_methods(self, device_id: str) -> List[Dict[str, any]]:
        """iOS lockscreen bypass methods"""
        methods = []
        
        # Method 1: Check device pair status
        method1 = {'name': 'Check Pair Status', 'success': False}
        try:
            result = subprocess.run(
                ['idevicepair', '-u', device_id, 'validate'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                method1['success'] = True
                method1['note'] = 'Device is paired and may allow access'
            else:
                method1['note'] = 'Device requires pairing'
        except (subprocess.SubprocessError, FileNotFoundError):
            method1['note'] = 'Unable to check pair status'
        methods.append(method1)
        
        # Method 2: Backup extraction
        method2 = {'name': 'Backup Extraction', 'success': False}
        try:
            method2['note'] = 'Backup extraction may be possible if device is paired'
            method2['command'] = 'idevicebackup2 backup --udid <device_id> <backup_dir>'
        except Exception as e:
            method2['note'] = f'Error: {str(e)}'
        methods.append(method2)
        
        # Method 3: Emergency call interface
        method3 = {'name': 'Emergency Interface Check', 'success': False}
        method3['note'] = 'Manual check: Emergency call interface may provide limited access'
        methods.append(method3)
        
        return methods
    
    def extract_data(self, device_id: str, output_dir: str) -> Dict[str, any]:
        """Extract data from device"""
        self.device_id = device_id
        result = {
            'device_id': device_id,
            'platform': self.platform.value,
            'output_dir': output_dir,
            'extracted_items': [],
            'errors': []
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
        if self.platform == Platform.ANDROID:
            result['extracted_items'] = self._android_data_extraction(device_id, output_dir)
        elif self.platform == Platform.IOS:
            result['extracted_items'] = self._ios_data_extraction(device_id, output_dir)
        
        return result
    
    def _android_data_extraction(self, device_id: str, output_dir: str) -> List[str]:
        """Extract data from Android device"""
        extracted = []
        
        # Extract system information
        try:
            info_file = os.path.join(output_dir, 'device_info.txt')
            result = subprocess.run(
                ['adb', '-s', device_id, 'shell', 'getprop'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                with open(info_file, 'w') as f:
                    f.write(result.stdout)
                extracted.append('device_info.txt')
        except Exception:
            pass
        
        # List installed packages
        try:
            packages_file = os.path.join(output_dir, 'installed_packages.txt')
            result = subprocess.run(
                ['adb', '-s', device_id, 'shell', 'pm', 'list', 'packages'],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0:
                with open(packages_file, 'w') as f:
                    f.write(result.stdout)
                extracted.append('installed_packages.txt')
        except Exception:
            pass
        
        # Get logcat snapshot
        try:
            logcat_file = os.path.join(output_dir, 'logcat.txt')
            result = subprocess.run(
                ['adb', '-s', device_id, 'logcat', '-d'],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0:
                with open(logcat_file, 'w') as f:
                    f.write(result.stdout)
                extracted.append('logcat.txt')
        except Exception:
            pass
        
        return extracted
    
    def _ios_data_extraction(self, device_id: str, output_dir: str) -> List[str]:
        """Extract data from iOS device"""
        extracted = []
        
        # Extract device information
        try:
            info_file = os.path.join(output_dir, 'device_info.txt')
            result = subprocess.run(
                ['ideviceinfo', '-u', device_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                with open(info_file, 'w') as f:
                    f.write(result.stdout)
                extracted.append('device_info.txt')
        except Exception:
            pass
        
        # List installed apps
        try:
            apps_file = os.path.join(output_dir, 'installed_apps.txt')
            result = subprocess.run(
                ['ideviceinstaller', '-u', device_id, '-l'],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0:
                with open(apps_file, 'w') as f:
                    f.write(result.stdout)
                extracted.append('installed_apps.txt')
        except Exception:
            pass
        
        # Get syslog
        try:
            syslog_file = os.path.join(output_dir, 'syslog.txt')
            result = subprocess.run(
                ['idevicesyslog', '-u', device_id],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                with open(syslog_file, 'w') as f:
                    f.write(result.stdout)
                extracted.append('syslog.txt')
        except Exception:
            pass
        
        return extracted


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='Mobile Forensic and Security Lockout Bypass Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List Android devices
  python mobile_forensic_tool.py --platform android --action list
  
  # Get device info
  python mobile_forensic_tool.py --platform android --action info --device <device_id>
  
  # Attempt lockscreen bypass
  python mobile_forensic_tool.py --platform android --action bypass --device <device_id>
  
  # Extract data
  python mobile_forensic_tool.py --platform android --action extract --device <device_id> --output ./forensic_data
        """
    )
    
    parser.add_argument('--platform', 
                       choices=['android', 'ios'], 
                       required=True,
                       help='Target platform')
    
    parser.add_argument('--action', 
                       choices=['list', 'info', 'bypass', 'extract'],
                       required=False,
                       help='Action to perform')
    
    parser.add_argument('--device', 
                       help='Device ID (required for info, bypass, extract)')
    
    parser.add_argument('--output', 
                       default='./forensic_output',
                       help='Output directory for extracted data')
    
    parser.add_argument('--check-deps', 
                       action='store_true',
                       help='Check if required dependencies are installed')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.check_deps and not args.action:
        parser.error("--action is required unless --check-deps is specified")
    
    # Create tool instance
    platform = Platform.ANDROID if args.platform == 'android' else Platform.IOS
    tool = MobileForensicTool(platform)
    
    # Check dependencies if requested
    if args.check_deps:
        deps_ok = tool.check_dependencies()
        if deps_ok:
            print(f"✓ {args.platform.upper()} dependencies are available")
            sys.exit(0)
        else:
            print(f"✗ {args.platform.upper()} dependencies are missing")
            if args.platform == 'android':
                print("  Install Android Debug Bridge (ADB)")
            else:
                print("  Install libimobiledevice tools")
            sys.exit(1)
    
    # Execute requested action
    if args.action == 'list':
        print(f"Scanning for {args.platform.upper()} devices...")
        devices = tool.list_devices()
        if devices:
            print(f"\nFound {len(devices)} device(s):")
            for device in devices:
                print(f"  ID: {device['id']}")
                print(f"  Status: {device['status']}")
                print(f"  Platform: {device['platform']}")
                print()
        else:
            print("No devices found")
            if not tool.check_dependencies():
                print(f"Note: {args.platform.upper()} tools may not be installed")
    
    elif args.action == 'info':
        if not args.device:
            print("Error: --device is required for info action")
            sys.exit(1)
        
        print(f"Getting device information for {args.device}...")
        info = tool.get_device_info(args.device)
        if info:
            print("\nDevice Information:")
            print(json.dumps(info, indent=2))
        else:
            print("Failed to retrieve device information")
    
    elif args.action == 'bypass':
        if not args.device:
            print("Error: --device is required for bypass action")
            sys.exit(1)
        
        print(f"Attempting lockscreen bypass on {args.device}...")
        print("WARNING: This tool is for authorized forensic use only!")
        print()
        result = tool.attempt_lockscreen_bypass(args.device)
        print("\nBypass Results:")
        print(json.dumps(result, indent=2))
    
    elif args.action == 'extract':
        if not args.device:
            print("Error: --device is required for extract action")
            sys.exit(1)
        
        print(f"Extracting data from {args.device}...")
        print(f"Output directory: {args.output}")
        result = tool.extract_data(args.device, args.output)
        print("\nExtraction Results:")
        print(json.dumps(result, indent=2))
        if result['extracted_items']:
            print(f"\nExtracted {len(result['extracted_items'])} items to {args.output}")


if __name__ == '__main__':
    main()
