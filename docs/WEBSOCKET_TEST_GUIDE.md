# WebSocket 테스트 가이드

**작성일**: 2025-11-08

---

## 📋 사전 준비

### 1. websockets 패키지 설치

```bash
# UV 사용
uv pip install websockets

# 또는 직접 설치
pip install websockets>=12.0
```

### 2. 환경 설정 확인

`.env` 파일 확인:
```bash
cat .env
```

**필수 설정**:
```env
KIWOOM_APP_KEY=실제_앱_키
KIWOOM_APP_SECRET=실제_시크릿키
KIWOOM_BASE_URL=https://api.kiwoom.com
```

### 3. 실제 API 키 입력

`.env` 파일에 키움증권에서 발급받은 **실제 API 키**를 입력해야 합니다.

---

## 🚀 테스트 실행 방법

### 방법 1: 전체 테스트 (권장)

```bash
# 가상환경 활성화
.venv\Scripts\activate

# 전체 테스트 실행
python scripts/test_websocket.py --mode all
```

**또는 UV 사용**:
```bash
uv run python scripts/test_websocket.py --mode all
```

**실행 순서**:
1. WebSocket 로그인 테스트
2. 조건검색 목록조회 테스트

---

### 방법 2: 로그인만 테스트

```bash
python scripts/test_websocket.py --mode login
```

**테스트 내용**:
- REST API 토큰 발급 (또는 기존 토큰 사용)
- WebSocket 연결
- 자동 로그인
- 응답 확인

---

### 방법 3: 조건검색 목록조회만 테스트

```bash
python scripts/test_websocket.py --mode list
```

**테스트 내용**:
- 토큰 확인/발급
- WebSocket 연결
- CNSRLST 요청
- 조건검색 목록 출력

---

## 📊 예상 출력

### 성공 시 (--mode all)

```
============================================================
  WebSocket 조건검색 목록조회 테스트
============================================================

============================================================
  1. WebSocket 로그인 테스트
============================================================

[STEP 1] 토큰 확인 및 발급...
[INFO] 기존 토큰 사용 (유효함)
  - 토큰: R22y0dDGXMrL56ZKARt...

[STEP 2] WebSocket 연결 및 로그인...
2025-11-08 23:45:12 - kiwoom - INFO - Connecting to WebSocket server: wss://api.kiwoom.com:10000/api/dostk/websocket
2025-11-08 23:45:13 - kiwoom - INFO - WebSocket connected successfully
2025-11-08 23:45:13 - kiwoom - INFO - Sending LOGIN packet to WebSocket server
2025-11-08 23:45:14 - kiwoom - INFO - WebSocket login successful
[SUCCESS] WebSocket 로그인 성공!

============================================================
  2. 조건검색 목록조회 테스트
============================================================

[STEP 1] 토큰 확인 및 발급...
[INFO] 기존 토큰 사용 (유효함)
  - 만료 시간: 2025-11-09 23:45:12
  - 남은 시간: 86340초

[STEP 2] WebSocket 연결...
2025-11-08 23:45:15 - kiwoom - INFO - Connecting to WebSocket server: wss://api.kiwoom.com:10000/api/dostk/websocket
2025-11-08 23:45:16 - kiwoom - INFO - WebSocket connected successfully
2025-11-08 23:45:16 - kiwoom - INFO - WebSocket login successful
[SUCCESS] WebSocket 연결 성공

[STEP 3] 조건검색 목록 조회...
2025-11-08 23:45:17 - kiwoom - INFO - Condition list request sent
2025-11-08 23:45:18 - kiwoom - INFO - WebSocket response received: CNSRLST
[SUCCESS] 조건검색 목록 조회 성공!

[응답 데이터]
  return_code: 0
  return_msg: 

[조건검색 목록]
  1. [0] 상승추세
  2. [1] 거래량급증
  3. [2] 신고가돌파
  4. [3] 골든크로스
  5. [4] 급등주

============================================================
  테스트 결과 요약
============================================================

  [SUCCESS] WebSocket 로그인
  [SUCCESS] 조건검색 목록조회

총 2개 중 2개 성공
============================================================
```

---

### 실패 시 (토큰 오류)

```
[STEP 1] 토큰 확인 및 발급...
[INFO] 유효한 토큰이 없음, 새로 발급...
2025-11-08 23:45:12 - kiwoom - ERROR - HTTP error: 403 - {"error_description":"유효하지 않은 AppKey입니다.","error_code":"EGW00103"}
[ERROR] 토큰 발급 실패: Token acquisition failed: HTTP 403
```

**해결**: `.env` 파일에 실제 API 키 입력

---

### 실패 시 (WebSocket 연결 오류)

```
[STEP 2] WebSocket 연결...
2025-11-08 23:45:15 - kiwoom - ERROR - WebSocket connection error: [Errno 11001] getaddrinfo failed
[ERROR] WebSocket 연결 실패
```

**원인**:
1. 네트워크 연결 문제
2. 방화벽 차단
3. VPN 사용 중

---

### 조건검색이 없는 경우

```
[조건검색 목록]
  (등록된 조건검색이 없습니다)
```

**해결**: 키움 HTS에서 조건검색 등록 필요

---

## 🔧 문제 해결

### 1. ModuleNotFoundError: No module named 'websockets'

```bash
# 설치
uv pip install websockets
# 또는
pip install websockets>=12.0
```

---

### 2. 토큰 발급 실패 (403 Forbidden)

**원인**: `.env` 파일의 API 키가 잘못되었거나 마스킹된 예제

**확인**:
```bash
cat .env | grep KIWOOM_APP_KEY
```

**수정**:
```bash
notepad .env
```

실제 키로 교체:
```env
KIWOOM_APP_KEY=YOUR_ACTUAL_APP_KEY
KIWOOM_APP_SECRET=YOUR_ACTUAL_SECRET_KEY
```

---

### 3. WebSocket 연결 실패

**원인 1**: Base URL이 잘못됨

`.env` 확인:
```env
KIWOOM_BASE_URL=https://api.kiwoom.com  # ✅ 올바름
# KIWOOM_BASE_URL=https://openapi.kiwoom.com  # ❌ 틀림
```

**원인 2**: 네트워크 차단

```bash
# 연결 테스트
ping api.kiwoom.com
```

**원인 3**: 방화벽 차단 (포트 10000)

방화벽에서 포트 10000 허용

---

### 4. 타임아웃 오류

```
[ERROR] 조건검색 목록 조회 실패: Condition list request timeout
```

**원인**: 
- 서버 응답이 늦음
- WebSocket 연결 불안정

**해결**: 재시도

---

## 🎯 단계별 테스트

### Step 1: 토큰 테스트

```bash
python scripts/test_token.py --mode quick
```

**예상 결과**:
```
[SUCCESS] 토큰 발급 성공!
```

---

### Step 2: WebSocket 로그인 테스트

```bash
python scripts/test_websocket.py --mode login
```

**예상 결과**:
```
[SUCCESS] WebSocket 로그인 성공!
```

---

### Step 3: 조건검색 목록조회 테스트

```bash
python scripts/test_websocket.py --mode list
```

**예상 결과**:
```
[SUCCESS] 조건검색 목록 조회 성공!
[조건검색 목록]
  1. [0] 조건1
  2. [1] 조건2
```

---

## 📝 체크리스트

테스트 전 확인:

- [ ] `websockets` 패키지 설치됨
- [ ] `.env` 파일에 실제 API 키 입력됨
- [ ] `KIWOOM_BASE_URL=https://api.kiwoom.com` 설정됨
- [ ] 네트워크 연결 정상
- [ ] 방화벽에서 포트 10000 허용
- [ ] 키움 HTS에서 조건검색 등록됨 (선택)

---

## 🐛 디버그 모드

로그를 더 자세히 보려면:

```bash
# 환경 변수 설정
set LOG_LEVEL=DEBUG

# 테스트 실행
python scripts/test_websocket.py --mode all
```

**또는 `.env` 파일 수정**:
```env
LOG_LEVEL=DEBUG
```

---

## 💡 팁

### 1. 빠른 테스트

```bash
# 로그인만 (가장 빠름)
python scripts/test_websocket.py --mode login
```

### 2. 반복 테스트

```bash
# 여러 번 실행해도 기존 토큰 재사용
python scripts/test_websocket.py --mode list
python scripts/test_websocket.py --mode list  # 빠름!
```

### 3. 로그 확인

```bash
# 다른 터미널에서
tail -f logs/app.log
```

---

## 🎓 다음 단계

1. ✅ WebSocket 로그인 성공
2. ✅ 조건검색 목록 조회 성공
3. ⏳ 조건검색 실행 기능 추가
4. ⏳ 실시간 조건검색 알림 추가

---

## 📞 문의

문제가 계속되면:
1. `logs/app.log` 파일 확인
2. 에러 메시지 전체 복사
3. 환경 정보 확인 (OS, Python 버전)

---

**준비되었으면 실행하세요!** 🚀

```bash
python scripts/test_websocket.py --mode all
```
