"""
조건검색 실행 테스트 스크립트
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.logging import logger
from app.client.websocket_client import KiwoomWebSocketClient
from app.client.rest_client import KiwoomRestClient
from app.core.security import token_manager


def print_separator(title: str = ""):
    """출력 구분선"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'='*60}\n")


async def test_condition_search():
    """조건검색 실행 테스트"""
    print_separator("조건검색 실행 테스트")
    
    # 토큰 확인 및 필요시 발급
    print("[STEP 1] 토큰 확인 및 발급...")
    
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
        condition_list = await ws_client.get_condition_list()
        
        data = condition_list.get("data", [])
        if not data:
            print("[WARNING] 등록된 조건검색이 없습니다.")
            print("  키움 HTS에서 조건검색을 먼저 등록해주세요.")
            return False
        
        print(f"[SUCCESS] {len(data)}개의 조건검색 발견\n")
        
        # 조건검색 목록 출력
        print("[조건검색 목록]")
        for idx, condition in enumerate(data, 1):
            cond_index, cond_name = condition
            print(f"  {idx}. [{cond_index}] {cond_name}")
        
        # 첫 번째 조건으로 검색 실행
        first_condition = data[21]
        seq, cond_name = first_condition
        
        print(f"\n[STEP 4] 조건검색 실행: [{seq}] {cond_name}")
        
        search_result = await ws_client.search_condition(seq)
        
        print("[SUCCESS] 조건검색 실행 성공!\n")
        
        # 결과 출력
        print("[검색 결과]")
        print(f"  return_code: {search_result.get('return_code')}")
        print(f"  return_msg: {search_result.get('return_msg')}")
        
        result_data = search_result.get("data", [])
        print(f"\n[종목 수]: {len(result_data)}개\n")
        
        if result_data:
            print("[종목 목록] (최대 10개)")
            for idx, stock in enumerate(result_data[:10], 1):
                # 응답 형식: dict with keys '9001' (종목코드), '302' (종목명)
                if isinstance(stock, dict):
                    stock_code = stock.get('9001', 'N/A').strip()  # 'A005930' 형식
                    stock_name = stock.get('302', 'N/A').strip()
                    current_price = stock.get('10', '0').strip()
                    
                    # 종목코드에서 'A' 제거 (A005930 -> 005930)
                    if stock_code.startswith('A'):
                        stock_code = stock_code[1:]
                    
                    print(f"  {idx}. [{stock_code}] {stock_name} - 현재가: {current_price}")
                else:
                    print(f"  {idx}. {stock}")
            
            if len(result_data) > 10:
                print(f"  ... 외 {len(result_data) - 10}개")
        else:
            print("  (조건에 맞는 종목이 없습니다)")
        
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
        print(f"[ERROR] 테스트 실패: {e}")
        logger.exception("Condition search test failed")
        
        # 연결 종료
        await ws_client.disconnect()
        
        return False


async def test_specific_condition(condition_index: str):
    """특정 조건검색 실행 테스트"""
    print_separator(f"조건검색 실행: 인덱스 {condition_index}")
    
    # 토큰 확인
    if not token_manager.is_token_valid():
        print("[INFO] 토큰 발급 중...")
        rest_client = KiwoomRestClient()
        async with rest_client:
            await rest_client.get_access_token()
    
    # WebSocket 연결
    ws_client = KiwoomWebSocketClient()
    receive_task = asyncio.create_task(ws_client.run())
    
    try:
        await asyncio.sleep(2)
        
        if not ws_client.connected:
            print("[ERROR] WebSocket 연결 실패")
            return False
        
        # 조건검색 실행
        print(f"[INFO] 조건검색 실행 중: {condition_index}")
        result = await ws_client.search_condition(condition_index)
        
        print("[SUCCESS] 조건검색 성공!\n")
        
        # 결과 출력
        data = result.get("data", [])
        print(f"[검색 결과]: {len(data)}개 종목\n")
        
        for idx, stock in enumerate(data[:20], 1):
            if isinstance(stock, dict):
                code = stock.get('9001', '').strip()
                name = stock.get('302', '').strip()
                price = stock.get('10', '').strip()
                if code.startswith('A'):
                    code = code[1:]
                print(f"  {idx}. [{code}] {name} - {price}")
        
        if len(data) > 20:
            print(f"  ... 외 {len(data) - 20}개")
        
        await ws_client.disconnect()
        
        try:
            await asyncio.wait_for(receive_task, timeout=1.0)
        except asyncio.TimeoutError:
            pass
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")
        logger.exception("Specific condition search failed")
        await ws_client.disconnect()
        return False


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="조건검색 실행 테스트")
    parser.add_argument(
        "--index",
        type=str,
        help="조건검색 인덱스 (지정 시 해당 조건만 실행)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.index:
            # 특정 조건검색 실행
            success = asyncio.run(test_specific_condition(args.index))
        else:
            # 전체 테스트 (목록 조회 후 첫 번째 실행)
            success = asyncio.run(test_condition_search())
        
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n[경고] 사용자가 중단했습니다.")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        logger.exception("Test script failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
