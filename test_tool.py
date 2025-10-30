#!/usr/bin/env python3
"""
Test suite for Mobile Forensic Tool
Tests basic functionality without requiring actual devices
"""

import json
import sys
from mobile_forensic_tool import MobileForensicTool, Platform


def test_initialization():
    """Test tool initialization"""
    print("Testing initialization...")
    android_tool = MobileForensicTool(Platform.ANDROID)
    assert android_tool.platform == Platform.ANDROID
    assert android_tool.device_id is None
    
    ios_tool = MobileForensicTool(Platform.IOS)
    assert ios_tool.platform == Platform.IOS
    assert ios_tool.device_id is None
    print("✓ Initialization tests passed")


def test_list_devices():
    """Test device listing (will be empty without tools)"""
    print("\nTesting device listing...")
    android_tool = MobileForensicTool(Platform.ANDROID)
    devices = android_tool.list_devices()
    assert isinstance(devices, list)
    print(f"  Found {len(devices)} Android device(s)")
    
    ios_tool = MobileForensicTool(Platform.IOS)
    devices = ios_tool.list_devices()
    assert isinstance(devices, list)
    print(f"  Found {len(devices)} iOS device(s)")
    print("✓ Device listing tests passed")


def test_dependency_check():
    """Test dependency checking"""
    print("\nTesting dependency checks...")
    android_tool = MobileForensicTool(Platform.ANDROID)
    android_deps = android_tool.check_dependencies()
    print(f"  Android dependencies: {'✓ Available' if android_deps else '✗ Missing'}")
    
    ios_tool = MobileForensicTool(Platform.IOS)
    ios_deps = ios_tool.check_dependencies()
    print(f"  iOS dependencies: {'✓ Available' if ios_deps else '✗ Missing'}")
    print("✓ Dependency check tests passed")


def test_bypass_methods_structure():
    """Test bypass methods return proper structure"""
    print("\nTesting bypass methods structure...")
    android_tool = MobileForensicTool(Platform.ANDROID)
    
    # Test with fake device ID
    result = android_tool.attempt_lockscreen_bypass('TEST_DEVICE')
    assert 'device_id' in result
    assert 'platform' in result
    assert 'methods_tried' in result
    assert 'success' in result
    assert result['device_id'] == 'TEST_DEVICE'
    assert result['platform'] == 'android'
    assert isinstance(result['methods_tried'], list)
    print(f"  Android bypass returned {len(result['methods_tried'])} methods")
    
    ios_tool = MobileForensicTool(Platform.IOS)
    result = ios_tool.attempt_lockscreen_bypass('TEST_DEVICE_IOS')
    assert 'device_id' in result
    assert 'platform' in result
    assert result['platform'] == 'ios'
    print(f"  iOS bypass returned {len(result['methods_tried'])} methods")
    print("✓ Bypass methods structure tests passed")


def test_extraction_structure():
    """Test extraction methods return proper structure"""
    print("\nTesting data extraction structure...")
    android_tool = MobileForensicTool(Platform.ANDROID)
    
    # Test with fake device ID and temp directory
    result = android_tool.extract_data('TEST_DEVICE', '/tmp/test_extraction')
    assert 'device_id' in result
    assert 'platform' in result
    assert 'output_dir' in result
    assert 'extracted_items' in result
    assert result['device_id'] == 'TEST_DEVICE'
    assert result['platform'] == 'android'
    print(f"  Extraction structure validated")
    print("✓ Data extraction structure tests passed")


def test_json_serialization():
    """Test that results can be serialized to JSON"""
    print("\nTesting JSON serialization...")
    android_tool = MobileForensicTool(Platform.ANDROID)
    
    # Test bypass result serialization
    result = android_tool.attempt_lockscreen_bypass('TEST_DEVICE')
    json_str = json.dumps(result, indent=2)
    assert len(json_str) > 0
    
    # Test extraction result serialization
    result = android_tool.extract_data('TEST_DEVICE', '/tmp/test_extraction')
    json_str = json.dumps(result, indent=2)
    assert len(json_str) > 0
    print("✓ JSON serialization tests passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Mobile Forensic Tool Tests")
    print("=" * 60)
    
    try:
        test_initialization()
        test_list_devices()
        test_dependency_check()
        test_bypass_methods_structure()
        test_extraction_structure()
        test_json_serialization()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
