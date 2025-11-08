# 조건검색 실행 테스트 가이드

**작성일**: 2025-11-08

---

## 🚀 빠른 시작

### 1. 가상환경 활성화

```bash
.venv\Scripts\activate
```

---

### 2. 테스트 실행

```bash
python scripts/test_condition_search.py
```

---

## 📋 사전 준비 체크리스트

### ✅ 필수 사항

- [ ] `websockets` 패키지 설치됨
- [ ] `.env` 파일에 실제 API 키 입력됨
- [ ] 키움 HTS에서 조건검색 등록됨
- [ ] 토큰 발급 가능 (test_token.py 성공)
- [ ] WebSocket 연결 가능 (test_websocket.py 성공)

---

## 📝 단계별 테스트

### Step 1: 패키지 확인

```bash
pip show websockets
```

**없으면 설치**:
```bash
pip install websockets>=12.0
```

---

### Step 2: 환경 설정 확인

```bash
cat .env
```

**확인 사항**:
```env
KIWOOM_APP_KEY=실제_앱_키      # ⚠️ 별표 아님!
KIWOOM_APP_SECRET=실제_시크릿키 # ⚠️ 별표 아님!
KIWOOM_BASE_URL=https://api.kiwoom.com  # ⚠️ 포트 없음!
```

---

### Step 3: 토큰 테스트 (선택적)

```bash
python scripts/test_token.py --mode quick
```

**예상 결과**:
```
[SUCCESS] 토큰 발급 성공!
```

---

### Step 4: WebSocket 연결 테스트 (선택적)

```bash
python scripts/test_websocket.py --mode login
```

**예상 결과**:
```
[SUCCESS] WebSocket 로그인 성공!
```

---

### Step 5: 조건검색 목록 확인

```bash
python scripts/test_websocket.py --mode list
```

**예상 결과**:
```
[조건검색 목록]
  1. [0] 상승추세
  2. [1] 거래량급증
```

**만약 목록이 비어있다면**:
→ 키움 HTS에서 조건검색을 먼저 등록해야 합니다!

---

### Step 6: 조건검색 실행 테스트 ⭐

```bash
python scripts/test_condition_search.py
```

**이 명령어가 실행하는 작업**:
1. 토큰 확인/발급
2. WebSocket 연결
3. 조건검색 목록 조회
4. 첫 번째 조건 자동 실행
5. 결과 출력

---

## 🎯 테스트 모드

### 모드 1: 자동 테스트 (기본)

```bash
python scripts/test_condition_search.py
```

**동작**:
- 조건검색 목록 조회
- 첫 번째 조건 자동 실행
- 최대 10개 종목 출력

---

### 모드 2: 특정 조건 실행

```bash
python scripts/test_condition_search.py --index 0
```

**동작**:
- 인덱스 "0"인 조건만 실행
- 최대 20개 종목 출력

다른 조건 실행:
```bash
python scripts/test_condition_search.py --index 1
python scripts/test_condition_search.py --index 2
```

---

## 📊 예상 출력

### ✅ 성공 시

```
============================================================
  조건검색 실행 테스트
============================================================

[STEP 1] 토큰 확인 및 발급...
[INFO] 기존 토큰 사용 (유효함)
  - 만료 시간: 2025-11-09 23:45:12
  - 남은 시간: 85200초

[STEP 2] WebSocket 연결...
2025-11-08 23:45:15 - kiwoom - INFO - Connecting to WebSocket server
2025-11-08 23:45:16 - kiwoom - INFO - WebSocket connected successfully
2025-11-08 23:45:16 - kiwoom - INFO - WebSocket login successful
[SUCCESS] WebSocket 연결 성공

[STEP 3] 조건검색 목록 조회...
[SUCCESS] 3개의 조건검색 발견

[조건검색 목록]
  1. [0] 상승추세
  2. [1] 거래량급증
  3. [2] 신고가돌파

[STEP 4] 조건검색 실행: [0] 상승추세
[SUCCESS] 조건검색 실행 성공!

[검색 결과]
  return_code: 0
  return_msg: 

[종목 수]: 42개

[종목 목록] (최대 10개)
  1. [005930] 삼성전자 - 현재가: 000075000
  2. [000660] SK하이닉스 - 현재가: 000145000
  3. [035420] NAVER - 현재가: 000198000
  4. [051910] LG화학 - 현재가: 000425000
  5. [006400] 삼성SDI - 현재가: 000387000
  6. [035720] 카카오 - 현재가: 000048500
  7. [207940] 삼성바이오로직스 - 현재가: 000840000
  8. [068270] 셀트리온 - 현재가: 000185000
  9. [005380] 현대차 - 현재가: 000198000
  10. [000270] 기아 - 현재가: 000092500
  ... 외 32개
```

---

### ❌ 실패 케이스

#### 케이스 1: 조건검색 미등록

```
[STEP 3] 조건검색 목록 조회...
[WARNING] 등록된 조건검색이 없습니다.
  키움 HTS에서 조건검색을 먼저 등록해주세요.
```

**해결 방법**:
1. 영웅문 HTS 실행
2. 조건검색 → 조건 관리
3. 조건식 작성 및 저장
4. 다시 테스트 실행

---

#### 케이스 2: 토큰 발급 실패

```
[STEP 1] 토큰 확인 및 발급...
[INFO] 유효한 토큰이 없음, 새로 발급...
[ERROR] 토큰 발급 실패: HTTP 403
```

**해결 방법**:
```bash
# .env 파일 수정
notepad .env

# 실제 API 키로 교체
KIWOOM_APP_KEY=실제_키
KIWOOM_APP_SECRET=실제_시크릿
```

---

#### 케이스 3: WebSocket 연결 실패

```
[STEP 2] WebSocket 연결...
[ERROR] WebSocket 연결 실패
```

**원인**:
1. 네트워크 문제
2. 방화벽 차단 (포트 10000)
3. Base URL 오류

**해결**:
```bash
# Base URL 확인
cat .env | grep KIWOOM_BASE_URL

# 올바른 값: https://api.kiwoom.com
```

---

#### 케이스 4: 타임아웃

```
[ERROR] 테스트 실패: Condition search request timeout
```

**원인**: 서버 응답 지연

**해결**: 재시도

---

## 🔧 문제 해결

### 문제 1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'websockets'
```

**해결**:
```bash
pip install websockets>=12.0
```

---

### 문제 2: 키움 HTS에서 조건검색 등록하기

**순서**:
1. 영웅문 HTS 실행
2. [0] 메뉴 → 조건검색 → 조건 관리
3. 신규 조건 작성:
   - 조건명: "상승추세" (예시)
   - 조건식: 원하는 조건 설정
   - 저장

4. 조건 확인:
   - 조건검색 창에서 등록된 조건 확인
   - 인덱스 번호 확인 (0, 1, 2, ...)

---

### 문제 3: 빈 결과

```
[종목 수]: 0개

  (조건에 맞는 종목이 없습니다)
```

**원인**: 현재 시장 상황에서 조건에 맞는 종목 없음

**해결**:
- 정상 동작입니다
- 다른 조건으로 테스트
- 또는 조건 완화

---

### 문제 4: 로그 확인

```bash
# 로그 파일 확인
cat logs/app.log

# 실시간 로그
tail -f logs/app.log
```

---

## 🎓 전체 테스트 플로우

### 최초 테스트 (모든 단계)

```bash
# 1. 가상환경 활성화
.venv\Scripts\activate

# 2. 패키지 확인
pip show websockets

# 3. 토큰 테스트
python scripts/test_token.py --mode quick

# 4. WebSocket 로그인 테스트
python scripts/test_websocket.py --mode login

# 5. 조건검색 목록 확인
python scripts/test_websocket.py --mode list

# 6. 조건검색 실행 테스트
python scripts/test_condition_search.py
```

---

### 빠른 테스트 (이미 설정 완료된 경우)

```bash
# 가상환경 활성화
.venv\Scripts\activate

# 바로 실행
python scripts/test_condition_search.py
```

---

## 💡 유용한 명령어

### 특정 조건만 빠르게 테스트

```bash
# 조건 0번 실행
python scripts/test_condition_search.py --index 0

# 조건 1번 실행
python scripts/test_condition_search.py --index 1
```

---

### 연속 테스트 (여러 조건)

```bash
# Windows PowerShell
for ($i=0; $i -lt 3; $i++) {
    python scripts/test_condition_search.py --index $i
    Start-Sleep -Seconds 2
}

# Git Bash / Linux
for i in {0..2}; do
    python scripts/test_condition_search.py --index $i
    sleep 2
done
```

---

## 📚 참고 문서

- **구현 가이드**: `docs/CONDITION_SEARCH_GUIDE.md`
- **WebSocket 테스트**: `docs/WEBSOCKET_TEST_GUIDE.md`
- **공식 샘플**: `docs/조건검색_요청_일반_샘플코드.md`

---

## 🎯 체크리스트

테스트 전 확인:

- [ ] 가상환경 활성화됨
- [ ] websockets 설치됨
- [ ] .env 파일에 실제 키 입력됨
- [ ] Base URL이 `https://api.kiwoom.com`
- [ ] 토큰 발급 테스트 성공
- [ ] WebSocket 로그인 성공
- [ ] 키움 HTS에서 조건검색 등록됨

---

## 🚀 준비되었으면 실행!

```bash
python scripts/test_condition_search.py
```

---

**성공을 기원합니다!** 🎉
