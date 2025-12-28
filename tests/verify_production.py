#!/usr/bin/env python3
"""
Production Verification Script
Tests all critical security features are working correctly
"""

import requests
import time
import sys

# Production URLs
BACKEND_URL = "https://smartboq-ai-w4sz.onrender.com"
FRONTEND_URL = "https://smartboq-ai.vercel.app"

def test_rate_limiting():
    """Test that rate limiting is working"""
    print("\n🔒 Testing Rate Limiting...")
    
    # Try to register 10 times rapidly
    rate_limited = False
    for i in range(10):
        response = requests.post(
            f"{BACKEND_URL}/api/auth/register",
            json={
                "email": f"test{i}_{int(time.time())}@example.com",
                "password": "Test1234",
                "full_name": "Test User"
            }
        )
        
        if response.status_code == 429:
            rate_limited = True
            print(f"   ✅ Rate limit triggered after {i+1} requests (expected: ~5)")
            break
        elif response.status_code == 400 and "already registered" in response.text:
            continue
        elif response.status_code == 200:
            continue
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    
    if not rate_limited:
        print("   ❌ Rate limiting NOT working - made 10 requests without limit")
        return False
    
    return True


def test_password_validation():
    """Test password strength requirements"""
    print("\n🔐 Testing Password Validation...")
    
    test_cases = [
        ("test", False, "Too short"),
        ("testtest", False, "No uppercase"),
        ("TESTTEST", False, "No digit"),
        ("Test1234", True, "Valid password"),
    ]
    
    for password, should_succeed, description in test_cases:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/register",
            json={
                "email": f"test_{int(time.time())}_{password}@example.com",
                "password": password,
                "full_name": "Test User"
            }
        )
        
        if should_succeed and response.status_code == 200:
            print(f"   ✅ {description}: Accepted as expected")
        elif not should_succeed and response.status_code == 422:
            print(f"   ✅ {description}: Rejected as expected")
        else:
            print(f"   ❌ {description}: Unexpected result (status: {response.status_code})")
            return False
    
    return True


def test_backend_health():
    """Test backend is responding"""
    print("\n🏥 Testing Backend Health...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ Backend is responding (FastAPI docs accessible)")
            return True
        else:
            print(f"   ❌ Backend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Backend not accessible: {str(e)}")
        return False


def test_frontend_health():
    """Test frontend is responding"""
    print("\n🌐 Testing Frontend Health...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("   ✅ Frontend is responding")
            return True
        else:
            print(f"   ❌ Frontend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend not accessible: {str(e)}")
        return False


def test_cors():
    """Test CORS is configured correctly"""
    print("\n🌍 Testing CORS Configuration...")
    
    response = requests.options(
        f"{BACKEND_URL}/api/auth/login",
        headers={
            "Origin": FRONTEND_URL,
            "Access-Control-Request-Method": "POST"
        }
    )
    
    if "access-control-allow-origin" in response.headers:
        print(f"   ✅ CORS enabled for: {response.headers.get('access-control-allow-origin')}")
        return True
    else:
        print("   ❌ CORS headers not found")
        return False


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("🚀 SmartBOQ AI - Production Verification")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Health", test_frontend_health),
        ("CORS Configuration", test_cors),
        ("Password Validation", test_password_validation),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n   ❌ {test_name} failed with error: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} | {test_name}")
    
    print("=" * 60)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All critical security features are working correctly!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the deployment.")
        sys.exit(1)


if __name__ == "__main__":
    main()
