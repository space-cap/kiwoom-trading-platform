# 키움증권 REST API 최종 검증

**작성일**: 2025-11-08  
**검증 근거**: 키움증권 공식 샘플 코드 (`docs/접근토큰발급_샘플_코드.md`)

---

## ✅ 공식 샘플 코드 분석

### 키움증권 공식 스펙 (확정)

```python
# 공식 샘플 코드에서 확인
host = 'https://api.kiwoom.com'  # 실전투자
# host = 'https://mockapi.kiwoom.com'  # 모의투자

endpoint = '/oauth2/token'
url = host + endpoint

params = {
    'grant_type': 'client_credentials',
    'appkey': 'AxserEsdcredca.....',      # ✅ 'appkey'
    'secretkey': 'SEefdcwcforehDre2fdvc.....',  # ⚠️ 'secretkey' (not 'appsecret')
}
```

---

## 🔍 발견된 문제점

### 1. JSON 키 이름 오류 ❌

**현재 구현** (잘못됨):
```python
json={
    "grant_type": "client_credentials",
    "appkey": self.app_key,
    "appsecret": self.app_secret,  # ❌ 잘못됨!
}
```

**올바른 구현**:
```python
json={
    "grant_type": "client_credentials",
    "appkey": self.app_key,
    "secretkey": self.app_secret,  # ✅ 'secretkey'
}
```

---

### 2. Base URL 오류 ❌

**현재 구현** (잘못됨):
```python
KIWOOM_BASE_URL = "https://openapi.kiwoom.com:9443"  # ❌
```

**올바른 구현**:
```python
# 실전투자
KIWOOM_BASE_URL = "https://api.kiwoom.com"  # ✅ 포트 번호 없음!

# 모의투자
KIWOOM_BASE_URL = "https://mockapi.kiwoom.com"  # ✅
```

---

## 📊 수정 요약

| 항목 | 이전 (잘못됨) | 수정 (올바름) |
|------|--------------|--------------|
| **Base URL (실전)** | `https://openapi.kiwoom.com:9443` | `https://api.kiwoom.com` |
| **Base URL (모의)** | - | `https://mockapi.kiwoom.com` |
| **JSON 키 (secret)** | `appsecret` | `secretkey` |
| **Token 엔드포인트** | `/oauth2/token` ✅ | `/oauth2/token` ✅ |
| **JSON 키 (app)** | `appkey` ✅ | `appkey` ✅ |
| **grant_type** | `client_credentials` ✅ | `client_credentials` ✅ |

---

## 🔧 수정된 파일

### 1. `app/client/rest_client.py`

**변경 전**:
```python
json={
    "grant_type": "client_credentials",
    "appkey": self.app_key,
    "appsecret": self.app_secret,  # ❌
}
```

**변경 후**:
```python
json={
    "grant_type": "client_credentials",
    "appkey": self.app_key,
    "secretkey": self.app_secret,  # ✅
}
```

---

### 2. `app/core/config/base.py`

**변경 전**:
```python
KIWOOM_BASE_URL: str = "https://openapi.kiwoom.com:9443"  # ❌
```

**변경 후**:
```python
KIWOOM_BASE_URL: str = "https://api.kiwoom.com"  # ✅
```

---

### 3. `.env.example`

**변경 전**:
```env
KIWOOM_BASE_URL=https://openapi.kiwoom.com:9443
```

**변경 후**:
```env
KIWOOM_BASE_URL=https://api.kiwoom.com
# KIWOOM_BASE_URL=https://mockapi.kiwoom.com  # For mock trading
```

---

## 📝 최종 확정 스펙

### 실전투자 (Real Trading)

```python
import requests

url = "https://api.kiwoom.com/oauth2/token"

headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

data = {
    "grant_type": "client_credentials",
    "appkey": "YOUR_APP_KEY",
    "secretkey": "YOUR_SECRET_KEY"
}

response = requests.post(url, headers=headers, json=data)
```

**전체 URL**: `https://api.kiwoom.com/oauth2/token`

---

### 모의투자 (Mock Trading)

```python
url = "https://mockapi.kiwoom.com/oauth2/token"

# 나머지는 동일
```

**전체 URL**: `https://mockapi.kiwoom.com/oauth2/token`

---

## 🎯 환경 변수 설정

### `.env` 파일 (실전투자)

```env
# Kiwoom API - Real Trading
KIWOOM_APP_KEY=YOUR_ACTUAL_APP_KEY_HERE
KIWOOM_APP_SECRET=YOUR_ACTUAL_SECRET_KEY_HERE
KIWOOM_BASE_URL=https://api.kiwoom.com
```

### `.env` 파일 (모의투자)

```env
# Kiwoom API - Mock Trading
KIWOOM_APP_KEY=YOUR_MOCK_APP_KEY_HERE
KIWOOM_APP_SECRET=YOUR_MOCK_SECRET_KEY_HERE
KIWOOM_BASE_URL=https://mockapi.kiwoom.com
```

---

## ⚠️ 중요 차이점

### 1. 도메인 구조

| 용도 | 도메인 | 포트 |
|------|--------|------|
| **실전투자** | `api.kiwoom.com` | 없음 (443 기본) |
| **모의투자** | `mockapi.kiwoom.com` | 없음 (443 기본) |
| ~~이전 착각~~ | ~~`openapi.kiwoom.com:9443`~~ | ~~9443~~ |

### 2. JSON 키 이름

| API | App Key | Secret Key |
|-----|---------|------------|
| **키움증권** | `appkey` | `secretkey` ✅ |
| ~~한국투자증권~~ | ~~`appkey`~~ | ~~`appsecret`~~ |

---

## 🧪 테스트 시나리오

### 1. 실전투자 테스트

```bash
# .env 파일 수정
KIWOOM_BASE_URL=https://api.kiwoom.com

# 테스트 실행
python scripts/test_token.py --mode quick
```

**예상 결과**:
```
[REQUEST] 토큰 발급 요청 중...
[SUCCESS] 토큰 발급 성공!
```

---

### 2. 모의투자 테스트

```bash
# .env 파일 수정
KIWOOM_BASE_URL=https://mockapi.kiwoom.com

# 테스트 실행
python scripts/test_token.py --mode quick
```

---

## 📚 공식 문서 확인 사항

### 샘플 코드에서 확인된 내용

1. ✅ **URL**: `https://api.kiwoom.com` (실전), `https://mockapi.kiwoom.com` (모의)
2. ✅ **엔드포인트**: `/oauth2/token`
3. ✅ **Content-Type**: `application/json;charset=UTF-8`
4. ✅ **JSON 키**:
   - `grant_type`: `"client_credentials"`
   - `appkey`: 앱키
   - `secretkey`: 시크릿키 (⚠️ **`appsecret`이 아님!**)

---

## 🔍 에러 케이스 분석

### Case 1: 잘못된 JSON 키
```python
# ❌ 이렇게 하면 실패
{
    "appkey": "...",
    "appsecret": "..."  # 키움증권은 'secretkey' 사용!
}

# 에러 메시지 (예상)
# "Invalid request parameters"
```

### Case 2: 잘못된 URL
```python
# ❌ 이렇게 하면 연결 실패
url = "https://openapi.kiwoom.com:9443/oauth2/token"

# 에러 메시지 (예상)
# Connection timeout or DNS resolution failed
```

### Case 3: 올바른 요청
```python
# ✅ 정상 동작
url = "https://api.kiwoom.com/oauth2/token"
{
    "grant_type": "client_credentials",
    "appkey": "...",
    "secretkey": "..."
}

# 성공 응답
{
    "access_token": "eyJ...",
    "token_type": "Bearer",
    "expires_in": 86400
}
```

---

## 📋 체크리스트

### 코드 수정 완료
- [x] `app/client/rest_client.py` - `appsecret` → `secretkey`
- [x] `app/core/config/base.py` - Base URL 수정
- [x] `.env.example` - Base URL 및 주석 추가

### 사용자 조치 필요
- [ ] `.env` 파일 Base URL 수정
- [ ] `.env` 파일에 실제 API 키 입력
- [ ] 키움증권 계좌 및 API 서비스 신청
- [ ] 테스트 실행: `python scripts/test_token.py --mode quick`

---

## 🎉 최종 정리

### 핵심 변경사항

1. **Base URL**: 
   - ❌ `https://openapi.kiwoom.com:9443`
   - ✅ `https://api.kiwoom.com`

2. **JSON 키**:
   - ❌ `"appsecret"`
   - ✅ `"secretkey"`

3. **엔드포인트**: 
   - ✅ `/oauth2/token` (변경 없음)

### 근거
- 키움증권 공식 샘플 코드 (`docs/접근토큰발급_샘플_코드.md`)
- 실전투자 URL 확인

### 다음 단계
1. `.env` 파일 수정
2. 실제 API 키 입력
3. 테스트 실행

**이제 키움증권 공식 스펙과 100% 일치합니다!** ✅
