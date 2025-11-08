# API 명세서

**프로젝트**: 키움 REST API 조건검색 트레이딩 플랫폼  
**API 버전**: v1  
**Base URL**: `http://localhost:8000/api/v1`  
**문서 버전**: 1.0  
**작성일**: 2025-11-08

---

## 목차

1. [개요](#개요)
2. [인증](#인증)
3. [공통 사항](#공통-사항)
4. [에러 코드](#에러-코드)
5. [API 엔드포인트](#api-엔드포인트)
   - [시스템](#시스템)
   - [인증](#인증-api)
   - [조건검색](#조건검색-api)

---

## 개요

### 특징
- RESTful API 설계
- JSON 요청/응답
- 비동기 처리
- Rate limiting 적용
- 자동 API 문서 (Swagger, ReDoc)

### 지원 형식
- **Content-Type**: `application/json`
- **Accept**: `application/json`

---

## 인증

### OAuth 2.0
키움증권 REST API는 OAuth 2.0 Client Credentials 방식을 사용합니다.

#### 인증 흐름
1. `/api/v1/auth/token` 엔드포인트로 토큰 발급
2. 이후 모든 요청에 Bearer 토큰 사용 (내부적으로 처리)
3. 토큰 만료 시 자동 갱신

#### 토큰 유효 기간
- **기본**: 24시간
- **자동 갱신**: 만료 5분 전

---

## 공통 사항

### 응답 형식

#### 성공 응답
```json
{
  "data": {
    // 응답 데이터
  }
}
```

#### 에러 응답
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

### HTTP 상태 코드
- `200 OK`: 성공
- `201 Created`: 생성 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 실패
- `404 Not Found`: 리소스 없음
- `429 Too Many Requests`: Rate limit 초과
- `500 Internal Server Error`: 서버 오류

### Rate Limiting
- **초당**: 최대 20건
- **분당**: 최대 1,000건
- **최소 간격**: 50ms

#### Rate Limit 헤더
```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 19
X-RateLimit-Reset: 1699999999
```

---

## 에러 코드

| 코드 | 설명 |
|------|------|
| `UNKNOWN_ERROR` | 알 수 없는 오류 |
| `API_ERROR` | API 오류 |
| `AUTH_ERROR` | 인증 오류 |
| `RATE_LIMIT_ERROR` | Rate limit 초과 |
| `INVALID_REQUEST` | 잘못된 요청 |
| `NOT_FOUND` | 리소스 없음 |
| `INTERNAL_ERROR` | 내부 서버 오류 |

---

## API 엔드포인트

---

## 시스템

### Root

#### `GET /`

애플리케이션 정보를 반환합니다.

**요청**
```bash
curl http://localhost:8000/
```

**응답**
```json
{
  "name": "Kiwoom Trading Platform",
  "version": "0.1.0",
  "status": "running",
  "environment": "development"
}
```

---

### Health Check

#### `GET /health`

시스템 상태를 확인합니다.

**요청**
```bash
curl http://localhost:8000/health
```

**응답**
```json
{
  "status": "healthy"
}
```

---

## 인증 API

### 토큰 발급

#### `POST /api/v1/auth/token`

키움 API용 OAuth 액세스 토큰을 발급받습니다.

**요청**
```bash
curl -X POST http://localhost:8000/api/v1/auth/token
```

**응답**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "expires_at": "2025-11-09T22:47:56.000Z"
}
```

**응답 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `access_token` | string | 액세스 토큰 |
| `token_type` | string | 토큰 타입 (Bearer) |
| `expires_in` | integer | 만료까지 남은 시간 (초) |
| `expires_at` | string | 만료 시간 (ISO 8601) |

**에러**

| 상태 코드 | 에러 코드 | 설명 |
|-----------|-----------|------|
| 401 | AUTH_ERROR | 인증 실패 (잘못된 API 키) |
| 500 | API_ERROR | 키움 API 오류 |

---

### 토큰 상태 확인

#### `GET /api/v1/auth/token/status`

현재 토큰의 유효성과 만료 정보를 확인합니다.

**요청**
```bash
curl http://localhost:8000/api/v1/auth/token/status
```

**응답 (유효한 토큰)**
```json
{
  "is_valid": true,
  "expires_at": "2025-11-09T22:47:56.000Z",
  "remaining_seconds": 86400
}
```

**응답 (만료된 토큰)**
```json
{
  "is_valid": false,
  "expires_at": null,
  "remaining_seconds": null
}
```

**응답 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `is_valid` | boolean | 토큰 유효 여부 |
| `expires_at` | string\|null | 만료 시간 (ISO 8601) |
| `remaining_seconds` | integer\|null | 남은 시간 (초) |

---

### 토큰 갱신

#### `POST /api/v1/auth/token/refresh`

만료된 토큰을 갱신하여 새 토큰을 발급받습니다.

**요청**
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh
```

**응답**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "expires_at": "2025-11-09T22:47:56.000Z"
}
```

**에러**

| 상태 코드 | 에러 코드 | 설명 |
|-----------|-----------|------|
| 401 | AUTH_ERROR | 갱신 실패 |

---

## 조건검색 API

### 조건 목록 조회

#### `GET /api/v1/conditions/`

데이터베이스에 저장된 조건검색 목록을 조회합니다.

**요청**
```bash
# 전체 조건
curl http://localhost:8000/api/v1/conditions/

# 활성 조건만
curl http://localhost:8000/api/v1/conditions/?active_only=true
```

**Query Parameters**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `active_only` | boolean | X | false | 활성 조건만 조회 |

**응답**
```json
[
  {
    "id": 1,
    "seq": "001",
    "name": "급등주",
    "description": null,
    "is_active": true,
    "created_at": "2025-11-08T22:00:00.000Z",
    "updated_at": "2025-11-08T22:00:00.000Z"
  },
  {
    "id": 2,
    "seq": "002",
    "name": "거래량 급증",
    "description": null,
    "is_active": true,
    "created_at": "2025-11-08T22:00:00.000Z",
    "updated_at": "2025-11-08T22:00:00.000Z"
  }
]
```

**응답 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | integer | 조건 ID |
| `seq` | string | 조건 시퀀스 번호 |
| `name` | string | 조건명 |
| `description` | string\|null | 조건 설명 |
| `is_active` | boolean | 활성 여부 |
| `created_at` | string | 생성 시간 |
| `updated_at` | string | 수정 시간 |

---

### 조건 동기화

#### `POST /api/v1/conditions/sync`

키움 HTS에 등록된 조건검색을 가져와 데이터베이스와 동기화합니다.

**요청**
```bash
curl -X POST http://localhost:8000/api/v1/conditions/sync
```

**응답**
```json
[
  {
    "id": 1,
    "seq": "001",
    "name": "급등주",
    "description": null,
    "is_active": true,
    "created_at": "2025-11-08T22:00:00.000Z",
    "updated_at": "2025-11-08T22:00:00.000Z"
  }
]
```

**처리 과정**
1. 키움 API에서 조건 목록 조회
2. 기존 조건과 비교
3. 신규 조건은 생성
4. 기존 조건은 유지
5. 동기화된 목록 반환

**에러**

| 상태 코드 | 에러 코드 | 설명 |
|-----------|-----------|------|
| 401 | AUTH_ERROR | 인증 필요 |
| 500 | API_ERROR | API 호출 실패 |

---

### 조건 검색 실행

#### `POST /api/v1/conditions/search`

특정 조건으로 검색을 실행하고 결과를 저장합니다.

**요청**
```bash
curl -X POST http://localhost:8000/api/v1/conditions/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER123",
    "seq": "001"
  }'
```

**요청 Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `user_id` | string | O | 사용자 ID |
| `seq` | string | O | 조건 시퀀스 번호 |

**응답**
```json
{
  "condition_seq": "001",
  "condition_name": "급등주",
  "total_count": 15,
  "new_entry_count": 3,
  "results": [
    {
      "id": 1,
      "condition_id": 1,
      "stock_code": "005930",
      "stock_name": "삼성전자",
      "current_price": 75000,
      "change_rate": 2.5,
      "volume": 12345678,
      "is_new_entry": true,
      "searched_at": "2025-11-08T22:00:00.000Z"
    },
    {
      "id": 2,
      "condition_id": 1,
      "stock_code": "000660",
      "stock_name": "SK하이닉스",
      "current_price": 125000,
      "change_rate": 3.2,
      "volume": 8765432,
      "is_new_entry": false,
      "searched_at": "2025-11-08T22:00:00.000Z"
    }
  ],
  "searched_at": "2025-11-08T22:00:00.000Z"
}
```

**응답 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `condition_seq` | string | 조건 시퀀스 번호 |
| `condition_name` | string | 조건명 |
| `total_count` | integer | 전체 결과 수 |
| `new_entry_count` | integer | 신규 편입 종목 수 |
| `results` | array | 검색 결과 목록 |
| `searched_at` | string | 검색 시간 |

**결과 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | integer | 결과 ID |
| `condition_id` | integer | 조건 ID |
| `stock_code` | string | 종목코드 (6자리) |
| `stock_name` | string | 종목명 |
| `current_price` | integer\|null | 현재가 |
| `change_rate` | float\|null | 등락률 (%) |
| `volume` | integer\|null | 거래량 |
| `is_new_entry` | boolean | 신규 편입 여부 |
| `searched_at` | string | 검색 시간 |

**처리 과정**
1. 조건 검증 (없으면 생성)
2. 이전 결과 조회 (최근 1시간)
3. 키움 API로 검색 실행
4. 결과 파싱 및 신규 편입 판단
5. 데이터베이스에 저장
6. 모니터링 히스토리 저장
7. 결과 반환

**에러**

| 상태 코드 | 에러 코드 | 설명 |
|-----------|-----------|------|
| 400 | INVALID_REQUEST | 잘못된 요청 (필수 필드 누락) |
| 401 | AUTH_ERROR | 인증 필요 |
| 500 | API_ERROR | 검색 실패 |

---

## 사용 예제

### 1. 전체 워크플로우

```bash
# 1. 토큰 발급
curl -X POST http://localhost:8000/api/v1/auth/token

# 2. 조건 동기화
curl -X POST http://localhost:8000/api/v1/conditions/sync

# 3. 조건 목록 확인
curl http://localhost:8000/api/v1/conditions/

# 4. 조건 검색 실행
curl -X POST http://localhost:8000/api/v1/conditions/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER123",
    "seq": "001"
  }'
```

### 2. Python 예제

```python
import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient() as client:
        # 토큰 발급
        token_response = await client.post(f"{BASE_URL}/auth/token")
        print(f"Token: {token_response.json()['access_token'][:20]}...")
        
        # 조건 동기화
        sync_response = await client.post(f"{BASE_URL}/conditions/sync")
        conditions = sync_response.json()
        print(f"Synced {len(conditions)} conditions")
        
        # 첫 번째 조건으로 검색
        if conditions:
            search_response = await client.post(
                f"{BASE_URL}/conditions/search",
                json={
                    "user_id": "USER123",
                    "seq": conditions[0]["seq"]
                }
            )
            result = search_response.json()
            print(f"Found {result['total_count']} stocks")
            print(f"New entries: {result['new_entry_count']}")

asyncio.run(main())
```

### 3. JavaScript 예제

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

async function main() {
    // 토큰 발급
    const tokenResponse = await fetch(`${BASE_URL}/auth/token`, {
        method: "POST"
    });
    const tokenData = await tokenResponse.json();
    console.log(`Token: ${tokenData.access_token.substring(0, 20)}...`);
    
    // 조건 동기화
    const syncResponse = await fetch(`${BASE_URL}/conditions/sync`, {
        method: "POST"
    });
    const conditions = await syncResponse.json();
    console.log(`Synced ${conditions.length} conditions`);
    
    // 첫 번째 조건으로 검색
    if (conditions.length > 0) {
        const searchResponse = await fetch(`${BASE_URL}/conditions/search`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "USER123",
                seq: conditions[0].seq
            })
        });
        const result = await searchResponse.json();
        console.log(`Found ${result.total_count} stocks`);
        console.log(`New entries: ${result.new_entry_count}`);
    }
}

main();
```

---

## API 문서 자동 생성

### Swagger UI
Interactive API 문서를 제공합니다.

**URL**: http://localhost:8000/docs

**특징**:
- 모든 엔드포인트 목록
- 요청/응답 스키마
- Try it out 기능
- 인증 테스트

### ReDoc
읽기 쉬운 API 문서를 제공합니다.

**URL**: http://localhost:8000/redoc

**특징**:
- 깔끔한 UI
- 스크롤 가능한 사이드바
- 코드 예제
- 다운로드 가능한 OpenAPI 스펙

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-11-08 | 초기 버전 작성 |

---

**문서 버전**: 1.0  
**최종 수정일**: 2025-11-08  
**관리자**: Development Team
