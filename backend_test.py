import requests
import sys
import os
from datetime import datetime
from io import BytesIO
from PIL import Image
import base64

class CarAnalysisAPITester:
    def __init__(self, base_url="https://bonnet-inspector.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.analysis_ids = []

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=60)
                else:
                    headers['Content-Type'] = 'application/json'
                    response = requests.post(url, json=data, headers=headers, timeout=60)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if 'id' in response_data:
                        self.analysis_ids.append(response_data['id'])
                        print(f"   Analysis ID: {response_data['id']}")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Response: {response.text[:200]}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def create_test_image(self, width=100, height=100, color=(255, 255, 255)):
        """Create a test image"""
        image = Image.new('RGB', (width, height), color)
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        return img_buffer

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_white_pixel_analysis(self):
        """Test white pixel analysis endpoint"""
        # Create a test image with white pixels
        test_image = self.create_test_image(50, 50, (255, 255, 255))
        files = {'file': ('test_white.png', test_image, 'image/png')}
        
        success, response = self.run_test(
            "White Pixel Analysis",
            "POST",
            "analyze/white-pixels",
            200,
            files=files
        )
        
        if success and response:
            print(f"   White pixels: {response.get('white_pixel_count', 'N/A')}")
            print(f"   Total pixels: {response.get('total_pixels', 'N/A')}")
            print(f"   Percentage: {response.get('percentage', 'N/A')}%")
        
        return success

    def test_bonnet_analysis(self):
        """Test bonnet analysis endpoint"""
        # Create a test image (simulating car bonnet)
        test_image = self.create_test_image(200, 150, (128, 128, 128))
        files = {'file': ('test_bonnet.png', test_image, 'image/png')}
        
        success, response = self.run_test(
            "Bonnet Analysis",
            "POST",
            "analyze/bonnet",
            200,
            files=files
        )
        
        if success and response:
            print(f"   Car color: {response.get('car_color', 'N/A')}")
            print(f"   Condition: {response.get('condition', 'N/A')}")
            print(f"   Recommendation: {response.get('wash_or_repaint', 'N/A')}")
        
        return success

    def test_analysis_history(self):
        """Test analysis history endpoint"""
        success, response = self.run_test(
            "Analysis History",
            "GET",
            "analysis/history",
            200
        )
        
        if success and response:
            print(f"   Found {len(response)} analyses in history")
        
        return success

    def test_analysis_detail(self):
        """Test analysis detail endpoint"""
        if not self.analysis_ids:
            print("⚠️  No analysis IDs available for detail test")
            return False
        
        analysis_id = self.analysis_ids[0]
        success, response = self.run_test(
            "Analysis Detail",
            "GET",
            f"analysis/{analysis_id}",
            200
        )
        
        if success and response:
            print(f"   Analysis type: {response.get('analysis_type', 'N/A')}")
            print(f"   Image name: {response.get('image_name', 'N/A')}")
        
        return success

    def test_invalid_analysis_detail(self):
        """Test analysis detail with invalid ID"""
        return self.run_test(
            "Invalid Analysis Detail",
            "GET",
            "analysis/invalid-id-123",
            404
        )

def main():
    print("🚀 Starting Car Analysis API Tests")
    print("=" * 50)
    
    # Setup
    tester = CarAnalysisAPITester()
    
    # Run tests in order
    tests = [
        ("Root API", tester.test_root_endpoint),
        ("White Pixel Analysis", tester.test_white_pixel_analysis),
        ("Bonnet Analysis", tester.test_bonnet_analysis),
        ("Analysis History", tester.test_analysis_history),
        ("Analysis Detail", tester.test_analysis_detail),
        ("Invalid Analysis Detail", tester.test_invalid_analysis_detail),
    ]
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())