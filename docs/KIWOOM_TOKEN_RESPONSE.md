# 키움증권 토큰 응답 구조

**작성일**: 2025-11-08  
**검증 방법**: 실제 API 응답 확인

---

## 📊 실제 응답 구조

### 키움증권 토큰 발급 응답

```json
{
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다",
    "token": "R22y0dDGXMrL56ZKARtZnO4_tlCVr7ZGliUmv_dLZGN5NJ1-HrWpUEj0yC7KvLDlVY4Dvkgl75iIpOA4UxbNPA",
    "token_type": "Bearer",
    "expires_dt": "20251109235445"
}
```

---

## 🔍 필드 설명

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| **return_code** | integer | 응답 코드 (0: 성공) | `0` |
| **return_msg** | string | 응답 메시지 | `"정상적으로 처리되었습니다"` |
| **token** | string | 액세스 토큰 | `"R22y0dDGXM..."` (86자) |
| **token_type** | string | 토큰 타입 | `"Bearer"` |
| **expires_dt** | string | 만료 일시 (YYYYMMDDHHmmss) | `"20251109235445"` |

---

## ⚠️ 중요한 차이점

### 일반적인 OAuth 2.0 응답 (표준)

```json
{
    "access_token": "...",  // ⚠️ 'access_token'
    "token_type": "Bearer",
    "expires_in": 86400     // ⚠️ 'expires_in' (초 단위)
}
```

### 키움증권 응답 (실제)

```json
{
    "token": "...",         // ✅ 'token' (not 'access_token')
    "token_type": "Bearer",
    "expires_dt": "20251109235445",  // ✅ 'expires_dt' (datetime string)
    "return_code": 0,       // ✅ 추가 필드
    "return_msg": "..."     // ✅ 추가 필드
}
```

---

## 🔧 코드 수정 사항

### 변경 전 (표준 OAuth 가정)

```python
access_token = response.get("access_token")  # ❌
expires_in = response.get("expires_in", 86400)  # ❌

if not access_token:
    raise AuthenticationException("No access token in response")
```

### 변경 후 (키움증권 실제 응답)

```python
# 1. 응답 코드 확인
return_code = response.get("return_code")
if return_code != 0:
    error_msg = response.get("return_msg", "Unknown error")
    raise AuthenticationException(f"Token request failed: {error_msg}")

# 2. 토큰 추출
access_token = response.get("token")  # ✅ 'token'

# 3. 만료 시간 파싱
expires_dt_str = response.get("expires_dt")  # ✅ '20251109235445'
expires_dt = datetime.strptime(expires_dt_str, "%Y%m%d%H%M%S")
expires_in = int((expires_dt - datetime.now()).total_seconds())
```

---

## 📝 expires_dt 파싱

### 형식
- **포맷**: `YYYYMMDDHHmmss`
- **예시**: `20251109235445` = 2025년 11월 9일 23시 54분 45초

### 파싱 코드

```python
from datetime import datetime

expires_dt_str = "20251109235445"
expires_dt = datetime.strptime(expires_dt_str, "%Y%m%d%H%M%S")

# datetime(2025, 11, 9, 23, 54, 45)
```

### expires_in 계산

```python
from datetime import datetime

expires_dt = datetime.strptime("20251109235445", "%Y%m%d%H%M%S")
now = datetime.now()
expires_in = int((expires_dt - now).total_seconds())

# 예: 86400 (24시간)
```

---

## 🎯 응답 코드

### return_code 값

| 코드 | 의미 | 처리 |
|------|------|------|
| **0** | 성공 | 토큰 저장 및 사용 |
| **non-0** | 실패 | return_msg 확인 및 에러 처리 |

### 에러 응답 예시

```json
{
    "return_code": 1001,
    "return_msg": "유효하지 않은 앱키입니다"
}
```

---

## 🔄 전체 플로우

### 1. 요청

```python
POST https://api.kiwoom.com/oauth2/token
Content-Type: application/json

{
    "grant_type": "client_credentials",
    "appkey": "YOUR_APP_KEY",
    "secretkey": "YOUR_SECRET_KEY"
}
```

### 2. 응답 (성공)

```json
{
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다",
    "token": "R22y0dDGXM...",
    "token_type": "Bearer",
    "expires_dt": "20251109235445"
}
```

### 3. 처리

```python
# 1. 응답 코드 확인
if response["return_code"] != 0:
    raise error

# 2. 토큰 추출
token = response["token"]

# 3. 만료 시간 계산
expires_dt = datetime.strptime(response["expires_dt"], "%Y%m%d%H%M%S")
expires_in = (expires_dt - datetime.now()).total_seconds()

# 4. 토큰 저장
token_manager.set_token(token, expires_in)
```

---

## 🧪 테스트 케이스

### 성공 케이스

```python
response = {
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다",
    "token": "R22y0dDGXMrL56ZKARtZnO4_tlCVr7ZGliUmv_dLZGN5NJ1-HrWpUEj0yC7KvLDlVY4Dvkgl75iIpOA4UxbNPA",
    "token_type": "Bearer",
    "expires_dt": "20251109235445"
}

# 예상 결과
access_token = "R22y0dDGXM..."  # ✅
expires_in = 86400  # ✅ (약 24시간)
```

### 실패 케이스 (잘못된 키)

```python
response = {
    "return_code": 1001,
    "return_msg": "유효하지 않은 앱키입니다"
}

# 예상: AuthenticationException 발생
```

### 실패 케이스 (필드 누락)

```python
response = {
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다",
    # "token" 누락!
    "token_type": "Bearer",
    "expires_dt": "20251109235445"
}

# 예상: AuthenticationException("No token in response")
```

---

## 📊 필드 비교표

| 필드 | OAuth 2.0 표준 | 키움증권 실제 | 변환 필요 |
|------|----------------|--------------|----------|
| 토큰 | `access_token` | `token` | ✅ |
| 만료 | `expires_in` (초) | `expires_dt` (datetime) | ✅ |
| 타입 | `token_type` | `token_type` | ❌ |
| 응답 코드 | HTTP status | `return_code` | ✅ |
| 응답 메시지 | - | `return_msg` | ✅ |

---

## 🎓 베스트 프랙티스

### 1. 응답 검증

```python
# 1단계: return_code 확인
if response.get("return_code") != 0:
    error_msg = response.get("return_msg", "Unknown error")
    raise AuthenticationException(f"API error: {error_msg}")

# 2단계: 필수 필드 확인
token = response.get("token")
if not token:
    raise AuthenticationException("No token in response")

# 3단계: 만료 시간 파싱 (with fallback)
expires_dt_str = response.get("expires_dt")
if expires_dt_str:
    try:
        expires_dt = datetime.strptime(expires_dt_str, "%Y%m%d%H%M%S")
        expires_in = int((expires_dt - datetime.now()).total_seconds())
    except Exception as e:
        logger.warning(f"Failed to parse expires_dt: {e}")
        expires_in = 86400  # Fallback to 24 hours
else:
    expires_in = 86400  # Default
```

### 2. 로깅

```python
logger.info(
    f"Access token acquired: "
    f"expires_at={expires_dt_str}, "
    f"remaining={expires_in}s, "
    f"msg={response.get('return_msg')}"
)
```

### 3. 에러 처리

```python
try:
    token = await client.get_access_token()
except AuthenticationException as e:
    logger.error(f"Token acquisition failed: {e}")
    # 재시도 로직 또는 알림
```

---

## 🔗 참고

### 관련 파일
- `app/client/rest_client.py` - 토큰 발급 로직
- `app/core/security.py` - 토큰 저장 및 관리
- `scripts/test_token.py` - 토큰 테스트 스크립트

### 관련 문서
- `docs/접근토큰발급_샘플_코드.md` - 공식 샘플 코드
- `docs/KIWOOM_API_FINAL_VERIFICATION.md` - API 검증 문서

---

## ✅ 체크리스트

수정 완료:
- [x] `token` 필드로 토큰 추출 (not `access_token`)
- [x] `expires_dt` 파싱 및 `expires_in` 계산
- [x] `return_code` 검증
- [x] `return_msg` 에러 메시지 처리
- [x] 예외 처리 및 fallback 로직

테스트 필요:
- [ ] 실제 API 키로 토큰 발급 테스트
- [ ] 만료 시간 계산 검증
- [ ] 에러 응답 처리 확인

---

**요약**: 키움증권 API는 표준 OAuth 2.0과 다른 응답 구조를 사용합니다!
- `access_token` → `token`
- `expires_in` → `expires_dt` (datetime string)
- 추가: `return_code`, `return_msg`
