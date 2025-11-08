# .gitignore 개선 사항

**날짜**: 2025-11-08  
**변경 사항**: 67줄 → 179줄 (112줄 추가)

---

## 추가된 주요 카테고리

### 1. Python 관련 추가 항목
```gitignore
*.pyo              # Python 최적화 바이트코드
*.pyd              # Python 동적 모듈 (Windows)
*.manifest         # 매니페스트 파일
*.spec             # PyInstaller spec 파일
pip-wheel-metadata/
share/python-wheels/
```

**이유**: Python 빌드 및 패키징 과정에서 생성되는 추가 파일들

---

### 2. 가상환경 추가
```gitignore
.virtualenv/       # virtualenv의 다른 이름
```

**이유**: 다양한 가상환경 도구 지원

---

### 3. IDE/편집기 확장
```gitignore
.project           # Eclipse
.pydevproject      # PyDev
.settings/         # Eclipse settings
*.sublime-project  # Sublime Text
*.sublime-workspace
```

**이유**: 더 많은 IDE 지원

---

### 4. 환경 파일 예외
```gitignore
!.env.example      # .env.example은 커밋 허용
```

**이유**: 예제 파일은 저장소에 포함되어야 함

---

### 5. 로그 파일 확장
```gitignore
*.log.*            # 로테이션된 로그 파일
```

**이유**: 로그 로테이션 시 생성되는 파일들 (app.log.1, app.log.2 등)

---

### 6. 데이터베이스 추가 파일
```gitignore
*.db-journal       # SQLite 저널 파일
*.db-shm          # SQLite 공유 메모리
*.db-wal          # SQLite Write-Ahead Log
```

**이유**: SQLite가 생성하는 추가 파일들

---

### 7. OS 관련 확장
```gitignore
Desktop.ini        # Windows 폴더 설정
*.bak             # 백업 파일
*.swp             # Vim 스왑 파일
*.tmp             # 임시 파일
```

**이유**: 다양한 OS와 에디터의 임시 파일

---

### 8. 테스트 도구 확장
```gitignore
.nox/             # Nox 테스트 환경
coverage.xml      # Coverage XML 보고서
*.cover           # Coverage 파일
.hypothesis/      # Hypothesis 테스트
.mypy_cache/      # MyPy 캐시
.dmypy.json
dmypy.json
```

**이유**: 다양한 테스트 및 타입 체킹 도구

---

### 9. 패키지 관리자 확장
```gitignore
uv.lock           # UV 락 파일
Pipfile.lock      # Pipenv 락 파일
```

**이유**: UV와 Pipenv 지원

---

### 10. 문서 빌드 파일 (NEW)
```gitignore
docs/_build/      # Sphinx 빌드 출력
docs/.doctrees/   # Sphinx doctrees
site/             # MkDocs 빌드 출력
```

**이유**: 문서 생성 도구들의 빌드 출력

---

### 11. Jupyter Notebook (NEW)
```gitignore
.ipynb_checkpoints
*.ipynb
```

**이유**: 데이터 분석 시 Jupyter 사용 가능성

---

### 12. Python 도구들 (NEW)
```gitignore
# pyenv
.python-version

# Celery (비동기 작업 큐)
celerybeat-schedule
celerybeat.pid

# Spyder (IDE)
.spyderproject
.spyproject

# Rope (리팩토링 도구)
.ropeproject

# Pyre (타입 체커)
.pyre/

# pytype (타입 분석)
.pytype/

# Cython
cython_debug/
```

**이유**: 향후 사용 가능한 다양한 Python 도구들

---

### 13. 백업 파일 (NEW)
```gitignore
*~
*.bak
*.backup
*.old
```

**이유**: 에디터와 도구들이 생성하는 백업 파일

---

### 14. 임시 파일 (NEW)
```gitignore
*.tmp
*.temp
.cache/
```

**이유**: 다양한 임시 파일들

---

### 15. 로컬 설정 (NEW)
```gitignore
local_settings.py  # Django 스타일 로컬 설정
.local/
```

**이유**: 개발자별 로컬 설정 파일

---

### 16. 보안 강화 (NEW) ⚠️ 중요
```gitignore
# Secrets and credentials
secrets/
credentials/
*.key             # 개인키
*.pem             # PEM 인증서
*.cert            # 인증서
*.crt             # 인증서
*.p12             # PKCS#12 인증서
```

**이유**: 민감한 인증 정보 보호

---

### 17. 데이터 파일 (NEW) ⚠️ 민감
```gitignore
*.csv             # CSV 데이터
*.xlsx            # Excel 파일
*.xls             # 구형 Excel
*.json.local      # 로컬 JSON 설정
```

**이유**: 실거래 데이터나 민감한 정보가 포함될 수 있는 파일들

---

### 18. Mac 특화 (NEW)
```gitignore
.AppleDouble
.LSOverride
Icon
._*
```

**이유**: macOS 메타데이터 파일들

---

### 19. Windows 특화 (NEW)
```gitignore
ehthumbs.db       # Windows 썸네일 캐시
ehthumbs_vista.db
```

**이유**: Windows 시스템 파일

---

### 20. 테스트 출력 (NEW)
```gitignore
test-results/
test-output/
```

**이유**: 테스트 프레임워크의 출력 디렉토리

---

## 특별 주의 항목 ⚠️

### 보안 관련 (절대 커밋 금지)
```gitignore
secrets/
credentials/
*.key
*.pem
*.cert
*.crt
*.p12
```

### 민감한 데이터 파일
```gitignore
*.csv              # 실거래 데이터 포함 가능
*.xlsx             # 종목 정보, 계좌 정보 등
data/              # 데이터베이스 파일
logs/              # 로그에 민감한 정보 포함 가능
```

### 환경 설정
```gitignore
.env               # API 키, 시크릿 포함
.env.local
.env.*.local
```

---

## 허용된 예외 파일

```gitignore
!.env.example      # 이 파일만 커밋 허용
```

`.env.example`은 실제 값이 없는 템플릿이므로 저장소에 포함됩니다.

---

## 프로젝트별 추가 고려사항

### 현재 프로젝트에서 생성될 수 있는 파일들

1. **데이터베이스**
   - `data/kiwoom.db` ✅ 이미 무시됨
   - `data/test.db` ✅ 이미 무시됨

2. **로그**
   - `logs/app.log` ✅ 이미 무시됨
   - `logs/app.log.1` ✅ 새로 추가됨

3. **테스트 출력**
   - `.pytest_cache/` ✅ 이미 무시됨
   - `htmlcov/` ✅ 이미 무시됨

4. **환경 파일**
   - `.env` ✅ 이미 무시됨
   - `.env.dev` ⚠️ 무시됨 (.env.*.local 패턴)
   - `.env.prod` ⚠️ 무시됨

---

## 확인 사항

현재 `.env.dev`와 `.env.prod` 파일이 untracked 상태입니다:

```bash
$ git status --porcelain
?? .env.dev
?? .env.prod
```

### 권장 사항:

**옵션 1**: 완전히 무시 (현재 설정) ✅ 권장
- `.env.dev`, `.env.prod`에 실제 API 키 저장
- 저장소에 커밋하지 않음
- 팀원들은 각자 로컬에서 생성

**옵션 2**: 템플릿만 커밋
- `.env.dev.example`, `.env.prod.example` 생성
- 실제 값 없이 구조만 포함
- `.gitignore`에서 예외 처리

```gitignore
# 추가할 경우
!.env.dev.example
!.env.prod.example
```

---

## 검증 명령어

### 무시된 파일 확인
```bash
git status --ignored
```

### 특정 파일이 무시되는지 확인
```bash
git check-ignore -v .env
git check-ignore -v logs/app.log
git check-ignore -v data/kiwoom.db
```

### 이미 추적 중인 파일 제거
```bash
# 캐시에서만 제거 (파일은 유지)
git rm --cached <file>

# 전체 디렉토리
git rm -r --cached <directory>
```

---

## 요약

### 변경 사항
- **이전**: 67줄, 7개 카테고리
- **이후**: 179줄, 20개 카테고리
- **추가**: 112줄

### 주요 개선점
1. ✅ 더 많은 Python 도구 지원
2. ✅ 보안 강화 (인증서, 키 파일)
3. ✅ 민감한 데이터 파일 보호
4. ✅ 다양한 IDE/OS 지원
5. ✅ 테스트 및 문서 도구 지원

### 보안 등급
- **높음**: secrets/, credentials/, *.key, *.pem
- **중간**: .env, *.csv, *.xlsx, data/
- **낮음**: logs/, __pycache__/

---

**작성자**: Development Team  
**최종 수정**: 2025-11-08
