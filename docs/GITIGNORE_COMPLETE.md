# .gitignore 완전 가이드

**작성일**: 2025-11-08  
**최종 업데이트**: 2025-11-08

---

## 📋 추가된 항목 요약

### 1. UV 관련
```gitignore
uv.lock
```
- UV 패키지 관리자의 lock 파일
- 프로젝트마다 다를 수 있으므로 무시
- 필요 시 `!uv.lock`로 예외 처리 가능

---

### 2. 환경별 설정 파일
```gitignore
.env.dev
.env.prod
!.env.dev.example
!.env.prod.example
```

**이유**:
- `.env.dev`, `.env.prod`는 실제 키를 포함하므로 무시
- `.env.dev.example`, `.env.prod.example`은 템플릿이므로 커밋 허용

**권장 구조**:
```
.env              # 실제 키 (무시됨)
.env.example      # 템플릿 (커밋됨) ✓
.env.dev          # 개발 실제 키 (무시됨)
.env.dev.example  # 개발 템플릿 (커밋됨) ✓
.env.prod         # 운영 실제 키 (무시됨)
.env.prod.example # 운영 템플릿 (커밋됨) ✓
```

---

### 3. Docker 관련
```gitignore
docker-compose.override.yml
.dockerignore
```

**docker-compose.override.yml**:
- 로컬 개발 시 개인별 설정 오버라이드
- 예: 포트 변경, 볼륨 마운트 경로

**예시**:
```yaml
# docker-compose.override.yml (무시됨)
version: '3.8'
services:
  app:
    ports:
      - "8001:8000"  # 개인별 포트 변경
```

---

### 4. 런타임 파일
```gitignore
*.pid
*.seed
*.pid.lock
```
- 프로세스 ID 파일
- 시드 파일
- Lock 파일

---

### 5. IDE 상세 설정
```gitignore
# VSCode
.vscode/*
!.vscode/settings.json.example
!.vscode/launch.json.example
!.vscode/extensions.json.example

# PyCharm
.idea/*
!.idea/codeStyles/
!.idea/inspectionProfiles/
```

**권장 프로젝트 설정 공유**:
```
.vscode/
├── settings.json.example     # 예제 (커밋됨) ✓
├── launch.json.example        # 디버그 설정 예제 (커밋됨) ✓
└── settings.json              # 실제 (무시됨)
```

---

### 6. 프로파일링
```gitignore
*.prof
*.lprof
```
- Python 프로파일러 출력
- 성능 분석 결과

---

### 7. 배포 파일
```gitignore
*.tar.gz
*.whl
*.zip
```
- 빌드된 패키지
- 압축 파일

---

### 8. 추가 인증서 형식
```gitignore
*.cer
*.der
*.p7b
*.p7c
*.pfx
```
- 다양한 인증서 형식
- 보안을 위해 모두 무시

---

### 9. 캐시 디렉토리
```gitignore
.cache/
cache/
.history/
```
- API 응답 캐시
- 로컬 히스토리

---

### 10. Node.js (선택적)
```gitignore
node_modules/
npm-debug.log
yarn-error.log
```
- 프론트엔드 도구 사용 시
- 문서 빌드 도구 사용 시

---

## 🔍 현재 무시되는 파일 확인

### 방법 1: git status
```bash
git status --ignored
```

### 방법 2: 특정 파일 확인
```bash
git check-ignore -v .env
git check-ignore -v uv.lock
git check-ignore -v data/kiwoom.db
```

**출력 예시**:
```
.gitignore:50:.env    .env
.gitignore:96:uv.lock uv.lock
.gitignore:60:data/   data/kiwoom.db
```

---

## 🎯 프로젝트별 무시 현황

### ✅ 정상적으로 무시됨
```
!! .env                          # 실제 API 키
!! .venv/                        # 가상환경
!! app/__pycache__/              # Python 바이트코드
!! data/                         # 데이터베이스 파일
!! logs/                         # 로그 파일
!! uv.lock                       # UV lock 파일
!! .python-version               # pyenv 버전 파일
```

### ⚠️ 추적되지 않음 (커밋 대기)
```
?? .env.example                  # 커밋 필요 ✓
?? .gitignore                    # 커밋 필요 ✓
?? pyproject.toml                # 커밋 필요 ✓
?? app/                          # 커밋 필요 ✓
?? docs/                         # 커밋 필요 ✓
```

### ❌ 환경 파일 처리 필요
```
?? .env.dev                      # 삭제 또는 .gitignore 업데이트 후 재확인
?? .env.prod                     # 삭제 또는 .gitignore 업데이트 후 재확인
```

---

## 📝 .dockerignore 파일

Docker 이미지 빌드 시 제외할 파일 목록을 생성했습니다.

**위치**: `.dockerignore`

**주요 제외 항목**:
- 개발 환경 파일 (.venv, .env)
- 로그 및 데이터베이스 파일
- 테스트 및 문서 파일
- Git 히스토리

**효과**:
- Docker 이미지 크기 감소
- 빌드 속도 향상
- 민감한 정보 제외

---

## 🔐 보안 체크리스트

### 절대 커밋되면 안 되는 파일

#### High Priority ⚠️⚠️⚠️
- [ ] `.env` (실제 API 키)
- [ ] `data/.token` (OAuth 토큰)
- [ ] `*.key`, `*.pem` (인증서 키)
- [ ] `secrets/` (시크릿 디렉토리)

#### Medium Priority ⚠️⚠️
- [ ] `data/*.db` (실제 거래 데이터)
- [ ] `logs/*.log` (민감한 로그)
- [ ] `.env.dev`, `.env.prod` (환경별 실제 키)

#### Low Priority ⚠️
- [ ] `__pycache__/` (바이트코드)
- [ ] `.venv/` (가상환경)
- [ ] `uv.lock` (lock 파일)

---

## 🧹 정리 명령어

### 이미 추적 중인 파일 제거
```bash
# 단일 파일
git rm --cached .env

# 디렉토리
git rm -r --cached __pycache__/

# 모든 무시 파일 제거
git rm -r --cached .
git add .
git commit -m "Apply .gitignore"
```

### .gitignore 적용 확인
```bash
# 변경 사항 확인
git status

# 무시되는 파일 확인
git status --ignored

# 캐시 정리 후 재확인
git rm -r --cached .
git add .
```

---

## 📊 .gitignore 구조

### 카테고리별 분류
1. **Python 관련** (30줄)
2. **가상환경** (5줄)
3. **IDE** (10줄)
4. **환경 파일** (10줄)
5. **로그** (5줄)
6. **데이터베이스** (10줄)
7. **보안** (10줄)
8. **테스트** (15줄)
9. **빌드** (10줄)
10. **OS** (10줄)
11. **기타** (50줄)

**총 라인**: ~200줄

---

## 💡 베스트 프랙티스

### 1. 환경 파일 관리
```
✓ DO:
- .env.example 커밋 (템플릿)
- .env 무시 (실제 키)
- README에 설정 방법 문서화

✗ DON'T:
- .env를 커밋
- 실제 키를 README에 작성
- 예제 파일에 실제 키 포함
```

### 2. 데이터 파일
```
✓ DO:
- data/ 디렉토리 전체 무시
- 샘플 데이터는 별도 디렉토리 (sample_data/)
- CSV/Excel은 기본적으로 무시

✗ DON'T:
- 실거래 데이터 커밋
- 개인정보 포함 파일 커밋
```

### 3. 로그 파일
```
✓ DO:
- logs/ 디렉토리 무시
- *.log 패턴 무시
- 로그 로테이션 설정

✗ DON'T:
- 로그를 git에 포함
- 민감한 정보 로깅
```

---

## 🔄 업데이트 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2025-11-08 | 1.0 | 초기 생성 (67줄) |
| 2025-11-08 | 2.0 | 대폭 확장 (179줄) |
| 2025-11-08 | 2.1 | UV, Docker, 환경별 파일 추가 (~200줄) |

---

## 🎓 참고 자료

### 공식 템플릿
- GitHub Python .gitignore: https://github.com/github/gitignore/blob/main/Python.gitignore
- GitIgnore.io: https://www.toptal.com/developers/gitignore

### 프로젝트 특화
- FastAPI 프로젝트
- SQLAlchemy 프로젝트
- UV 패키지 관리자

---

**요약**: .gitignore가 완벽하게 설정되었습니다! 보안, 성능, 협업을 모두 고려한 설정입니다. 🎉
