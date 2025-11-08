"""
Test API endpoints
"""

import asyncio
import httpx


BASE_URL = "http://localhost:8000"


async def test_health():
    """Test health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        print(response.json())
        print()


async def test_root():
    """Test root endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"Root: {response.status_code}")
        print(response.json())
        print()


async def test_get_token():
    """Test token acquisition"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/auth/token")
        print(f"Get Token: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Access Token: {data['access_token'][:50]}...")
            print(f"Expires In: {data['expires_in']}s")
        else:
            print(response.text)
        print()


async def test_token_status():
    """Test token status"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/auth/token/status")
        print(f"Token Status: {response.status_code}")
        print(response.json())
        print()


async def test_sync_conditions():
    """Test condition sync"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/conditions/sync")
        print(f"Sync Conditions: {response.status_code}")
        if response.status_code == 200:
            conditions = response.json()
            print(f"Synced {len(conditions)} conditions")
            for cond in conditions[:3]:
                print(f"  - {cond['name']} (seq: {cond['seq']})")
        else:
            print(response.text)
        print()


async def main():
    """Run all tests"""
    print("="*60)
    print("Testing Kiwoom Trading Platform API")
    print("="*60)
    print()
    
    try:
        await test_health()
        await test_root()
        
        print("="*60)
        print("Authentication Tests")
        print("="*60)
        print()
        
        await test_get_token()
        await test_token_status()
        
        print("="*60)
        print("Condition Tests")
        print("="*60)
        print()
        
        await test_sync_conditions()
        
    except httpx.ConnectError:
        print("❌ Could not connect to server. Make sure it's running:")
        print("   python app/main.py")
        print("   or")
        print("   uvicorn app.main:app --reload")


if __name__ == "__main__":
    asyncio.run(main())
