#!/usr/bin/env python3
"""
Test script for the Therapy Response Synthesis API

This script demonstrates how to make requests to the therapy synthesis API endpoint.
"""

import requests
import json
import time

# API base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure the server is running!")
        return False

def test_synthesis_example():
    """Test the synthesis example endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/synthesis-example")
        print(f"\n📋 Example Request Format:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"❌ Error getting example: {e}")
        return None

def test_quick_synthesis():
    """Test the quick synthesis endpoint."""
    try:
        print(f"\n🔬 Testing Quick Synthesis...")
        response = requests.get(f"{BASE_URL}/test-synthesis")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Test synthesis successful!")
            print(f"Synthesized Response Preview: {result['result']['synthesized_response'][:200]}...")
            return True
        else:
            print(f"❌ Test synthesis failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error in quick synthesis: {e}")
        return False

def test_custom_synthesis():
    """Test the main synthesis endpoint with a custom request."""
    try:
        print(f"\n🎯 Testing Custom Synthesis...")
        
        # Custom request data
        request_data = {
            "user_query": """
            Patient: "I'm having trouble sleeping lately. I keep thinking about all the things 
            I need to do tomorrow and my mind just won't quiet down. I've been lying awake 
            for hours every night. This has been going on for about two weeks now."
            
            Question: What therapeutic approaches would be most helpful for this patient's 
            sleep difficulties and racing thoughts?
            """,
            "keywords": ["Sleep", "Anxiety"],
            "top_k": 4
        }
        
        response = requests.post(
            f"{BASE_URL}/synthesize-therapy-response",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Custom synthesis successful!")
            print(f"Keywords Used: {result['keywords']}")
            print(f"Similar Examples Found: {len(result['similar_examples'])}")
            print(f"Synthesized Response: {result['synthesized_response'][:300]}...")
            return True
        else:
            print(f"❌ Custom synthesis failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in custom synthesis: {e}")
        return False

def main():
    """Run all API tests."""
    print("🚀 Starting Therapy Synthesis API Tests")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server with:")
        print("python run_server.py")
        return
    
    # Test 2: Get example format
    example = test_synthesis_example()
    
    # Test 3: Quick synthesis test
    test_quick_synthesis()
    
    # Test 4: Custom synthesis
    test_custom_synthesis()
    
    print(f"\n🎉 API Testing Complete!")
    print(f"\nTo use the API:")
    print(f"1. Start server: python run_server.py")
    print(f"2. API docs: {BASE_URL}/docs")
    print(f"3. Main endpoint: POST {BASE_URL}/synthesize-therapy-response")

if __name__ == "__main__":
    main() 