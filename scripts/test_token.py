"""
토큰 발급 및 관리 테스트 스크립트
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.logging import logger
from app.core.security import token_manager
from app.client.rest_client import KiwoomRestClient
from app.core.config import get_settings


def print_separator(title: str = ""):
    """출력 구분선"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'='*60}\n")


def print_token_info():
    """토큰 정보 출력"""
    info = token_manager.get_token_info()
    
    print("[TOKEN INFO] 토큰 상태:")
    print(f"  - 토큰 존재: {info['has_token']}")
    print(f"  - 유효성: {info['is_valid']}")
    
    if info['has_token']:
        print(f"  - 만료 시간: {info['expires_at']}")
        print(f"  - 남은 시간: {info['remaining_seconds']}초")
        print(f"  - 토큰 미리보기: {info['token_preview']}")
    print()


async def test_token_issue():
    """토큰 발급 테스트"""
    print_separator("1. 토큰 발급 테스트")
    
    settings = get_settings()
    
    # API 키 확인
    print("[API KEY] API 설정 확인:")
    print(f"  App Key: {settings.KIWOOM_APP_KEY[:10]}...{settings.KIWOOM_APP_KEY[-5:]}")
    print(f"  App Secret: {settings.KIWOOM_APP_SECRET[:10]}...{settings.KIWOOM_APP_SECRET[-5:]}")
    print(f"  Base URL: {settings.KIWOOM_BASE_URL}")
    print()
    
    # 토큰 발급 시도
    print("[REQUEST] 토큰 발급 요청 중...")
    try:
        client = KiwoomRestClient()
        
        async with client:
            access_token = await client.get_access_token()
        
        print("[SUCCESS] 토큰 발급 성공!")
        print()
        
        # 토큰 정보 출력
        print_token_info()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 토큰 발급 실패: {e}")
        logger.exception("Token issue failed")
        return False


async def test_token_from_file():
    """파일에서 토큰 로드 테스트"""
    print_separator("2. 파일에서 토큰 로드 테스트")
    
    # 토큰 파일 확인
    token_file = Path("data/.token")
    
    if not token_file.exists():
        print("❌ 토큰 파일이 없습니다.")
        print(f"   경로: {token_file.absolute()}")
        print()
        return False
    
    print(f"📁 토큰 파일 발견: {token_file.absolute()}")
    
    # 파일 내용 확인
    try:
        import json
        with open(token_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📄 파일 내용:")
        print(f"  Access Token: {data['access_token'][:30]}...")
        print(f"  Expires At: {data['expires_at']}")
        print(f"  Created At: {data['created_at']}")
        print()
        
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
        return False
    
    # 메모리 초기화 후 다시 로드
    print("🔄 메모리 초기화 후 재로드...")
    token_manager._access_token = None
    token_manager._token_expires_at = None
    
    # 토큰 조회 (자동으로 파일에서 로드됨)
    token = token_manager.get_token()
    
    if token:
        print("✅ 파일에서 토큰 로드 성공!")
        print()
        print_token_info()
        return True
    else:
        print("❌ 토큰 로드 실패 (만료되었거나 유효하지 않음)")
        return False


async def test_token_validity():
    """토큰 유효성 테스트"""
    print_separator("3. 토큰 유효성 테스트")
    
    # 토큰 유효성 확인
    is_valid = token_manager.is_token_valid()
    
    print(f"🔍 토큰 유효성: {'✅ 유효함' if is_valid else '❌ 유효하지 않음'}")
    print()
    
    if is_valid:
        token = token_manager.get_token()
        print(f"📝 토큰: {token[:50]}...")
        print()
    
    return is_valid


async def test_api_call():
    """실제 API 호출 테스트"""
    print_separator("4. 실제 API 호출 테스트")
    
    if not token_manager.is_token_valid():
        print("❌ 유효한 토큰이 없어서 API 호출을 건너뜁니다.")
        return False
    
    print("🌐 조건검색 목록 조회 테스트...")
    
    try:
        client = KiwoomRestClient()
        
        async with client:
            response = await client.get_condition_list()
        
        print("✅ API 호출 성공!")
        print(f"\n📦 응답 데이터:")
        
        import json
        print(json.dumps(response, indent=2, ensure_ascii=False)[:500])
        print("...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ API 호출 실패: {e}")
        logger.exception("API call failed")
        return False


async def test_token_clear():
    """토큰 삭제 테스트"""
    print_separator("5. 토큰 삭제 테스트")
    
    print("🗑️  토큰 삭제 중...")
    token_manager.clear_token()
    
    print("✅ 토큰 삭제 완료!")
    print()
    
    # 파일 확인
    token_file = Path("data/.token")
    if token_file.exists():
        print("❌ 파일이 아직 존재합니다.")
        return False
    else:
        print("✅ 파일도 삭제되었습니다.")
        print()
    
    # 토큰 정보 확인
    print_token_info()
    
    return True


async def interactive_menu():
    """대화형 메뉴"""
    print_separator("토큰 관리 테스트 메뉴")
    
    while True:
        print("\n선택하세요:")
        print("  1. 토큰 발급 (새로 발급)")
        print("  2. 토큰 정보 조회")
        print("  3. 파일에서 토큰 로드")
        print("  4. 토큰 유효성 확인")
        print("  5. API 호출 테스트")
        print("  6. 토큰 삭제")
        print("  7. 전체 테스트 실행")
        print("  0. 종료")
        print()
        
        choice = input("입력: ").strip()
        
        if choice == "1":
            await test_token_issue()
        elif choice == "2":
            print_separator("토큰 정보")
            print_token_info()
        elif choice == "3":
            await test_token_from_file()
        elif choice == "4":
            await test_token_validity()
        elif choice == "5":
            await test_api_call()
        elif choice == "6":
            await test_token_clear()
        elif choice == "7":
            await run_all_tests()
        elif choice == "0":
            print("\n👋 종료합니다.")
            break
        else:
            print("❌ 잘못된 입력입니다.")


async def run_all_tests():
    """모든 테스트 실행"""
    print_separator("🧪 전체 테스트 실행")
    
    results = []
    
    # 1. 토큰 발급
    result = await test_token_issue()
    results.append(("토큰 발급", result))
    
    if not result:
        print("⚠️  토큰 발급 실패로 이후 테스트를 건너뜁니다.")
        return
    
    # 2. 파일에서 로드
    result = await test_token_from_file()
    results.append(("파일 로드", result))
    
    # 3. 유효성 확인
    result = await test_token_validity()
    results.append(("유효성 확인", result))
    
    # 4. API 호출
    result = await test_api_call()
    results.append(("API 호출", result))
    
    # 결과 요약
    print_separator("📊 테스트 결과 요약")
    
    for name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"  {name}: {status}")
    
    success_count = sum(1 for _, r in results if r)
    total_count = len(results)
    
    print(f"\n총 {total_count}개 중 {success_count}개 성공")
    print_separator()


async def quick_test():
    """빠른 테스트 (토큰 발급만)"""
    print_separator("⚡ 빠른 토큰 발급 테스트")
    
    # 현재 토큰 확인
    print("1️⃣ 현재 토큰 확인...")
    print_token_info()
    
    # 토큰 발급
    print("2️⃣ 토큰 발급 시도...")
    success = await test_token_issue()
    
    if success:
        print("3️⃣ 최종 상태:")
        print_token_info()
    
    return success


def main():
    """메인 함수"""
    import argparse
    import sys
    import io
    
    # Windows 콘솔 인코딩 설정
    if sys.platform == 'win32':
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        except:
            pass
    
    parser = argparse.ArgumentParser(description="토큰 관리 테스트 스크립트")
    parser.add_argument(
        "--mode",
        choices=["quick", "all", "interactive"],
        default="interactive",
        help="실행 모드 (기본: interactive)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  [TOKEN TEST] 키움 토큰 관리 테스트")
    print("="*60)
    
    try:
        if args.mode == "quick":
            # 빠른 테스트
            success = asyncio.run(quick_test())
            sys.exit(0 if success else 1)
        
        elif args.mode == "all":
            # 전체 테스트
            asyncio.run(run_all_tests())
            sys.exit(0)
        
        else:
            # 대화형 모드
            asyncio.run(interactive_menu())
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        logger.exception("Test script failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
