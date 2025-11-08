# 키움증권 vs 한국투자증권 API 혼동 수정

**작성일**: 2025-11-08  
**중요도**: 🔴 Critical

---

## ⚠️ 중요한 발견

프로젝트에서 **키움증권(Kiwoom Securities)** API와 **한국투자증권(Korea Investment & Securities, KIS)** API가 혼동되어 있었습니다!

---

## 🔍 문제 발견 경위

1. **사용자 지적**: "지금하는 프로젝트는 한국투자증권이 아니다. 키움증권 REST API 사용을 해야 된다."

2. **코드 검증 시도**: 
   - 웹 검색으로 `/oauth2/tokenP` 엔드포인트 발견
   - 이것은 **한국투자증권(KIS)** API의 엔드포인트였음
   - **키움증권(Kiwoom)**은 `/oauth2/token` 사용

3. **Base URL 확인**:
   - 설정: `https://openapi.koreainvestment.com:9443` ❌
   - 올바름: `https://openapi.kiwoom.com:9443` ✅

---

## 📊 두 API 비교

### 키움증권 (Kiwoom Securities) ✅ 우리가 사용해야 할 API

| 항목 | 값 |
|------|-----|
| **회사명** | 키움증권 |
| **영문명** | Kiwoom Securities |
| **Base URL** | `https://openapi.kiwoom.com:9443` |
| **WebSocket** | `wss://openapi.kiwoom.com/ws` |
| **Token Endpoint** | `/oauth2/token` |
| **공식 사이트** | https://openapi.kiwoom.com/ |
| **특징** | 국내 점유율 1위, 조건검색 기능 강력 |

---

### 한국투자증권 (Korea Investment & Securities) ❌ 혼동된 API

| 항목 | 값 |
|------|-----|
| **회사명** | 한국투자증권 (구 대우증권) |
| **영문명** | Korea Investment & Securities (KIS) |
| **Base URL** | `https://openapi.koreainvestment.com:9443` |
| **WebSocket** | `ws://ops.koreainvestment.com:21000` |
| **Token Endpoint** | `/oauth2/tokenP` (P 대문자!) |
| **공식 사이트** | https://apiportal.koreainvestment.com/ |
| **특징** | REST API + WebSocket 제공 |

---

## 🔧 수정된 파일

### 1. `.env.example`

**수정 전**:
```env
KIWOOM_BASE_URL=https://openapi.koreainvestment.com:9443
KIWOOM_WEBSOCKET_URL=ws://ops.koreainvestment.com:21000
```

**수정 후**:
```env
KIWOOM_BASE_URL=https://openapi.kiwoom.com:9443
KIWOOM_WEBSOCKET_URL=wss://openapi.kiwoom.com/ws
```

---

### 2. `app/core/config/base.py`

**수정 전**:
```python
KIWOOM_BASE_URL: str = "https://openapi.koreainvestment.com:9443"
KIWOOM_WEBSOCKET_URL: str = "ws://ops.koreainvestment.com:21000"
```

**수정 후**:
```python
KIWOOM_BASE_URL: str = "https://openapi.kiwoom.com:9443"
KIWOOM_WEBSOCKET_URL: str = "wss://openapi.kiwoom.com/ws"
```

---

### 3. `app/client/rest_client.py`

**확인 결과**: 
```python
"/oauth2/token"  # ✅ 올바름 (키움증권은 /oauth2/token 사용)
```

**주의**: 한국투자증권은 `/oauth2/tokenP` 사용하지만, 키움증권은 `/oauth2/token` 사용!

---

## 📝 OAuth 엔드포인트 비교

### 키움증권 (우리 프로젝트)
```http
POST https://openapi.kiwoom.com:9443/oauth2/token
Content-Type: application/json

{
    "grant_type": "client_credentials",
    "appkey": "YOUR_APP_KEY",
    "appsecret": "YOUR_APP_SECRET"
}
```

### 한국투자증권 (참고용)
```http
POST https://openapi.koreainvestment.com:9443/oauth2/tokenP
Content-Type: application/json

{
    "grant_type": "client_credentials",
    "appkey": "YOUR_APP_KEY",
    "appsecret": "YOUR_APP_SECRET"
}
```

---

## ✅ 검증 완료 사항

### 1. 엔드포인트
- ✅ `/oauth2/token` (키움증권)
- ❌ `/oauth2/tokenP` (한국투자증권 - 혼동했던 것)

### 2. JSON 파라미터
- ✅ `grant_type: client_credentials`
- ✅ `appkey: YOUR_APP_KEY`
- ✅ `appsecret: YOUR_APP_SECRET`

### 3. Base URL
- ✅ `https://openapi.kiwoom.com:9443` (수정 완료)
- ❌ `https://openapi.koreainvestment.com:9443` (이전 잘못된 값)

---

## 🎯 API 키 발급 방법

### 키움증권 REST API 사용 신청

1. **키움증권 계좌 개설**
   - 키움증권 계좌 필요
   - https://www.kiwoom.com/

2. **REST API 서비스 신청**
   - https://openapi.kiwoom.com/
   - 로그인 후 서비스 신청
   - 이용약관 동의

3. **IP 등록**
   - 최대 10개 IP 등록 가능
   - API 요청은 등록된 IP에서만 가능

4. **App Key & App Secret 발급**
   - 앱 등록 후 1회만 다운로드 가능
   - 분실 시 재발급 필요

5. **접근 토큰 발급**
   - OAuth 2.0 Client Credentials Grant
   - 유효기간: 24시간
   - 매일 재발급 필요

---

## 📚 참고 자료

### 키움증권 공식
- **메인**: https://openapi.kiwoom.com/
- **서비스 안내**: https://openapi.kiwoom.com/intro/serviceInfo
- **API 가이드**: https://openapi.kiwoom.com/apiservice (PDF 다운로드)

### 커뮤니티 가이드
- [키움 REST API 완전 가이드](https://insight6910.tistory.com/entry/키움-REST-API-완전)
- [키움증권 REST API로 주식 분봉차트 조회하기](https://iotnbigdata.tistory.com/829)
- [키움 증권 API를 이용하여 주식 자동 매매 프로그램 개발하기](https://steady-coding.tistory.com/268)

---

## 🔍 혼동 방지 팁

### 프로젝트 이름/변수에 명확히 표시
```python
# Good ✅
KIWOOM_APP_KEY
KIWOOM_BASE_URL  # 키움증권임이 명확

# Bad ❌
API_KEY  # 어느 증권사인지 불명확
```

### Base URL로 구분
```python
# 키움증권
"openapi.kiwoom.com"  # ✅

# 한국투자증권
"openapi.koreainvestment.com"  # ❌ (이 프로젝트에서는 사용 안 함)
```

### 엔드포인트로 구분
```python
# 키움증권
"/oauth2/token"  # ✅

# 한국투자증권  
"/oauth2/tokenP"  # ❌ (P가 있으면 한국투자증권)
```

---

## ⚠️ 주의사항

### 1. API 호환성 없음
- 키움증권 API ≠ 한국투자증권 API
- App Key를 서로 교환해서 사용할 수 없음
- 각 증권사에서 별도 발급 필요

### 2. 문서 확인
- **반드시** 키움증권 공식 문서 참조
- 한국투자증권 문서와 혼동 주의
- 커뮤니티 블로그도 어느 증권사 API인지 확인

### 3. 에러 메시지
```
403 Forbidden: "유효하지 않은 AppKey입니다"
→ App Key가 잘못되었거나
→ Base URL이 잘못되었거나 (다른 증권사 URL 사용)
→ IP가 등록되지 않았거나
```

---

## ✅ 체크리스트

수정 완료한 항목:
- [x] `.env.example` Base URL 수정
- [x] `app/core/config/base.py` 기본값 수정
- [x] `app/client/rest_client.py` 엔드포인트 확인 (원래 올바름)
- [x] 문서화 작성

확인 필요한 항목:
- [ ] 실제 `.env` 파일도 Base URL 수정 (사용자가 직접 수정 필요)
- [ ] 키움증권 계좌 보유 여부 확인
- [ ] 키움증권 REST API 서비스 신청
- [ ] App Key & App Secret 발급
- [ ] IP 주소 등록

---

## 🎉 결론

1. **올바른 API**: 키움증권 (Kiwoom Securities)
2. **올바른 Base URL**: `https://openapi.kiwoom.com:9443`
3. **올바른 Token Endpoint**: `/oauth2/token`
4. **코드 수정**: Base URL만 수정하면 됨 (엔드포인트는 원래 올바름)

**다음 단계**: 
1. `.env` 파일의 Base URL 수정
2. 키움증권에서 API 키 발급
3. 실제 키를 `.env`에 입력
4. `python scripts/test_token.py --mode quick` 실행

---

**중요**: 이 프로젝트는 **키움증권 API**를 사용합니다! 한국투자증권이 아닙니다!
