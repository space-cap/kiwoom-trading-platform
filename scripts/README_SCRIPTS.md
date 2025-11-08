# Scripts 사용 가이드

**작성일**: 2025-11-08

---

## 📁 스크립트 목록

### 1. init_db.py
**기능**: 데이터베이스 초기화

**사용법**:
```bash
python scripts/init_db.py
```

**설명**:
- SQLAlchemy 모델 기반으로 테이블 생성
- 기존 테이블이 있어도 안전
- 로그에 생성된 테이블 목록 출력

---

### 2. start_scheduler.py
**기능**: 스케줄러 독립 실행

**사용법**:
```bash
python scripts/start_scheduler.py
```

**설명**:
- API 서버와 별도로 스케줄러 실행
- 실시간 조건검색 모니터링
- Ctrl+C로 안전하게 종료

**스케줄**:
- 조건 검색: 30초마다
- 토큰 갱신: 매일 08:00

---

### 3. test_token.py ⭐ NEW
**기능**: 토큰 발급 및 관리 테스트

**사용법**:

#### 대화형 모드 (기본)
```bash
python scripts/test_token.py
```

메뉴:
```
1. 토큰 발급 (새로 발급)
2. 토큰 정보 조회
3. 파일에서 토큰 로드
4. 토큰 유효성 확인
5. API 호출 테스트
6. 토큰 삭제
7. 전체 테스트 실행
0. 종료
```

#### 빠른 테스트
```bash
python scripts/test_token.py --mode quick
```

현재 토큰 확인 → 새 토큰 발급 → 결과 출력

#### 전체 테스트
```bash
python scripts/test_token.py --mode all
```

모든 테스트를 순차적으로 실행:
1. 토큰 발급
2. 파일 로드
3. 유효성 확인
4. API 호출

---

## 🎯 test_token.py 상세

### 실행 모드

#### 1. Interactive Mode (기본)
```bash
python scripts/test_token.py
# 또는
python scripts/test_token.py --mode interactive
```

**특징**:
- 메뉴 기반 인터페이스
- 원하는 테스트만 선택 실행
- 반복 테스트 가능

**사용 예**:
```
선택하세요:
  1. 토큰 발급 (새로 발급)
  2. 토큰 정보 조회
  ...

입력: 1

============================================================
  1. 토큰 발급 테스트
============================================================

🔑 API 설정 확인:
  App Key: PSKRmVaM5w...Ae0zk
  App Secret: ********************
  Base URL: https://openapi.koreainvestment.com:9443

🚀 토큰 발급 요청 중...
✅ 토큰 발급 성공!

📋 토큰 상태:
  ✓ 토큰 존재: True
  ✓ 유효성: True
  ✓ 만료 시간: 2025-11-09T22:47:56
  ✓ 남은 시간: 86400초
  ✓ 토큰 미리보기: eyJhbGciOiJIUzI1NiI...
```

#### 2. Quick Mode
```bash
python scripts/test_token.py --mode quick
```

**특징**:
- 가장 빠른 테스트
- 토큰 발급만 수행
- CI/CD에 적합

**출력**:
```
============================================================
  ⚡ 빠른 토큰 발급 테스트
============================================================

1️⃣ 현재 토큰 확인...
📋 토큰 상태:
  ✓ 토큰 존재: False
  ✓ 유효성: False

2️⃣ 토큰 발급 시도...
✅ 토큰 발급 성공!

3️⃣ 최종 상태:
📋 토큰 상태:
  ✓ 토큰 존재: True
  ✓ 유효성: True
  ...
```

#### 3. All Mode
```bash
python scripts/test_token.py --mode all
```

**특징**:
- 전체 테스트 스위트 실행
- 자동화된 검증
- 결과 요약 제공

**출력**:
```
============================================================
  🧪 전체 테스트 실행
============================================================

1. 토큰 발급 테스트
...
✅ 토큰 발급 성공!

2. 파일에서 토큰 로드 테스트
...
✅ 파일에서 토큰 로드 성공!

...

============================================================
  📊 테스트 결과 요약
============================================================

  토큰 발급: ✅ 성공
  파일 로드: ✅ 성공
  유효성 확인: ✅ 성공
  API 호출: ✅ 성공

총 4개 중 4개 성공
```

---

## 🧪 테스트 시나리오

### 시나리오 1: 최초 토큰 발급
```bash
# 1. 토큰 파일 확인 (없어야 함)
ls data/.token

# 2. 빠른 테스트
python scripts/test_token.py --mode quick

# 3. 파일 생성 확인
cat data/.token
```

### 시나리오 2: 서버 재시작 시뮬레이션
```bash
# 1. 토큰 발급
python scripts/test_token.py --mode quick

# 2. 메모리에서 토큰 제거 (서버 재시작 시뮬레이션)
# → 대화형 모드에서 "3. 파일에서 토큰 로드" 선택

# 3. 파일에서 자동 로드 확인
```

### 시나리오 3: 만료된 토큰 처리
```bash
# 1. 토큰 파일 수동 수정 (만료 시간을 과거로)
# data/.token 파일의 expires_at을 과거 날짜로 변경

# 2. 토큰 로드 시도
python scripts/test_token.py --mode interactive
# → "3. 파일에서 토큰 로드" 선택

# 3. 자동 삭제 확인
```

### 시나리오 4: API 호출 테스트
```bash
# 1. 전체 테스트
python scripts/test_token.py --mode all

# 2. 실제 API 응답 확인
# → 조건검색 목록 조회 결과 출력
```

---

## 🔍 출력 설명

### 토큰 정보
```
📋 토큰 상태:
  ✓ 토큰 존재: True         # 토큰이 메모리/파일에 있는지
  ✓ 유효성: True             # 만료되지 않았는지
  ✓ 만료 시간: 2025-11-09... # ISO 8601 형식
  ✓ 남은 시간: 86400초       # 초 단위
  ✓ 토큰 미리보기: eyJ...    # 처음 20자 + ...
```

### 파일 내용
```
📄 파일 내용:
  Access Token: eyJhbGciOiJIUzI1NiIsInR5c...  # 처음 30자
  Expires At: 2025-11-09T22:47:56.123456      # 만료 시간
  Created At: 2025-11-08T22:47:56.123456      # 생성 시간
```

### API 응답
```
📦 응답 데이터:
{
  "rt_cd": "0",           # 응답 코드 (0=성공)
  "msg_cd": "...",        # 메시지 코드
  "msg1": "...",          # 메시지
  "output": [...]         # 실제 데이터
}
```

---

## ⚠️ 주의사항

### 1. API 키 필요
`.env` 파일에 다음 설정 필요:
```env
KIWOOM_APP_KEY=your_app_key
KIWOOM_APP_SECRET=your_app_secret
```

### 2. 네트워크 필요
- 키움 API 서버 접속 필요
- VPN 사용 시 제한 가능성

### 3. Rate Limit
- 초당 20건 제한
- 연속 테스트 시 주의

### 4. 로그 파일
- `logs/app.log`에 상세 로그 기록
- 오류 발생 시 확인

---

## 🐛 문제 해결

### "No module named 'app'"
```bash
# 프로젝트 루트에서 실행
cd C:\workdir\space-cap\kiwoom-trading-platform
python scripts/test_token.py
```

### "KIWOOM_APP_KEY is required"
```bash
# .env 파일 확인
cat .env

# 없으면 생성
cp .env.example .env
# 실제 API 키 입력
```

### "Authentication failed"
- API 키가 올바른지 확인
- 키움 계좌가 활성화되어 있는지 확인
- 실계좌 전용 (모의투자 미지원)

### "Token file deleted"
- 정상 동작 (만료된 토큰 자동 삭제)
- 새로 발급하면 됨

---

## 💡 팁

### 1. 빠른 확인
```bash
# 토큰 파일 존재 여부만 확인
ls data/.token

# 토큰 만료 시간만 확인
cat data/.token | grep expires_at
```

### 2. 로그 실시간 확인
```bash
# 다른 터미널에서
tail -f logs/app.log
```

### 3. 토큰 수동 삭제
```bash
rm data/.token
```

### 4. CI/CD 통합
```bash
# Exit code 사용
python scripts/test_token.py --mode quick
if [ $? -eq 0 ]; then
  echo "Token test passed"
else
  echo "Token test failed"
  exit 1
fi
```

---

## 📊 Exit Codes

- `0`: 성공
- `1`: 실패 또는 오류

---

**작성자**: Development Team  
**최종 수정**: 2025-11-08
