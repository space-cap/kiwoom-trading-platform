# 🚀 Kiwoom Trading Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-FF6B6B?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**키움증권 REST API 기반 조건검색 자동화 트레이딩 플랫폼**

[Features](#-주요-기능) • [Demo](#-데모) • [Installation](#-설치) • [Usage](#-사용법) • [Architecture](#-아키텍처)

</div>

---

## 📋 목차

- [개요](#-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [아키텍처](#-아키텍처)
- [설치](#-설치)
- [사용법](#-사용법)
- [데모](#-데모)
- [API 문서](#-api-문서)
- [프로젝트 구조](#-프로젝트-구조)
- [개발 진행 상황](#-개발-진행-상황)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 개요

**Kiwoom Trading Platform**은 키움증권의 REST API와 WebSocket API를 활용하여 조건검색 기반 자동 매매를 구현한 Python 트레이딩 플랫폼입니다.

### 💡 프로젝트 배경

- 기존 키움 OpenAPI+는 Windows ActiveX에 의존적이며 크로스 플랫폼 지원이 불가능
- REST API를 통해 **클라우드 배포**가 가능한 현대적인 트레이딩 시스템 구축
- **실시간 조건검색**을 통한 체계적인 종목 발굴 및 자동화된 매매 시스템 필요

### 🎨 핵심 가치

✅ **크로스 플랫폼** - Windows 환경에 종속되지 않는 Python 기반 시스템  
✅ **실시간 모니터링** - WebSocket을 통한 조건검색 실시간 알림  
✅ **확장 가능** - FastAPI 기반의 모듈식 아키텍처  
✅ **완전한 문서화** - 16+ 개의 상세 가이드 문서  

---

## ✨ 주요 기능

### 🔐 OAuth 2.0 인증 시스템
- Access Token 자동 발급 및 갱신
- 토큰 파일 저장으로 서버 재시작 시에도 재사용
- 만료 5분 전 자동 갱신 로직
- Thread-safe 구현

### 📊 조건검색 시스템
- **조건검색 목록 조회** (CNSRLST) - HTS에 등록된 조건 자동 로드
- **조건검색 실행** (CNSRREQ) - 조건에 부합하는 종목 실시간 검색
- **실시간 알림** (CNSSRALM) - 조건 진입/이탈 종목 실시간 알림 *(예정)*
- 다중 조건 동시 검색 지원

### 🌐 WebSocket 실시간 통신
- 자동 연결 및 로그인
- 메시지 핸들러 시스템
- PING-PONG 자동 응답
- 비동기 메시지 처리

### 🗄️ 데이터 관리
- SQLAlchemy ORM 기반 데이터베이스
- Alembic 마이그레이션
- 조건검색 결과 자동 저장
- 히스토리 관리 및 통계

### ⏰ 스케줄러
- APScheduler 기반 주기적 작업 실행
- 시장 시간 체크
- 자동 토큰 갱신
- 로그 정리 *(예정)*

### 🔔 알림 시스템
- 신규 종목 진입 알림
- 조건 이탈 알림
- Slack/Discord 웹훅 *(예정)*
- 이메일 알림 *(예정)*

---

## 🛠 기술 스택

### Backend Framework
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)

### Communication
![HTTPX](https://img.shields.io/badge/HTTPX-0.25+-blue?style=flat-square)
![WebSockets](https://img.shields.io/badge/WebSockets-12.0+-FF6B6B?style=flat-square)

### Task Scheduling
![APScheduler](https://img.shields.io/badge/APScheduler-3.10+-green?style=flat-square)

### Database
![SQLite](https://img.shields.io/badge/SQLite-Development-003B57?style=flat-square&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-4169E1?style=flat-square&logo=postgresql&logoColor=white)

### DevOps
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migration-orange?style=flat-square)

### Package Management
![UV](https://img.shields.io/badge/UV-Package%20Manager-blueviolet?style=flat-square)

---

## 🏗 아키텍처

### 레이어 구조

```
┌─────────────────────────────────────────────────────┐
│              Application Layer                      │
│        (FastAPI Server, CLI Tools)                  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│               Service Layer                         │
│   (Business Logic, Condition Search Service)       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│          Client Layer (API Communication)           │
│      REST Client  |  WebSocket Client               │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│           Repository Layer (Data Access)            │
│              (SQLAlchemy ORM)                       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│      External APIs & Database                       │
│  Kiwoom REST/WebSocket API  |  SQLite/PostgreSQL   │
└─────────────────────────────────────────────────────┘
```

### 주요 컴포넌트

| 컴포넌트 | 책임 | 파일 |
|---------|------|-----|
| **AuthManager** | OAuth 인증 및 토큰 관리 | `app/core/security.py` |
| **RestClient** | REST API 통신 | `app/client/rest_client.py` |
| **WebSocketClient** | WebSocket 실시간 통신 | `app/client/websocket_client.py` |
| **ConditionService** | 조건검색 비즈니스 로직 | `app/modules/condition/` |
| **DatabaseRepository** | 데이터 저장/조회 | `app/modules/*/repository.py` |
| **Scheduler** | 주기적 작업 실행 | `app/scheduler/` |

---

## 📦 설치

### 사전 요구사항

- Python 3.10 이상
- 키움증권 REST API 계정 (App Key, App Secret)
- HTS에 조건검색 등록 필요

### 1. 저장소 클론

```bash
git clone https://github.com/space-cap/kiwoom-trading-platform.git
cd kiwoom-trading-platform
```

### 2. 패키지 매니저 설치 (UV)

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

자세한 설치 방법은 [INSTALL_UV.md](INSTALL_UV.md) 참조

### 3. 의존성 설치

```bash
# UV 사용
uv sync

# 또는 pip 사용
pip install -e .
```

### 4. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_APP_SECRET=your_app_secret_here
```

### 5. 데이터베이스 초기화

```bash
uv run python scripts/init_db.py
```

---

## 🚀 사용법

### 토큰 발급 테스트

```bash
# 대화형 모드 (기본)
uv run python scripts/test_token.py

# 빠른 토큰 발급
uv run python scripts/test_token.py --mode quick

# 전체 테스트
uv run python scripts/test_token.py --mode all
```

### 조건검색 목록 조회

```bash
# WebSocket 연결 및 조건검색 목록 조회
uv run python scripts/test_websocket.py
```

### 조건검색 실행

```bash
# 첫 번째 조건 자동 실행
uv run python scripts/test_condition_search.py

# 특정 조건 실행 (인덱스 지정)
uv run python scripts/test_condition_search.py --index 0
```

### FastAPI 서버 실행

```bash
# 개발 모드
uv run uvicorn app.main:app --reload --port 8000

# 프로덕션 모드
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

서버 실행 후 http://localhost:8000/docs 에서 API 문서 확인

### 스케줄러 실행 *(예정)*

```bash
uv run python scripts/start_scheduler.py
```

---

## 🎬 데모

### 1. 토큰 발급

```bash
$ uv run python scripts/test_token.py --mode quick

============================================================
  키움증권 REST API 토큰 테스트
============================================================

[STEP 1] 토큰 발급 요청...
[SUCCESS] 토큰 발급 성공!

[토큰 정보]
  - Token: **************************
  - Type: Bearer
  - Expires: 2025-11-09 23:54:45
```

### 2. 조건검색 목록 조회

```bash
$ uv run python scripts/test_websocket.py

============================================================
  조건검색 목록 조회 테스트
============================================================

[STEP 1] WebSocket 연결...
[SUCCESS] WebSocket 연결 성공

[STEP 2] 조건검색 목록 조회...
[SUCCESS] 3개의 조건검색 발견

[조건검색 목록]
  1. [0] 상승추세
  2. [1] 거래량급증
  3. [2] 신고가돌파
```

### 3. 조건검색 실행

```bash
$ uv run python scripts/test_condition_search.py

============================================================
  조건검색 실행: [0] 상승추세
============================================================

[검색 결과]: 15개 종목

[종목 목록] (최대 10개)
  1. [005930] 삼성전자 - 현재가: 75,000
  2. [000660] SK하이닉스 - 현재가: 142,000
  3. [035420] NAVER - 현재가: 195,000
  ...
```

---

## 📚 API 문서

### REST API 엔드포인트

#### 1. OAuth 토큰 발급

```http
POST https://api.kiwoom.com/oauth2/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "appkey": "YOUR_APP_KEY",
  "secretkey": "YOUR_APP_SECRET"
}
```

**Response:**
```json
{
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다",
  "token": "**************************",
  "token_type": "Bearer",
  "expires_dt": "20251109235445"
}
```

#### 2. WebSocket 조건검색 목록 (CNSRLST)

```json
{
  "trnm": "CNSRLST"
}
```

**Response:**
```json
{
  "trnm": "CNSRLST",
  "return_code": 0,
  "data": [
    ["0", "상승추세"],
    ["1", "거래량급증"]
  ]
}
```

#### 3. WebSocket 조건검색 실행 (CNSRREQ)

```json
{
  "trnm": "CNSRREQ",
  "seq": "0",
  "search_type": "0",
  "stex_tp": "K",
  "cont_yn": "N"
}
```

**Response:**
```json
{
  "trnm": "CNSRREQ",
  "return_code": 0,
  "data": [
    {
      "9001": "A005930",
      "302": "삼성전자",
      "10": "000075000"
    }
  ]
}
```

자세한 API 문서는 [docs/API_SPECIFICATION.md](docs/API_SPECIFICATION.md) 참조

---

## 📂 프로젝트 구조

```
kiwoom-trading-platform/
├── app/                          # 애플리케이션 소스 코드
│   ├── api/                      # FastAPI 라우터
│   │   └── v1/
│   │       ├── endpoints/        # API 엔드포인트
│   │       └── router.py
│   ├── client/                   # API 클라이언트
│   │   ├── base.py              # Base HTTP 클라이언트
│   │   ├── rest_client.py       # REST API 클라이언트 (212줄)
│   │   └── websocket_client.py  # WebSocket 클라이언트 (270줄)
│   ├── core/                     # 핵심 모듈
│   │   ├── config/              # 설정 관리
│   │   ├── database.py          # DB 연결
│   │   ├── logging.py           # 로깅 설정
│   │   ├── security.py          # 토큰 관리 (150줄)
│   │   └── constants.py
│   ├── modules/                  # 비즈니스 로직
│   │   ├── auth/                # 인증 모듈
│   │   ├── condition/           # 조건검색 모듈
│   │   ├── notifications/       # 알림 모듈
│   │   ├── stock/               # 주식 정보
│   │   └── order/               # 주문 (예정)
│   ├── scheduler/                # 스케줄러
│   │   ├── jobs.py
│   │   └── tasks.py
│   ├── shared/                   # 공유 유틸리티
│   │   ├── exceptions/
│   │   ├── middleware/
│   │   └── utils/
│   └── main.py                   # FastAPI 앱 엔트리포인트
├── scripts/                      # 유틸리티 스크립트
│   ├── init_db.py               # DB 초기화
│   ├── test_token.py            # 토큰 테스트 (246줄)
│   ├── test_websocket.py        # WebSocket 테스트 (246줄)
│   └── test_condition_search.py # 조건검색 테스트 (244줄)
├── tests/                        # 단위 테스트 (예정)
├── docs/                         # 문서
│   ├── PRD.md                   # 제품 요구사항
│   ├── API_SPECIFICATION.md     # API 명세
│   ├── PROJECT_PROGRESS.md      # 개발 진행 상황
│   └── ...                      # 16+ 개의 가이드 문서
├── alembic/                      # DB 마이그레이션
├── data/                         # 데이터 디렉토리 (gitignore)
│   └── .token                   # 토큰 저장
├── logs/                         # 로그 디렉토리 (gitignore)
├── .env                          # 환경 변수 (gitignore)
├── .env.example                  # 환경 변수 템플릿
├── pyproject.toml                # 프로젝트 설정
├── uv.lock                       # UV 잠금 파일
├── Dockerfile                    # Docker 설정
├── docker-compose.yml            # Docker Compose
└── README.md                     # 프로젝트 소개
```

---

## 📈 개발 진행 상황

### 전체 진행률: 90%

```
████████████████████░  90%
```

### 완료된 기능 ✅

- [x] 프로젝트 구조 및 설정
- [x] OAuth 2.0 인증 시스템
- [x] 토큰 파일 저장 및 자동 로드
- [x] REST API 클라이언트
- [x] WebSocket 클라이언트
- [x] 조건검색 목록 조회 (CNSRLST)
- [x] 조건검색 실행 (CNSRREQ)
- [x] 테스트 도구 (3개)
- [x] 완전한 문서화 (16+ 개)

### 진행 예정 ⏳

- [ ] 실시간 조건검색 알림 (CNSSRALM)
- [ ] 스케줄러 통합
- [ ] FastAPI 엔드포인트 구현
- [ ] 단위 테스트 (pytest)
- [ ] 자동 매매 시스템
- [ ] 백테스팅 시스템

자세한 내용은 [docs/PROJECT_PROGRESS.md](docs/PROJECT_PROGRESS.md) 참조

---

## 📖 문서

### 핵심 문서

- [PRD.md](docs/PRD.md) - 제품 요구사항 문서
- [API_SPECIFICATION.md](docs/API_SPECIFICATION.md) - API 명세서
- [PROJECT_PROGRESS.md](docs/PROJECT_PROGRESS.md) - 개발 진행 상황
- [IMPLEMENTATION_DETAILS.md](docs/IMPLEMENTATION_DETAILS.md) - 구현 상세

### API 검증 문서

- [API_VERIFICATION.md](docs/API_VERIFICATION.md) - API 검증
- [KIWOOM_API_CORRECTION.md](docs/KIWOOM_API_CORRECTION.md) - API 스펙 수정
- [KIWOOM_TOKEN_RESPONSE.md](docs/KIWOOM_TOKEN_RESPONSE.md) - 토큰 응답 구조

### 구현 가이드

- [WEBSOCKET_CONDITION_LIST.md](docs/WEBSOCKET_CONDITION_LIST.md) - 조건검색 목록 구현
- [CONDITION_SEARCH_GUIDE.md](docs/CONDITION_SEARCH_GUIDE.md) - 조건검색 실행 구현
- [TOKEN_REUSE_PATTERN.md](docs/TOKEN_REUSE_PATTERN.md) - 토큰 재사용 패턴

### 테스트 가이드

- [WEBSOCKET_TEST_GUIDE.md](docs/WEBSOCKET_TEST_GUIDE.md) - WebSocket 테스트
- [CONDITION_SEARCH_TEST_GUIDE.md](docs/CONDITION_SEARCH_TEST_GUIDE.md) - 조건검색 테스트

### 공식 샘플 코드

- [접근토큰발급_샘플_코드.md](docs/접근토큰발급_샘플_코드.md)
- [조건검색_목록조회_샘플코드.md](docs/조건검색_목록조회_샘플코드.md)
- [조건검색_요청_일반_샘플코드.md](docs/조건검색_요청_일반_샘플코드.md)

---

## 🧪 테스트

### 단위 테스트 (예정)

```bash
# 모든 테스트 실행
uv run pytest

# 커버리지 리포트
uv run pytest --cov=app --cov-report=html

# 특정 테스트 실행
uv run pytest tests/test_rest_client.py -v
```

### 통합 테스트 도구

현재 3개의 통합 테스트 스크립트 제공:
- `test_token.py` - OAuth 토큰 발급
- `test_websocket.py` - WebSocket 연결 및 조건검색 목록
- `test_condition_search.py` - 조건검색 실행

---

## 🐳 Docker

### Docker 이미지 빌드

```bash
docker build -t kiwoom-trading-platform .
```

### Docker Compose 실행

```bash
# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

---

## 🔧 개발 환경 설정

### VS Code 확장 추천

- Python
- Pylance
- Python Test Explorer
- Docker
- REST Client

### 코드 포맷팅

```bash
# Black 포맷팅
uv run black app/

# isort import 정리
uv run isort app/

# flake8 린트
uv run flake8 app/
```

---

## 🤝 Contributing

기여를 환영합니다! 다음 단계를 따라주세요:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 커밋 메시지 규칙

- `feat:` - 새로운 기능
- `fix:` - 버그 수정
- `docs:` - 문서 변경
- `refactor:` - 리팩토링
- `test:` - 테스트 추가/수정
- `chore:` - 기타 변경

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [키움증권](https://www.kiwoom.com/) - REST API 제공
- [FastAPI](https://fastapi.tiangolo.com/) - 웹 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [APScheduler](https://apscheduler.readthedocs.io/) - 작업 스케줄링

---

## 📞 Contact

**GitHub Repository**: [https://github.com/space-cap/kiwoom-trading-platform](https://github.com/space-cap/kiwoom-trading-platform)

**Issues**: [https://github.com/space-cap/kiwoom-trading-platform/issues](https://github.com/space-cap/kiwoom-trading-platform/issues)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=space-cap/kiwoom-trading-platform&type=Date)](https://star-history.com/#space-cap/kiwoom-trading-platform&Date)

---

<div align="center">

**Made with ❤️ for the Trading Community**

[⬆ Back to Top](#-kiwoom-trading-platform)

</div>
