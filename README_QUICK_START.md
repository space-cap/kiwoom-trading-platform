# 🚀 Quick Start Guide

## 완료된 구현 사항

✅ **프로젝트 구조** - Clean Architecture 기반
✅ **FastAPI 메인 애플리케이션** - CORS, 미들웨어, 예외 처리
✅ **키움 REST API 클라이언트** - Rate limiting, 에러 핸들링
✅ **인증 모듈** - OAuth 2.0 토큰 관리
✅ **조건검색 모듈** - 검색 실행, 신규 편입 감지
✅ **알림 시스템** - Console, Slack, Email 지원
✅ **스케줄러** - 실시간 모니터링
✅ **데이터베이스** - SQLite/PostgreSQL 지원

## 실행 방법

### 1. 데이터베이스 초기화 (완료)

```bash
python scripts/init_db.py
```

### 2. API 서버 실행

```bash
# 방법 1: 직접 실행
python app/main.py

# 방법 2: uvicorn 사용 (권장)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API 문서 확인

브라우저에서 열기:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. API 테스트

터미널을 새로 열고:

```bash
python test_api.py
```

## 주요 API 엔드포인트

### 인증 (Authentication)

#### 토큰 발급
```bash
curl -X POST http://localhost:8000/api/v1/auth/token
```

#### 토큰 상태 확인
```bash
curl http://localhost:8000/api/v1/auth/token/status
```

#### 토큰 갱신
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh
```

### 조건검색 (Condition Search)

#### 조건 목록 동기화
```bash
curl -X POST http://localhost:8000/api/v1/conditions/sync
```

#### 조건 목록 조회
```bash
curl http://localhost:8000/api/v1/conditions/
```

#### 조건 검색 실행
```bash
curl -X POST http://localhost:8000/api/v1/conditions/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USER_ID",
    "seq": "CONDITION_SEQ"
  }'
```

## 스케줄러 실행 (실시간 모니터링)

별도 터미널에서:

```bash
python scripts/start_scheduler.py
```

스케줄러는:
- 30초마다 모든 활성 조건을 검색
- 신규 편입 종목 발견 시 알림 발송
- 매일 오전 8시에 토큰 자동 갱신

## 설정

`.env` 파일에서 설정 변경:

```env
# 필수 설정
KIWOOM_APP_KEY=your_app_key
KIWOOM_APP_SECRET=your_app_secret

# 스케줄러 설정
SCHEDULER_ENABLED=True
CONDITION_CHECK_INTERVAL=30  # 초

# 로그 설정
LOG_LEVEL=INFO
DEBUG=False

# Slack 알림 (선택)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

## 개발 모드

개발 시 편리한 기능:

1. **자동 리로드**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **디버그 모드** (`.env`에서)
   ```env
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

3. **API 문서** - http://localhost:8000/docs

## Docker 실행

```bash
# 빌드
docker-compose build

# 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

## 문제 해결

### 포트가 이미 사용 중
```bash
# 포트 변경
uvicorn app.main:app --reload --port 8080
```

### 데이터베이스 초기화 필요
```bash
# 데이터베이스 파일 삭제 후 재생성
rm data/kiwoom.db
python scripts/init_db.py
```

### 패키지 누락
```bash
uv pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings httpx python-dotenv apscheduler pytz alembic
```

## 다음 단계

1. **실제 API 키로 테스트**
   - `.env` 파일에 실제 키움 API 키 입력
   - `python test_api.py` 실행하여 토큰 발급 테스트

2. **조건검색 설정**
   - HTS에서 조건검색 등록
   - `/api/v1/conditions/sync` 호출하여 동기화
   - 조건 검색 실행 테스트

3. **스케줄러 실행**
   - `python scripts/start_scheduler.py`
   - 로그에서 실시간 모니터링 확인

4. **알림 설정**
   - Slack webhook URL 설정
   - 신규 종목 편입 시 알림 수신

## 지원

문제가 발생하면:
1. `logs/app.log` 파일 확인
2. 디버그 모드 활성화 (`DEBUG=True`)
3. API 문서에서 요청/응답 형식 확인
