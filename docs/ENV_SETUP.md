# 환경 변수 설정 가이드

**작성일**: 2025-11-08

---

## ⚠️ 중요: 실제 API 키 입력 필요

`.env` 파일에 **실제 키움증권 API 키**를 입력해야 합니다.

---

## 🔍 현재 문제

### `.env` 파일 확인
```bash
cat .env | grep KIWOOM_APP_KEY
```

**잘못된 예**:
```env
KIWOOM_APP_KEY=*******************************************
KIWOOM_APP_SECRET=*******************************************
```

이것은 **예제/마스킹된 값**입니다. 실제 동작하지 않습니다!

---

## ✅ 올바른 설정 방법

### 1. 키움증권 개발자센터에서 API 키 발급

1. **키움증권 개발자센터** 접속
   - URL: https://apiportal.koreainvestment.com/ (또는 해당 포털)
   
2. **앱 등록/조회**
   - 로그인 후 "앱 관리" 메뉴
   - "앱 등록" 또는 기존 앱 조회
   
3. **App Key와 App Secret 복사**
   - App Key: 약 36~50자 길이의 영숫자 문자열
   - App Secret: 약 36~50자 길이의 영숫자 문자열

### 예시 (실제 키 형식)
```
App Key: YOUR_ACTUAL_APP_KEY_HERE_36_TO_50_CHARS
App Secret: YOUR_ACTUAL_APP_SECRET_HERE_36_TO_100_CHARS
```
예: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` 형태

---

### 2. `.env` 파일 수정

`.env` 파일을 열어서 **실제 키 값**으로 교체:

```env
# Kiwoom API
KIWOOM_APP_KEY=여기에_실제_App_Key_입력
KIWOOM_APP_SECRET=여기에_실제_App_Secret_입력
KIWOOM_BASE_URL=https://openapi.koreainvestment.com:9443
KIWOOM_WEBSOCKET_URL=ws://ops.koreainvestment.com:21000
```

**올바른 예**:
```env
KIWOOM_APP_KEY=YOUR_ACTUAL_APP_KEY_FROM_KIWOOM
KIWOOM_APP_SECRET=YOUR_ACTUAL_APP_SECRET_FROM_KIWOOM
```

⚠️ **주의**: 
- `*` 문자가 아닌 **실제 영숫자 문자열**
- 따옴표 없이 그대로 입력
- 앞뒤 공백 제거

---

### 3. 설정 확인

`.env` 파일 수정 후 확인:

```bash
# 방법 1: 파일 직접 확인
cat .env | grep KIWOOM_APP_KEY

# 방법 2: Python으로 확인
python -c "from app.core.config import get_settings; s = get_settings(); print(f'Key length: {len(s.KIWOOM_APP_KEY)}'); print(f'First 10 chars: {s.KIWOOM_APP_KEY[:10]}')"
```

**정상인 경우**:
```
Key length: 36
First 10 chars: (실제키의처음10자)
```

**비정상인 경우**:
```
Key length: 43
First 10 chars: **********
```

---

## 🧪 테스트

설정 완료 후 토큰 테스트:

```bash
python scripts/test_token.py --mode quick
```

**성공 시**:
```
[SUCCESS] 토큰 발급 성공!

[TOKEN INFO] 토큰 상태:
  - 토큰 존재: True
  - 유효성: True
  - 만료 시간: 2025-11-09T23:18:07
  - 남은 시간: 86400초
```

**실패 시**:
```
[ERROR] 토큰 발급 실패: Token acquisition failed: HTTP 403
error_code: EGW00103
error_description: "유효하지 않은 AppKey입니다."
```

---

## 🔐 보안 주의사항

### ✅ 해야 할 것
- `.env` 파일에 실제 키 입력
- `.env`는 `.gitignore`에 포함됨 (커밋 안됨)
- 로컬 환경에만 보관

### ❌ 하지 말아야 할 것
- `.env` 파일을 git에 커밋
- 공개 저장소에 API 키 노출
- 스크린샷이나 공유 시 키 노출

---

## 🔄 환경별 설정

### 개발 환경
```bash
# .env 파일 사용
KIWOOM_APP_KEY=개발용_키
KIWOOM_APP_SECRET=개발용_시크릿
```

### 운영 환경
```bash
# 환경 변수로 직접 설정
export KIWOOM_APP_KEY="운영용_키"
export KIWOOM_APP_SECRET="운영용_시크릿"
```

---

## 📝 전체 .env 파일 예시

```env
# Application
APP_NAME=Kiwoom Trading Platform
APP_VERSION=0.1.0
DEBUG=True
ENVIRONMENT=development

# Kiwoom API (⚠️ 실제 키 입력 필요!)
KIWOOM_APP_KEY=YOUR_ACTUAL_APP_KEY_FROM_KIWOOM_PORTAL
KIWOOM_APP_SECRET=YOUR_ACTUAL_APP_SECRET_FROM_KIWOOM_PORTAL
KIWOOM_BASE_URL=https://openapi.koreainvestment.com:9443
KIWOOM_WEBSOCKET_URL=ws://ops.koreainvestment.com:21000

# Database
DATABASE_URL=sqlite:///./data/kiwoom.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5

# Scheduler
SCHEDULER_ENABLED=True
CONDITION_CHECK_INTERVAL=30

# Slack Notification (Optional)
SLACK_WEBHOOK_URL=

# Email Notification (Optional)
EMAIL_ENABLED=False
EMAIL_SMTP_HOST=
EMAIL_SMTP_PORT=
EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_FROM=
EMAIL_TO=
```

---

## 🐛 문제 해결

### Q: "유효하지 않은 AppKey입니다" 에러

**원인**:
1. API 키가 `*` 문자로 마스킹되어 있음
2. 잘못된 키 입력
3. 복사 시 공백 포함

**해결**:
```bash
# 1. .env 파일 확인
cat .env | grep KIWOOM_APP_KEY

# 2. 실제 키인지 확인 (첫 10자)
python -c "from app.core.config import get_settings; s = get_settings(); print(s.KIWOOM_APP_KEY[:10])"

# 3. * 가 나오면 실제 키로 교체 필요
```

---

### Q: 키를 입력했는데도 작동 안 함

**체크리스트**:
- [ ] `.env` 파일이 프로젝트 루트에 있는가?
- [ ] 파일명이 정확히 `.env`인가? (`.env.txt` 아님)
- [ ] API 키에 따옴표가 없는가?
- [ ] 앞뒤 공백이 없는가?
- [ ] 키 전체가 복사되었는가? (잘림 없음)

---

### Q: 키움증권 API 키 발급 방법

1. **실계좌 개설 필요**
   - 키움증권 계좌가 있어야 함
   - 모의투자는 REST API 미지원

2. **개발자센터 접속**
   - 키움증권 개발자 포털
   - 로그인 (계좌 정보 사용)

3. **앱 등록**
   - 앱 이름 입력
   - 리다이렉트 URL (선택)
   - 앱 생성 후 키 발급

4. **키 복사**
   - App Key 복사
   - App Secret 복사
   - 안전하게 보관

---

## 💡 팁

### 키 유효성 빠른 확인
```bash
# 키 길이와 첫 10자 확인
python -c "
from app.core.config import get_settings
s = get_settings()
key = s.KIWOOM_APP_KEY
print(f'길이: {len(key)}')
print(f'첫 10자: {key[:10]}')
print(f'별표 포함: {\"*\" in key}')
if '*' in key:
    print('⚠️  경고: 실제 키가 아닙니다!')
else:
    print('✅ 실제 키로 보입니다.')
"
```

### 환경 변수로 직접 설정 (임시)
```bash
# Windows PowerShell
$env:KIWOOM_APP_KEY="실제_키"
$env:KIWOOM_APP_SECRET="실제_시크릿"
python scripts/test_token.py --mode quick

# Linux/Mac
export KIWOOM_APP_KEY="실제_키"
export KIWOOM_APP_SECRET="실제_시크릿"
python scripts/test_token.py --mode quick
```

---

**다음 단계**: 키 입력 후 `python scripts/test_token.py --mode quick` 실행! 🚀
