# agentic-qa-practice — 워크숍 진입을 한 명령으로
# 사용: make help

.DEFAULT_GOAL := help
.PHONY: help install backend frontend test test-backend test-frontend clean check-tools

help: ## 사용 가능한 명령 목록
	@awk 'BEGIN {FS = ":.*##"; printf "\n명령:\n"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-tools: ## 필수 도구 (uv, node, npm) 설치 확인
	@command -v uv >/dev/null 2>&1 || { echo "❌ uv 미설치 — https://docs.astral.sh/uv/getting-started/installation/"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "❌ node 미설치 — https://nodejs.org/"; exit 1; }
	@command -v npm >/dev/null 2>&1 || { echo "❌ npm 미설치"; exit 1; }
	@echo "✓ uv $(shell uv --version | awk '{print $$2}')"
	@echo "✓ node $(shell node --version)"
	@echo "✓ npm $(shell npm --version)"

install: check-tools ## 백엔드(uv sync) + 프론트엔드(npm install) 의존성 설치
	@echo "→ backend 의존성 설치..."
	cd backend && uv sync
	@echo "→ frontend 의존성 설치..."
	cd frontend && npm install
	@echo ""
	@echo "✓ 설치 완료. 다음:"
	@echo "  make backend     # FastAPI dev 서버 (port 8000)"
	@echo "  make frontend    # Vite dev 서버 (port 5173)"
	@echo "  make test        # 전체 테스트"

backend: ## FastAPI 개발 서버 실행 (port 8000)
	cd backend && uv run uvicorn app.main:app --reload --port 8000

frontend: ## Vite 개발 서버 실행 (port 5173)
	cd frontend && npm run dev

test: test-backend test-frontend ## 백엔드 + 프론트엔드 테스트 일괄 실행

test-backend: ## 백엔드 pytest
	cd backend && uv run pytest

test-frontend: ## 프론트엔드 vitest
	cd frontend && npm test

clean: ## .venv, node_modules, sqlite db 제거
	rm -rf backend/.venv backend/rental.db backend/.pytest_cache
	rm -rf frontend/node_modules frontend/dist
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ 정리 완료"
