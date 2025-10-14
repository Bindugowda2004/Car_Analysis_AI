import requests
import sys
import os
from datetime import datetime
from io import BytesIO
from PIL import Image
import base64

def test_gpt4_response():
    """Test GPT-4 bonnet analysis and check actual response"""
    base_url = "https://bonnet-inspector.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🔍 Testing GPT-4 Vision response parsing...")
    
    # Create a test image (simulating car bonnet)
    test_image = Image.new('RGB', (200, 150), (128, 128, 128))  # Gray color
    img_buffer = BytesIO()
    test_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    files = {'file': ('debug_bonnet.png', img_buffer, 'image/png')}
    
    try:
        url = f"{api_url}/analyze/bonnet"
        print(f"URL: {url}")
        
        response = requests.post(url, files=files, timeout=60)
        
        if response.status_code == 200:
            print("✅ API call successful")
            data = response.json()
            
            print("\n📊 Analysis Results:")
            print(f"   ID: {data.get('id', 'N/A')}")
            print(f"   Car Color: '{data.get('car_color', 'N/A')}'")
            print(f"   Condition: '{data.get('condition', 'N/A')}'")
            print(f"   Wash/Repaint: '{data.get('wash_or_repaint', 'N/A')}'")
            print(f"   Issues: {data.get('issues', [])}")
            print(f"   Recommendations: {data.get('recommendations', [])}")
            print(f"   Detailed Report: '{data.get('detailed_report', 'N/A')[:200]}...'")
            
            # Check if we're getting placeholder values
            if data.get('car_color') == '[color]':
                print("\n❌ ISSUE FOUND: GPT-4 response is not being parsed correctly!")
                print("   The response contains placeholder values instead of actual analysis.")
                return False
            else:
                print("\n✅ GPT-4 response parsing appears to be working correctly")
                return True
                
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gpt4_response()
    sys.exit(0 if success else 1)