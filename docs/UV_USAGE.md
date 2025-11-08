# UV 사용 가이드

**작성일**: 2025-11-08

---

## UV로 스크립트 실행하는 방법

### 방법 1: 직접 실행 (추천) ⭐

가상환경을 먼저 활성화하고 실행:

```bash
# 1. 가상환경 활성화
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. 스크립트 실행
python scripts/test_token.py
python scripts/test_token.py --mode quick
python scripts/init_db.py
python scripts/start_scheduler.py
```

**장점**:
- 빠르고 간단
- 에러 메시지 명확
- 디버깅 쉬움

---

### 방법 2: uv run python (간단)

가상환경 없이 바로 실행:

```bash
uv run python scripts/test_token.py
uv run python scripts/test_token.py --mode quick
```

**동작 원리**:
- uv가 자동으로 .venv를 찾아서 실행
- 가상환경 활성화 없이도 동작

---

### 방법 3: uv run (패키지로 설치 후)

패키지를 editable 모드로 설치 후 실행:

```bash
# 1. 패키지 설치 (최초 1회만)
uv pip install -e .

# 2. 실행
uv run python scripts/test_token.py
```

---

## 각 스크립트 실행 방법

### 1. 토큰 테스트

```bash
# 가상환경 활성화 후
python scripts/test_token.py

# 또는 uv 사용
uv run python scripts/test_token.py

# 빠른 테스트
python scripts/test_token.py --mode quick

# 전체 테스트
python scripts/test_token.py --mode all
```

### 2. 데이터베이스 초기화

```bash
# 가상환경 활성화 후
python scripts/init_db.py

# 또는 uv 사용
uv run python scripts/init_db.py
```

### 3. 스케줄러 실행

```bash
# 가상환경 활성화 후
python scripts/start_scheduler.py

# 또는 uv 사용
uv run python scripts/start_scheduler.py
```

### 4. API 테스트

```bash
# 가상환경 활성화 후
python test_api.py

# 또는 uv 사용
uv run python test_api.py
```

### 5. API 서버 실행

```bash
# 가상환경 활성화 후
uvicorn app.main:app --reload

# 또는 uv 사용
uv run uvicorn app.main:app --reload

# 또는 main.py 직접 실행
python app/main.py
uv run python app/main.py
```

---

## UV 명령어 치트시트

### 패키지 관리

```bash
# 패키지 설치
uv pip install fastapi
uv pip install -r requirements.txt

# 패키지 제거
uv pip uninstall fastapi

# 패키지 목록
uv pip list

# 프로젝트 설치 (editable)
uv pip install -e .

# 개발 의존성 포함
uv pip install -e ".[dev]"
```

### 스크립트 실행

```bash
# Python 스크립트 실행
uv run python script.py

# 모듈 실행
uv run python -m module_name

# PYTHONPATH 설정하여 실행
PYTHONPATH=. uv run python scripts/test.py
```

### 가상환경

```bash
# 가상환경 생성
uv venv

# 가상환경 활성화
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 가상환경 비활성화
deactivate
```

---

## 문제 해결

### Q: "Unable to determine which files to ship" 에러

**원인**: pyproject.toml에 패키지 설정 누락

**해결책 1**: 직접 실행 사용 (추천)
```bash
.venv\Scripts\activate
python scripts/test_token.py
```

**해결책 2**: pyproject.toml 수정
```toml
[tool.hatch.build.targets.wheel]
packages = ["app"]
```

---

### Q: "No module named 'app'" 에러

**원인**: PYTHONPATH가 설정되지 않음

**해결책 1**: 프로젝트 루트에서 실행
```bash
cd C:\workdir\space-cap\kiwoom-trading-platform
python scripts/test_token.py
```

**해결책 2**: PYTHONPATH 설정
```bash
# Windows PowerShell
$env:PYTHONPATH="."
python scripts/test_token.py

# Linux/Mac
PYTHONPATH=. python scripts/test_token.py
```

**해결책 3**: editable 설치
```bash
uv pip install -e .
```

---

### Q: uv run이 느림

**원인**: uv가 매번 환경을 체크

**해결**: 가상환경 활성화 후 직접 실행
```bash
.venv\Scripts\activate
python scripts/test_token.py  # 훨씬 빠름
```

---

## 권장 워크플로우

### 개발 시 (추천) ⭐

```bash
# 1. 가상환경 활성화 (터미널 시작 시 1회)
.venv\Scripts\activate

# 2. 이후 모든 명령은 python 직접 사용
python scripts/test_token.py
python scripts/init_db.py
uvicorn app.main:app --reload
pytest

# 3. 작업 끝나면 비활성화
deactivate
```

**장점**:
- 빠름
- 명확한 에러 메시지
- IDE와 호환성 좋음

---

### CI/CD 또는 자동화 (uv run 사용)

```bash
# 가상환경 활성화 없이 바로 실행
uv run python scripts/test_token.py --mode quick
uv run pytest
uv run uvicorn app.main:app
```

**장점**:
- 스크립트에서 사용 편리
- 환경 자동 관리

---

## 빠른 참조

| 작업 | 직접 실행 | uv run |
|------|-----------|--------|
| 토큰 테스트 | `python scripts/test_token.py` | `uv run python scripts/test_token.py` |
| DB 초기화 | `python scripts/init_db.py` | `uv run python scripts/init_db.py` |
| 스케줄러 | `python scripts/start_scheduler.py` | `uv run python scripts/start_scheduler.py` |
| API 서버 | `uvicorn app.main:app --reload` | `uv run uvicorn app.main:app --reload` |
| 테스트 | `pytest` | `uv run pytest` |

---

## VSCode 설정

`.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": ".venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true
}
```

터미널을 열면 자동으로 가상환경 활성화!

---

**추천**: 대부분의 경우 **가상환경 활성화 + 직접 실행**이 가장 편리합니다! 🚀
