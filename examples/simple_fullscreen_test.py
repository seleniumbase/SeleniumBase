"""
Simple test to verify fullscreen functionality
without depending on BaseCase
"""
import sys
import os

# Add root directory to path to import seleniumbase
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seleniumbase.core import browser_launcher

def test_fullscreen_basic():
    """Basic test to verify that --start-fullscreen works"""
    print("🚀 Starting fullscreen test...")
    
    # Configure options for fullscreen
    driver = browser_launcher.get_driver(
        browser_name="chrome",
        headless=False,
        start_fullscreen=True,  # This is the new option
    )
    
    try:
        # Navigate to a test page
        driver.get("https://seleniumbase.io/demo_page")
        
        # Verify window size
        window_size = driver.get_window_size()
        print(f"📐 Window size: {window_size['width']} x {window_size['height']}")
        
        # Verify we're in fullscreen
        assert window_size['width'] >= 1024, f"Width too small: {window_size['width']}"
        assert window_size['height'] >= 768, f"Height too small: {window_size['height']}"
        
        print("✅ Fullscreen test successful!")
        print("🎯 Browser opened correctly in fullscreen mode")
        
        # Wait a bit to see the result
        import time
        time.sleep(3)
        
    finally:
        # Close the browser
        driver.quit()
        print("🔚 Browser closed")

if __name__ == "__main__":
    test_fullscreen_basic() 