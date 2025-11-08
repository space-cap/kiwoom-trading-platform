# 토큰 관리 시스템

**날짜**: 2025-11-08  
**버전**: 2.0 (파일 영속성 추가)

---

## 개요

키움 REST API 토큰을 파일에 저장하여 서버 재시작 시에도 토큰을 재사용할 수 있도록 개선했습니다.

---

## 주요 특징

### 1. 파일 영속성
- **저장 위치**: `data/.token`
- **형식**: JSON
- **인코딩**: UTF-8

### 2. 자동 로드
- 서버 시작 시 파일에서 자동으로 토큰 로드
- 만료된 토큰은 자동 삭제

### 3. 동시성 제어
- `threading.Lock`을 사용한 파일 접근 제어
- 여러 프로세스가 안전하게 토큰 공유

### 4. 보안
- Unix 시스템에서 파일 권한 0600 (소유자만 읽기/쓰기)
- `.gitignore`에 등록되어 저장소에 커밋되지 않음

---

## 파일 구조

### data/.token
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-11-09T22:47:56.123456",
  "created_at": "2025-11-08T22:47:56.123456"
}
```

**필드 설명**:
- `access_token`: OAuth 액세스 토큰
- `expires_at`: 만료 시간 (ISO 8601 형식)
- `created_at`: 토큰 생성 시간

---

## API 개선 사항

### 1. set_token()
```python
def set_token(self, access_token: str, expires_in: int) -> None:
    """
    토큰 설정 및 파일 저장
    
    변경사항:
    - 메모리에 저장 후 자동으로 파일에도 저장
    - 로깅 추가
    """
```

### 2. get_token()
```python
def get_token(self) -> Optional[str]:
    """
    토큰 조회
    
    변경사항:
    - 메모리에 없으면 파일에서 자동 로드 시도
    - 만료 확인 (5분 버퍼)
    - 만료 시 자동 삭제
    """
```

### 3. clear_token()
```python
def clear_token(self) -> None:
    """
    토큰 삭제
    
    변경사항:
    - 메모리와 파일 모두 삭제
    - 로깅 추가
    """
```

### 4. get_token_info() (NEW)
```python
def get_token_info(self) -> dict:
    """
    토큰 정보 조회
    
    반환:
    {
        'has_token': bool,
        'is_valid': bool,
        'expires_at': str,
        'remaining_seconds': int,
        'token_preview': str
    }
    """
```

---

## 사용 예제

### 기본 사용 (변경 없음)
```python
from app.core.security import token_manager

# 토큰 설정 (자동으로 파일에 저장됨)
token_manager.set_token("access_token_here", 86400)

# 토큰 조회 (파일에서 자동 로드됨)
token = token_manager.get_token()

# 토큰 유효성 확인
if token_manager.is_token_valid():
    print("Token is valid")
```

### 토큰 정보 조회 (NEW)
```python
info = token_manager.get_token_info()
print(f"Has token: {info['has_token']}")
print(f"Is valid: {info['is_valid']}")
print(f"Expires at: {info['expires_at']}")
print(f"Remaining: {info['remaining_seconds']}s")
```

### 토큰 삭제
```python
# 메모리와 파일에서 모두 삭제
token_manager.clear_token()
```

---

## 동작 흐름

### 서버 시작 시
```
1. TokenManager 초기화
   ↓
2. _load_token_from_file() 호출
   ↓
3. data/.token 파일 확인
   ↓
4-A. 파일이 있고 유효함
   → 메모리에 로드
   → "Loaded valid token from file" 로그
   
4-B. 파일이 없거나 만료됨
   → 파일 삭제
   → 새 토큰 필요
```

### 토큰 발급 시
```
1. API로부터 토큰 수신
   ↓
2. token_manager.set_token() 호출
   ↓
3. 메모리에 저장
   ↓
4. _save_token_to_file() 호출
   ↓
5. data/.token 파일 생성/업데이트
   ↓
6. 파일 권한 설정 (Unix)
   ↓
7. "Token saved to file" 로그
```

### 토큰 조회 시
```
1. get_token() 호출
   ↓
2. 메모리 확인
   ↓
3-A. 메모리에 있음
   → 유효성 확인 (5분 버퍼)
   → 토큰 반환 또는 None
   
3-B. 메모리에 없음
   → _load_token_from_file() 호출
   → 파일에서 로드 시도
   → 토큰 반환 또는 None
```

---

## 보안 고려사항

### 1. 파일 권한
```python
# Unix 시스템
os.chmod(self.TOKEN_FILE, 0o600)  # rw-------
```

**Windows**: 파일 시스템 권한 자동 적용

### 2. .gitignore 등록
```gitignore
# Token files (security)
.token
*.token
```

### 3. 디렉토리 위치
- `data/` 디렉토리에 저장
- `data/` 전체가 `.gitignore`에 포함됨

### 4. 원자적 쓰기
```python
# 임시 파일에 먼저 쓰기
temp_file.write(data)
# 원자적으로 교체
temp_file.replace(self.TOKEN_FILE)
```

---

## 장점

### 1. 서버 재시작 시 토큰 유지
**Before**:
```
서버 시작 → 토큰 없음 → API 호출 → 토큰 발급
```

**After**:
```
서버 시작 → 파일에서 토큰 로드 → 즉시 사용 가능
```

### 2. 여러 프로세스 간 공유
```
API 서버 (uvicorn) ←→ data/.token ←→ 스케줄러
```

두 프로세스가 동일한 토큰 사용

### 3. Rate Limit 절약
- 불필요한 토큰 재발급 방지
- API 호출 횟수 감소

### 4. 디버깅 용이
```bash
# 토큰 상태 확인
cat data/.token

# 토큰 만료 시간 확인
cat data/.token | jq .expires_at
```

---

## 테스트

### 1. 토큰 저장 확인
```python
from app.core.security import token_manager

# 토큰 설정
token_manager.set_token("test_token", 86400)

# 파일 확인
import json
with open("data/.token") as f:
    data = json.load(f)
    print(data)
```

### 2. 서버 재시작 테스트
```bash
# 1. 서버 실행 및 토큰 발급
python app/main.py

# 2. 서버 중지 (Ctrl+C)

# 3. 토큰 파일 확인
cat data/.token

# 4. 서버 재시작
python app/main.py
# → 로그에 "Loaded valid token from file" 출력 확인
```

### 3. 만료 토큰 처리 테스트
```python
import json
from datetime import datetime, timedelta

# 만료된 토큰 파일 생성
data = {
    "access_token": "expired_token",
    "expires_at": (datetime.now() - timedelta(days=1)).isoformat(),
    "created_at": datetime.now().isoformat()
}

with open("data/.token", "w") as f:
    json.dump(data, f)

# 서버 시작
# → 만료된 토큰 자동 삭제 확인
```

---

## 로그 예제

### 정상 로드
```
2025-11-08 22:47:56 - kiwoom - INFO - Loaded valid token from file (expires at 2025-11-09 22:47:56)
```

### 토큰 저장
```
2025-11-08 22:47:56 - kiwoom - INFO - Token set (expires in 86400s)
2025-11-08 22:47:56 - kiwoom - INFO - Token saved to file (expires at 2025-11-09 22:47:56)
```

### 만료된 토큰
```
2025-11-08 22:47:56 - kiwoom - INFO - Token in file has expired
2025-11-08 22:47:56 - kiwoom - DEBUG - Token file deleted
```

### 토큰 삭제
```
2025-11-08 22:47:56 - kiwoom - INFO - Token expired, clearing...
2025-11-08 22:47:56 - kiwoom - INFO - Token cleared
2025-11-08 22:47:56 - kiwoom - DEBUG - Token file deleted
```

---

## 문제 해결

### Q: 토큰 파일이 손상되었을 때?
**A**: 자동으로 감지하고 삭제됩니다.
```python
except json.JSONDecodeError:
    logger.error("Failed to parse token file (invalid JSON)")
    self._delete_token_file()
```

### Q: 여러 프로세스가 동시에 접근하면?
**A**: Lock을 사용하여 안전하게 처리됩니다.
```python
with self.TOKEN_FILE_LOCK:
    # 파일 읽기/쓰기
```

### Q: 파일 권한 문제가 발생하면?
**A**: 
```bash
# Unix
chmod 600 data/.token

# Windows
# 파일 속성 → 보안 → 소유자만 읽기/쓰기
```

### Q: 토큰 파일을 수동으로 삭제하려면?
**A**:
```bash
rm data/.token
# 또는
python -c "from app.core.security import token_manager; token_manager.clear_token()"
```

---

## 마이그레이션

기존 코드는 **변경 불필요**합니다. 기존 API가 그대로 유지되며, 파일 저장 기능만 추가되었습니다.

```python
# 기존 코드 그대로 동작
from app.core.security import token_manager

token = token_manager.get_token()
if not token:
    # 새 토큰 발급
    pass
```

---

## 성능 영향

- **파일 I/O**: 토큰 설정/조회 시에만 발생
- **메모리 우선**: 메모리에 있으면 파일 접근 안함
- **오버헤드**: 거의 없음 (JSON 파싱만)

---

## 향후 개선 사항

1. **암호화**: 토큰을 암호화하여 저장
2. **TTL 모니터링**: 만료 임박 시 사전 갱신
3. **Redis 지원**: 분산 환경을 위한 Redis 백엔드
4. **Refresh Token**: Refresh token 지원

---

**작성자**: Development Team  
**최종 수정**: 2025-11-08
