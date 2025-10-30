#!/bin/bash
# Mobile Forensic Tool - Usage Examples
# This script demonstrates common use cases

echo "=== Mobile Forensic Tool Examples ==="
echo ""

# Check if tools are available
echo "1. Checking Android dependencies..."
python3 mobile_forensic_tool.py --platform android --check-deps
echo ""

echo "2. Checking iOS dependencies..."
python3 mobile_forensic_tool.py --platform ios --check-deps
echo ""

# List devices
echo "3. Listing Android devices..."
python3 mobile_forensic_tool.py --platform android --action list
echo ""

echo "4. Listing iOS devices..."
python3 mobile_forensic_tool.py --platform ios --action list
echo ""

# Example with device (requires actual device connected)
# Uncomment and replace <DEVICE_ID> with your device ID

# echo "5. Getting Android device information..."
# python3 mobile_forensic_tool.py --platform android --action info --device <DEVICE_ID>
# echo ""

# echo "6. Attempting Android lockscreen bypass..."
# python3 mobile_forensic_tool.py --platform android --action bypass --device <DEVICE_ID>
# echo ""

# echo "7. Extracting Android forensic data..."
# python3 mobile_forensic_tool.py --platform android --action extract --device <DEVICE_ID> --output ./android_evidence
# echo ""

# echo "8. Getting iOS device information..."
# python3 mobile_forensic_tool.py --platform ios --action info --device <DEVICE_ID>
# echo ""

# echo "9. Attempting iOS lockscreen bypass..."
# python3 mobile_forensic_tool.py --platform ios --action bypass --device <DEVICE_ID>
# echo ""

# echo "10. Extracting iOS forensic data..."
# python3 mobile_forensic_tool.py --platform ios --action extract --device <DEVICE_ID> --output ./ios_evidence
# echo ""

echo "=== Examples Complete ==="
echo ""
echo "Note: Device-specific examples are commented out."
echo "To use them, connect a device and replace <DEVICE_ID> with the actual device identifier."
