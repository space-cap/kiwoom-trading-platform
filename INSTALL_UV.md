# UV 사용 설치 가이드

## UV란?

`uv`는 Rust로 작성된 초고속 Python 패키지 관리자입니다. pip보다 10-100배 빠릅니다.

## 설치 방법

### 1. UV 설치 (아직 설치하지 않은 경우)

Windows PowerShell:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

또는 pip로:
```bash
pip install uv
```

### 2. 가상환경 생성 및 활성화

이미 `.venv`가 있으니 활성화만 하면 됩니다:

```bash
.venv\Scripts\activate  # Windows
```

### 3. 프로젝트 의존성 설치

#### 기본 의존성 설치:
```bash
uv pip install -e .
```

또는 개별 패키지 설치:
```bash
uv pip install fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings httpx python-dotenv apscheduler pytz alembic
```

#### 개발 의존성 포함:
```bash
uv pip install -e ".[dev]"
```

또는:
```bash
uv pip install pytest pytest-asyncio pytest-cov pytest-mock black isort flake8 mypy
```

### 4. UV ADD 명령어 사용 (새 패키지 추가 시)

새 패키지를 추가하려면:
```bash
uv add <package-name>
```

예시:
```bash
uv add requests
uv add --dev pytest
```

### 5. 설치 확인

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

## UV의 장점

1. **속도**: pip보다 10-100배 빠름
2. **의존성 해결**: 더 빠르고 정확한 의존성 해결
3. **호환성**: pip와 동일한 방식으로 작동
4. **안정성**: Rust 기반으로 메모리 안전성 보장

## 자주 사용하는 UV 명령어

```bash
# 패키지 설치
uv pip install <package>

# 패키지 제거
uv pip uninstall <package>

# requirements.txt 설치
uv pip install -r requirements.txt

# 현재 설치된 패키지 목록
uv pip list

# 패키지 업그레이드
uv pip install --upgrade <package>

# 전체 업그레이드
uv pip install --upgrade -r requirements.txt
```

## 프로젝트에서 UV 사용하기

### pyproject.toml vs requirements.txt

현재 `pyproject.toml`에 의존성이 정의되어 있으므로:

```bash
# 설치
uv pip install -e .

# 또는 requirements.txt 생성 후
uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt
```

### 가상환경 동기화

```bash
uv pip sync requirements.txt
```

## 문제 해결

### UV가 느린 경우

캐시 초기화:
```bash
uv cache clean
```

### 의존성 충돌

```bash
uv pip install --force-reinstall <package>
```

## 참고 자료

- UV 공식 문서: https://github.com/astral-sh/uv
- UV 벤치마크: https://astral.sh/blog/uv
