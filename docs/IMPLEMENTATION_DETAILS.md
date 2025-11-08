# 구현 상세 문서

**프로젝트**: 키움 REST API 조건검색 트레이딩 플랫폼  
**작성일**: 2025-11-08  
**버전**: 1.0

---

## 목차

1. [아키텍처 개요](#아키텍처-개요)
2. [레이어별 상세](#레이어별-상세)
3. [핵심 컴포넌트](#핵심-컴포넌트)
4. [데이터 흐름](#데이터-흐름)
5. [보안 및 인증](#보안-및-인증)
6. [에러 처리](#에러-처리)
7. [성능 최적화](#성능-최적화)
8. [확장 가능성](#확장-가능성)

---

## 아키텍처 개요

### Clean Architecture

본 프로젝트는 Clean Architecture 원칙을 따릅니다:

```
┌─────────────────────────────────────┐
│     Presentation Layer              │
│  (FastAPI, Routes, Schemas)         │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│     Application Layer               │
│  (Services, Use Cases)              │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│     Domain Layer                    │
│  (Models, Business Logic)           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│     Infrastructure Layer            │
│  (Repository, External APIs, DB)    │
└─────────────────────────────────────┘
```

### 의존성 방향

- **외부 → 내부**: 외부 레이어가 내부 레이어에 의존
- **내부 ↛ 외부**: 내부 레이어는 외부를 모름
- **인터페이스 기반**: 추상화를 통한 결합도 최소화

---

## 레이어별 상세

### 1. Presentation Layer (API)

#### 책임
- HTTP 요청 수신 및 검증
- 응답 포맷팅
- 인증 및 권한 검증
- API 문서 생성

#### 주요 컴포넌트

**FastAPI Application** (`app/main.py`)
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: DB 초기화
    init_db()
    yield
    # Shutdown: 정리 작업

app = FastAPI(lifespan=lifespan)
```

**Router** (`app/api/v1/router.py`)
```python
api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(condition_router)
```

**Endpoints** (`app/modules/*/api.py`)
```python
@router.post("/search")
async def execute_condition_search(
    request: ConditionSearchRequest,
    service: ConditionService = Depends(get_service)
):
    return await service.execute_condition_search(...)
```

#### Pydantic Schemas
- **요청 검증**: BaseModel 상속
- **응답 직렬화**: `model_validate()`
- **타입 안전성**: 타입 힌팅

```python
class ConditionSearchRequest(BaseModel):
    user_id: str
    seq: str
    
    @validator('seq')
    def validate_seq(cls, v):
        if not v:
            raise ValueError('seq is required')
        return v
```

---

### 2. Application Layer (Services)

#### 책임
- 비즈니스 로직 구현
- Use Case 조율
- 트랜잭션 관리
- 도메인 모델 조작

#### Service 패턴

**AuthService** (`app/modules/auth/service.py`)
```python
class AuthService:
    def __init__(self):
        self.client = KiwoomRestClient()
    
    async def get_token(self) -> TokenResponse:
        # 1. API 클라이언트로 토큰 발급
        async with self.client:
            token = await self.client.get_access_token()
        
        # 2. 응답 포맷팅
        return TokenResponse(
            access_token=token,
            expires_in=86400,
            ...
        )
```

**ConditionService** (`app/modules/condition/service.py`)
```python
class ConditionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ConditionRepository(db)
        self.client = KiwoomRestClient()
    
    async def execute_condition_search(
        self, user_id: str, seq: str
    ) -> ConditionSearchResponse:
        # 1. 조건 조회/생성
        condition = self.repository.get_condition_by_seq(seq)
        
        # 2. 이전 결과 조회
        previous = self.repository.get_previous_results(...)
        
        # 3. API 호출
        response = await self.client.search_by_condition(...)
        
        # 4. 신규 편입 감지
        new_entries = self._detect_new_entries(...)
        
        # 5. 결과 저장
        results = self.repository.save_search_results(...)
        
        # 6. 히스토리 저장
        self.repository.save_monitoring_history(...)
        
        return ConditionSearchResponse(...)
```

#### 트랜잭션 관리

```python
def get_service(db: Session = Depends(get_db)):
    """Service with DB session"""
    try:
        service = ConditionService(db)
        yield service
    finally:
        db.close()
```

---

### 3. Domain Layer (Models)

#### 책임
- 비즈니스 엔티티 정의
- 도메인 로직 포함
- 불변성 유지

#### SQLAlchemy Models

**Condition Model** (`app/modules/condition/models.py`)
```python
class Condition(Base):
    __tablename__ = "conditions"
    
    id = Column(Integer, primary_key=True)
    seq = Column(String(50), unique=True, index=True)
    name = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    results = relationship("SearchResult", back_populates="condition")
    
    def __repr__(self):
        return f"<Condition(seq={self.seq}, name={self.name})>"
```

**Relationships**
```python
# One-to-Many
class Condition(Base):
    results = relationship("SearchResult", back_populates="condition")

class SearchResult(Base):
    condition_id = Column(Integer, ForeignKey("conditions.id"))
    condition = relationship("Condition", back_populates="results")
```

---

### 4. Infrastructure Layer

#### 책임
- 외부 시스템 연동
- 데이터 영속성
- 기술적 세부사항

#### Repository 패턴

**ConditionRepository** (`app/modules/condition/repository.py`)
```python
class ConditionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_condition_by_seq(self, seq: str) -> Optional[Condition]:
        return self.db.query(Condition)\
            .filter(Condition.seq == seq)\
            .first()
    
    def save_search_results(
        self, condition_id: int, results: List[dict], previous: set
    ) -> List[SearchResult]:
        saved = []
        for data in results:
            is_new = data['stock_code'] not in previous
            result = SearchResult(
                condition_id=condition_id,
                is_new_entry=is_new,
                **data
            )
            self.db.add(result)
            saved.append(result)
        
        self.db.commit()
        return saved
```

#### API Client

**Base Client** (`app/client/base.py`)
```python
class BaseAPIClient:
    async def _wait_for_rate_limit(self):
        """Rate limiting with lock"""
        async with self._rate_limit_lock:
            elapsed = time.time() - self._last_request_time
            if elapsed < MIN_REQUEST_INTERVAL:
                await asyncio.sleep(MIN_REQUEST_INTERVAL - elapsed)
            self._last_request_time = time.time()
    
    async def _request(self, method, endpoint, **kwargs):
        await self._wait_for_rate_limit()
        
        try:
            response = await self._client.request(...)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitException()
            raise APIException(...)
```

**Kiwoom Client** (`app/client/rest_client.py`)
```python
class KiwoomRestClient(BaseAPIClient):
    def _get_auth_headers(self, tr_id: str) -> Dict:
        token = token_manager.get_token()
        if not token:
            raise AuthenticationException()
        
        return {
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
        }
    
    async def ensure_authenticated(self):
        """Ensure valid token before API call"""
        if not token_manager.is_token_valid():
            await self.get_access_token()
```

---

## 핵심 컴포넌트

### 1. Token Manager

**역할**: OAuth 토큰 관리

**구현** (`app/core/security.py`)
```python
class TokenManager:
    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
    def set_token(self, access_token: str, expires_in: int):
        """Store token with expiration"""
        self._access_token = access_token
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)
    
    def get_token(self) -> Optional[str]:
        """Get token if still valid (5min buffer)"""
        if self._token_expires_at:
            if datetime.now() < self._token_expires_at - timedelta(minutes=5):
                return self._access_token
        return None
    
    def is_token_valid(self) -> bool:
        """Check if token is valid"""
        return self.get_token() is not None

# Global singleton
token_manager = TokenManager()
```

**사용**:
```python
# Set token
token_manager.set_token(token, 86400)

# Get token
token = token_manager.get_token()

# Check validity
if token_manager.is_token_valid():
    # Use token
```

---

### 2. Scheduler

**역할**: 주기적 작업 실행

**구조**:
```
scheduler/
├── config.py      # Scheduler 생성 및 설정
├── tasks.py       # 작업 정의 (실제 로직)
└── jobs.py        # 작업 스케줄링 (등록, 시작, 중지)
```

**Config** (`app/scheduler/config.py`)
```python
def create_scheduler() -> AsyncIOScheduler:
    return AsyncIOScheduler(
        timezone="Asia/Seoul",
        job_defaults={
            'coalesce': True,  # 여러 pending을 하나로
            'max_instances': 1,  # 동시 실행 방지
            'misfire_grace_time': 30,  # 30초 grace time
        }
    )
```

**Tasks** (`app/scheduler/tasks.py`)
```python
async def check_conditions_task():
    """주기적 조건 체크"""
    # 1. 장 운영 시간 체크
    if not is_market_open():
        logger.info("Market closed")
        return
    
    # 2. DB 세션 생성
    db = SessionLocal()
    
    try:
        # 3. 활성 조건 조회
        service = ConditionService(db)
        conditions = service.get_all_conditions(active_only=True)
        
        # 4. 각 조건 검색
        for condition in conditions:
            result = await service.execute_condition_search(...)
            
            # 5. 신규 편입 알림
            if result.new_entry_count > 0:
                await notification_service.send_new_entry_alert(...)
    
    finally:
        db.close()
```

**Jobs** (`app/scheduler/jobs.py`)
```python
def register_jobs(scheduler: AsyncIOScheduler):
    # Job 1: 조건 체크 (30초마다)
    scheduler.add_job(
        check_conditions_task,
        trigger=IntervalTrigger(seconds=30),
        id="check_conditions",
        replace_existing=True,
    )
    
    # Job 2: 토큰 갱신 (매일 08:00)
    scheduler.add_job(
        token_refresh_task,
        trigger=CronTrigger(hour=8, minute=0),
        id="refresh_token",
        replace_existing=True,
    )

def start_scheduler(scheduler: AsyncIOScheduler):
    register_jobs(scheduler)
    scheduler.start()
```

---

### 3. Notification Service

**역할**: 다중 채널 알림 발송

**구현** (`app/modules/notifications/service.py`)
```python
class NotificationService:
    def __init__(self):
        self.enabled_channels = self._get_enabled_channels()
    
    def _get_enabled_channels(self) -> List[str]:
        """설정에 따라 활성 채널 결정"""
        channels = [NOTIFICATION_CONSOLE]
        if settings.SLACK_WEBHOOK_URL:
            channels.append(NOTIFICATION_SLACK)
        if settings.EMAIL_ENABLED:
            channels.append(NOTIFICATION_EMAIL)
        return channels
    
    async def send_new_entry_alert(
        self, condition_name, stock_code, stock_name, ...
    ):
        """신규 편입 알림"""
        message = self._format_new_entry_message(...)
        await self._send_notification(message, level="info")
    
    async def _send_notification(self, message: str, level: str):
        """모든 활성 채널로 발송"""
        for channel in self.enabled_channels:
            if channel == NOTIFICATION_CONSOLE:
                await self._send_console(message, level)
            elif channel == NOTIFICATION_SLACK:
                await self._send_slack(message)
            elif channel == NOTIFICATION_EMAIL:
                await self._send_email(message, level)
```

---

## 데이터 흐름

### 조건 검색 실행 플로우

```
[Client]
   ↓ POST /api/v1/conditions/search
[API Router]
   ↓ validate request
[ConditionService]
   ↓ get_condition_by_seq()
[Repository]
   ↓ SELECT FROM conditions
[Database]
   ↓ return Condition
[Repository]
   ↓ return to Service
[ConditionService]
   ↓ get_previous_results()
[Repository]
   ↓ SELECT FROM search_results
[Database]
   ↓ return results
[ConditionService]
   ↓ search_by_condition()
[KiwoomRestClient]
   ↓ _wait_for_rate_limit()
[BaseAPIClient]
   ↓ async sleep if needed
[KiwoomRestClient]
   ↓ GET with auth headers
[Kiwoom API]
   ↓ return search results
[ConditionService]
   ↓ detect new entries
   ↓ save_search_results()
[Repository]
   ↓ INSERT INTO search_results
[Database]
   ↓ commit
[ConditionService]
   ↓ save_monitoring_history()
[Repository]
   ↓ INSERT INTO monitoring_history
[Database]
   ↓ commit
[ConditionService]
   ↓ return ConditionSearchResponse
[API Router]
   ↓ serialize response
[Client]
   ↓ receive JSON
```

---

## 보안 및 인증

### OAuth 2.0 Client Credentials

**흐름**:
1. App Key + App Secret → Token 발급
2. Token을 TokenManager에 저장
3. 모든 API 호출 시 자동으로 Bearer 토큰 추가
4. 만료 5분 전 자동 갱신

**구현**:
```python
# 1. Token 발급
async def get_access_token(self):
    response = await self.post(
        "/oauth2/tokenP",
        json={
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
        }
    )
    token_manager.set_token(response['access_token'], response['expires_in'])

# 2. 인증 확인
async def ensure_authenticated(self):
    if not token_manager.is_token_valid():
        await self.get_access_token()

# 3. 헤더 추가
def _get_auth_headers(self, tr_id):
    token = token_manager.get_token()
    return {
        "authorization": f"Bearer {token}",
        "appkey": self.app_key,
        ...
    }
```

### 환경 변수 보안

**민감 정보**:
- `KIWOOM_APP_KEY`
- `KIWOOM_APP_SECRET`
- `SLACK_WEBHOOK_URL`
- `EMAIL_PASSWORD`

**보호 방법**:
1. `.env` 파일 사용
2. `.gitignore`에 등록
3. Pydantic validator로 검증
4. 로그에서 제외

```python
@field_validator('KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET')
@classmethod
def validate_sensitive_fields(cls, v):
    if not v:
        raise ValueError('Required field is missing')
    return v
```

---

## 에러 처리

### 계층별 예외 처리

```
┌─────────────────────────────────────┐
│  API Layer                          │
│  - FastAPI HTTPException            │
│  - 상태 코드 + 메시지               │
└─────────────────────────────────────┘
           ↑ try/except
┌─────────────────────────────────────┐
│  Service Layer                      │
│  - KiwoomException                  │
│  - 비즈니스 로직 예외               │
└─────────────────────────────────────┘
           ↑ try/except
┌─────────────────────────────────────┐
│  Infrastructure Layer               │
│  - APIException                     │
│  - 외부 시스템 예외                 │
└─────────────────────────────────────┘
```

### 전역 예외 핸들러

```python
# app/main.py
app.add_exception_handler(KiwoomException, kiwoom_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# app/shared/exceptions/handlers.py
async def kiwoom_exception_handler(request, exc):
    logger.error(f"KiwoomException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code if isinstance(exc, APIException) else 500,
        content={"error": {"code": exc.code, "message": exc.message}}
    )
```

### Retry 로직

```python
@retry_on_failure(max_retries=3, delay=1.0)
async def api_call():
    # 실패 시 자동 재시도 (1초, 2초, 3초 간격)
    return await client.get(...)
```

---

## 성능 최적화

### 1. 비동기 처리

**httpx AsyncClient**:
```python
async with httpx.AsyncClient() as client:
    response = await client.get(...)
```

**asyncio 동시 처리**:
```python
# 여러 조건 동시 검색
tasks = [
    service.execute_condition_search(cond.seq)
    for cond in conditions
]
results = await asyncio.gather(*tasks)
```

### 2. Rate Limiting

**구현**:
```python
class BaseAPIClient:
    async def _wait_for_rate_limit(self):
        async with self._rate_limit_lock:
            elapsed = time.time() - self._last_request_time
            if elapsed < MIN_REQUEST_INTERVAL:
                await asyncio.sleep(MIN_REQUEST_INTERVAL - elapsed)
            self._last_request_time = time.time()
```

**효과**:
- API 제한 준수 (초당 20건)
- 429 에러 방지
- 안정적인 요청 처리

### 3. 데이터베이스 인덱스

**Indexes**:
```python
# 검색에 자주 사용되는 필드
__table_args__ = (
    Index('idx_stock_code', 'stock_code'),
    Index('idx_searched_at', 'searched_at'),
)
```

**효과**:
- 빠른 종목 조회
- 시간 범위 검색 최적화

### 4. 연결 풀링

**SQLAlchemy Engine**:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
```

---

## 확장 가능성

### 1. 모듈 추가

**새 모듈 생성**:
```bash
mkdir app/modules/order
touch app/modules/order/{__init__,api,service,repository,models,schemas}.py
```

**Router 등록**:
```python
# app/api/v1/router.py
from app.modules.order.api import router as order_router
api_router.include_router(order_router)
```

### 2. 데이터베이스 변경

**PostgreSQL로 전환**:
```python
# .env
DATABASE_URL=postgresql://user:pass@localhost/kiwoom

# 자동으로 PostgreSQL 사용
```

### 3. 알림 채널 추가

**새 Provider 생성**:
```python
# app/modules/notifications/providers/telegram.py
class TelegramNotificationProvider:
    async def send(self, message: str):
        # Telegram API 호출
```

**Service에 등록**:
```python
# app/modules/notifications/service.py
if settings.TELEGRAM_BOT_TOKEN:
    channels.append(NOTIFICATION_TELEGRAM)
```

### 4. WebSocket 추가

**실시간 시세**:
```python
# app/client/websocket_client.py
class KiwoomWebSocketClient:
    async def connect(self):
        async with websockets.connect(url) as ws:
            await ws.send(subscribe_message)
            async for message in ws:
                yield parse(message)
```

---

**문서 버전**: 1.0  
**최종 수정일**: 2025-11-08  
**작성자**: Development Team
