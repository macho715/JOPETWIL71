# 문서 인덱스

## 메타
- 문서 목적: `myagent-copilot-kit` 내부 문서 세트를 한 번에 파악할 수 있도록, 읽기 순서와 분기 기준을 제공합니다.
- 대상 독자: 처음 키트를 접하는 운영자와 개발자, OpenClaw 경유 구성을 standalone package로 옮기려는 사용자
- 기준 운영안: `kits/myagent-copilot-kit/standalone-package`
- 현재 기준 버전/산출물: `v0.1.0`, `release/myagent-copilot-standalone-v0.1.0.zip`
- 관련 문서:
  - `../README.md`
  - `../../MyAgent-Standalone-문서-인덱스.md`
  - `../standalone-package/README.md`

## 1. 읽기 순서

### 1.1 처음 설치할 때
1. `02-사전준비-체크리스트.md`
2. `03-로컬-실행-가이드.md`
3. `07-검증-체크리스트.md`

### 1.2 퍼블릭으로 운영할 때
1. `01-아키텍처-개요.md`
2. `04-퍼블릭-배포-가이드.md`
3. `05-보안-운영-가이드.md`
4. `07-검증-체크리스트.md`

### 1.3 새 프로젝트에 붙일 때
1. `08-다른-프로젝트-적용-절차.md`
2. `05-보안-운영-가이드.md`
3. `07-검증-체크리스트.md`

### 1.4 OpenClaw에서 넘어올 때
1. `09-오픈클로-비경유-단독-실행-가이드.md`
2. `../standalone-package/MIGRATION.md`
3. `07-검증-체크리스트.md`

## 2. 문서별 목적
- `01-아키텍처-개요.md`
  - 전체 컴포넌트와 신뢰 경계 설명
- `02-사전준비-체크리스트.md`
  - 설치 전 확인 항목
- `03-로컬-실행-가이드.md`
  - 로컬 프록시 실행 절차
- `04-퍼블릭-배포-가이드.md`
  - 외부 서버와 HTTPS 프록시 운영 절차
- `05-보안-운영-가이드.md`
  - DLP, 라우팅, 토큰, 로그 기준
- `06-장애대응-런북.md`
  - 에러별 진단 및 복구
- `07-검증-체크리스트.md`
  - 표준 테스트 순서
- `08-다른-프로젝트-적용-절차.md`
  - 새 프런트엔드/대시보드에 AI 붙이는 방법
- `09-오픈클로-비경유-단독-실행-가이드.md`
  - OpenClaw 제품 비경유와 standalone package의 차이

## 3. 기본 기준값
- 기본 엔드포인트: `GET /api/ai/health`, `POST /api/ai/chat`
- 기본 모델: `github-copilot/gpt-5-mini`
- 공개 배포 필수 환경변수: `MYAGENT_PROXY_AUTH_TOKEN`, `MYAGENT_PROXY_CORS_ORIGINS`
- 상태 경로: `~/.myagent-copilot`
- fallback auth store: `~/.openclaw/.../auth-profiles.json`
- 배포 산출물: `release/myagent-copilot-standalone-v0.1.0.zip`

## 4. 문서 전반의 표현 규칙
- `Standalone 우선`
- `OpenClaw 경유는 호환 경로`
- `무차감 관측`
- `정책상 무제한 확정 불가`

이 표현은 키트 문서뿐 아니라 루트 문서에서도 동일하게 사용합니다.

## 5. 최소 실행 경로
```bash
cd kits/myagent-copilot-kit/standalone-package
pnpm install
pnpm build
pnpm login
pnpm serve:local
```

그다음 브라우저나 프런트에서 `http://127.0.0.1:3010/api/ai/health`를 열어 응답을 확인합니다.

## 운영 공통 블록
### 검증 명령
```bash
node ../standalone-package/dist/cli.js health
node ../standalone-package/dist/cli.js
```

### 주의사항
- 문서 인덱스는 요약용이 아니라 진입점입니다. 실제 실행은 반드시 각 상세 문서를 따르십시오.

### 다음에 읽을 문서
- `01-아키텍처-개요.md`

### 변경 이력/기준일
- 2026-03-10: Standalone 우선 기준으로 키트 문서 인덱스 전면 재작성
