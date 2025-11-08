"""
WebSocket 조건검색 목록조회 테스트 스크립트
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.logging import logger
from app.client.websocket_client import KiwoomWebSocketClient
from app.client.rest_client import KiwoomRestClient


def print_separator(title: str = ""):
    """출력 구분선"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'='*60}\n")


async def test_websocket_login():
    """WebSocket 로그인 테스트"""
    print_separator("1. WebSocket 로그인 테스트")
    
    # 토큰 확인 및 필요시 발급
    print("[STEP 1] 토큰 확인 및 발급...")
    from app.core.security import token_manager
    
    if token_manager.is_token_valid():
        print("[INFO] 기존 토큰 사용 (유효함)")
        token = token_manager.get_token()
        print(f"  - 토큰: {token[:20]}...")
    else:
        print("[INFO] 유효한 토큰이 없음, 새로 발급...")
        rest_client = KiwoomRestClient()
        try:
            async with rest_client:
                token = await rest_client.get_access_token()
            print(f"[SUCCESS] 토큰 발급 성공: {token[:20]}...")
        except Exception as e:
            print(f"[ERROR] 토큰 발급 실패: {e}")
            return False
    
    # WebSocket 연결 및 로그인
    print("\n[STEP 2] WebSocket 연결 및 로그인...")
    ws_client = KiwoomWebSocketClient()
    
    try:
        success = await ws_client.connect()
        if success:
            print("[SUCCESS] WebSocket 로그인 성공!")
            
            # 메시지 수신 태스크 시작 (백그라운드)
            receive_task = asyncio.create_task(ws_client.receive_messages())
            
            # 잠시 대기 (로그인 응답 수신)
            await asyncio.sleep(2)
            
            # 연결 종료
            await ws_client.disconnect()
            
            # 수신 태스크 종료 대기
            try:
                await asyncio.wait_for(receive_task, timeout=1.0)
            except asyncio.TimeoutError:
                pass
            
            return True
        else:
            print("[ERROR] WebSocket 로그인 실패")
            return False
            
    except Exception as e:
        print(f"[ERROR] WebSocket 테스트 실패: {e}")
        logger.exception("WebSocket login test failed")
        return False


async def test_condition_list():
    """조건검색 목록조회 테스트"""
    print_separator("2. 조건검색 목록조회 테스트")
    
    # 토큰 확인 및 필요시 발급
    print("[STEP 1] 토큰 확인 및 발급...")
    from app.core.security import token_manager
    
    if token_manager.is_token_valid():
        print("[INFO] 기존 토큰 사용 (유효함)")
        token_info = token_manager.get_token_info()
        print(f"  - 만료 시간: {token_info.get('expires_at')}")
        print(f"  - 남은 시간: {token_info.get('remaining_seconds')}초")
    else:
        print("[INFO] 유효한 토큰이 없음, 새로 발급...")
        rest_client = KiwoomRestClient()
        try:
            async with rest_client:
                await rest_client.get_access_token()
            print("[SUCCESS] 토큰 발급 성공")
        except Exception as e:
            print(f"[ERROR] 토큰 발급 실패: {e}")
            return False
    
    # WebSocket 클라이언트 생성
    print("\n[STEP 2] WebSocket 연결...")
    ws_client = KiwoomWebSocketClient()
    
    # 메시지 수신 태스크 시작 (백그라운드)
    receive_task = asyncio.create_task(ws_client.run())
    
    try:
        # 연결 대기
        await asyncio.sleep(2)
        
        if not ws_client.connected:
            print("[ERROR] WebSocket 연결 실패")
            return False
        
        print("[SUCCESS] WebSocket 연결 성공")
        
        # 조건검색 목록 조회
        print("\n[STEP 3] 조건검색 목록 조회...")
        response = await ws_client.get_condition_list()
        
        print("[SUCCESS] 조건검색 목록 조회 성공!\n")
        
        # 응답 출력
        print("[응답 데이터]")
        print(f"  return_code: {response.get('return_code')}")
        print(f"  return_msg: {response.get('return_msg')}")
        print(f"\n[조건검색 목록]")
        
        data = response.get("data", [])
        if data:
            for idx, condition in enumerate(data, 1):
                cond_id, cond_name = condition
                print(f"  {idx}. [{cond_id}] {cond_name}")
        else:
            print("  (등록된 조건검색이 없습니다)")
        
        print()
        
        # 연결 종료
        await ws_client.disconnect()
        
        # 수신 태스크 종료 대기
        try:
            await asyncio.wait_for(receive_task, timeout=1.0)
        except asyncio.TimeoutError:
            pass
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 조건검색 목록 조회 실패: {e}")
        logger.exception("Condition list test failed")
        
        # 연결 종료
        await ws_client.disconnect()
        
        return False


async def run_all_tests():
    """전체 테스트 실행"""
    print_separator("WebSocket 조건검색 목록조회 테스트")
    
    results = []
    
    # 1. WebSocket 로그인 테스트
    result = await test_websocket_login()
    results.append(("WebSocket 로그인", result))
    
    if not result:
        print("\n[경고] WebSocket 로그인 실패로 이후 테스트를 건너뜁니다.")
        return
    
    # 잠시 대기
    await asyncio.sleep(1)
    
    # 2. 조건검색 목록조회 테스트
    result = await test_condition_list()
    results.append(("조건검색 목록조회", result))
    
    # 결과 요약
    print_separator("테스트 결과 요약")
    
    for name, result in results:
        status = "[SUCCESS]" if result else "[FAILED]"
        print(f"  {status} {name}")
    
    success_count = sum(1 for _, r in results if r)
    total_count = len(results)
    
    print(f"\n총 {total_count}개 중 {success_count}개 성공")
    print_separator()


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WebSocket 조건검색 목록조회 테스트")
    parser.add_argument(
        "--mode",
        choices=["login", "list", "all"],
        default="all",
        help="테스트 모드 (기본: all)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == "login":
            # 로그인 테스트만
            success = asyncio.run(test_websocket_login())
            sys.exit(0 if success else 1)
        
        elif args.mode == "list":
            # 조건검색 목록조회 테스트만
            success = asyncio.run(test_condition_list())
            sys.exit(0 if success else 1)
        
        else:
            # 전체 테스트
            asyncio.run(run_all_tests())
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\n[경고] 사용자가 중단했습니다.")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        logger.exception("Test script failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
