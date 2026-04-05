# MyAgent Copilot 재사용 키트

## 메타
- 문서 목적: `myagent-copilot-standalone`를 다른 프로젝트에 그대로 재사용할 수 있도록, 실행 경로와 문서 구조를 운영자 관점에서 정리합니다.
- 대상 독자: 로컬 대시보드 운영자, 프런트엔드 개발자, 사내 배포 담당자, 기존 OpenClaw 연동 경험자
- 기준 운영안: `kits/myagent-copilot-kit/standalone-package`
- 현재 기준 버전/산출물: `v0.1.0`, `release/myagent-copilot-standalone-v0.1.0.zip`
- 관련 문서:
  - `../MyAgent-Standalone-문서-인덱스.md`
  - `./docs/00-INDEX.md`
  - `./standalone-package/README.md`
  - `../MYAGENT-PROXY-FRONTEND-AND-LOG-SCHEMA.md`

## 1. 이 키트가 해결하는 문제
이 키트는 다음 요구를 만족하기 위해 만들어졌습니다.
- OpenClaw 앱이나 게이트웨이를 반드시 띄우지 않아도 GitHub Copilot 기반 AI 프록시를 독립 실행할 수 있어야 한다.
- 로컬 HTML 리포트, 사내 대시보드, Vercel 프런트엔드에서 같은 API 계약으로 붙을 수 있어야 한다.
- Copilot 인증, runtime token 교환, DLP, 라우팅, 프록시 CORS, 토큰 인증을 재사용 가능한 폴더 하나로 묶어야 한다.
- 비용 해석은 항상 `무차감 관측`과 `정책상 무제한 확정 불가`를 구분해서 운영 기록에 남겨야 한다.

## 2. 기본 운영 기준
- `Standalone 우선`
  - 실제 실행 기준 폴더는 `kits/myagent-copilot-kit/standalone-package`입니다.
- `OpenClaw 경유는 호환 경로`
  - 기존 `~/.openclaw/.../auth-profiles.json`은 fallback으로 읽을 수 있지만, 기본 운영 절차는 standalone package를 기준으로 작성합니다.
- 기본 엔드포인트
  - `GET /api/ai/health`
  - `POST /api/ai/chat`
- 기본 모델
  - `github-copilot/gpt-5-mini`
- 퍼블릭 운영 필수 환경변수
  - `MYAGENT_PROXY_AUTH_TOKEN`
  - `MYAGENT_PROXY_CORS_ORIGINS`

## 3. 폴더 구조
```text
kits/myagent-copilot-kit/
├─ README.md
├─ .env.local.example
├─ .env.public.example
├─ run-local.ps1
├─ run-public.ps1
├─ run-local.sh
├─ run-public.sh
├─ healthcheck.ps1
├─ healthcheck.sh
├─ docs/
│  ├─ 00-INDEX.md
│  ├─ 01-아키텍처-개요.md
│  ├─ 02-사전준비-체크리스트.md
│  ├─ 03-로컬-실행-가이드.md
│  ├─ 04-퍼블릭-배포-가이드.md
│  ├─ 05-보안-운영-가이드.md
│  ├─ 06-장애대응-런북.md
│  ├─ 07-검증-체크리스트.md
│  ├─ 08-다른-프로젝트-적용-절차.md
│  └─ 09-오픈클로-비경유-단독-실행-가이드.md
├─ examples/
│  ├─ frontend-fetch.ts
│  ├─ frontend-axios.ts
│  └─ jpt71-runtime-config.html
└─ standalone-package/
   ├─ README.md
   ├─ OPERATIONS.md
   ├─ MIGRATION.md
   ├─ src/
   ├─ dist/
   ├─ release/
   ├─ package.json
   ├─ pnpm-lock.yaml
   ├─ build.bat
   ├─ login.bat
   ├─ token.bat
   ├─ usage.bat
   ├─ health.bat
   ├─ serve-local.bat
   ├─ serve-public.bat
   └─ export-release.bat
```

## 4. 가장 빠른 시작 경로

### 4.1 로컬 전용
1. `standalone-package`로 이동합니다.
2. `pnpm install`
3. `pnpm build`
4. `pnpm login`
5. `pnpm serve:local`
6. `GET http://127.0.0.1:3010/api/ai/health`로 헬스체크를 확인합니다.
7. 프런트에서 `http://127.0.0.1:3010/api/ai/chat`를 호출합니다.

### 4.2 퍼블릭 배포
1. 외부 서버에서 `standalone-package`를 설치합니다.
2. `MYAGENT_PROXY_AUTH_TOKEN`, `MYAGENT_PROXY_CORS_ORIGINS`를 설정합니다.
3. `pnpm build`
4. `node dist/cli.js serve --host 0.0.0.0 --port 3010`
5. HTTPS 리버스 프록시를 붙입니다.
6. Vercel 대시보드에서 엔드포인트와 토큰을 런타임 주입합니다.

## 5. 이 키트가 제공하는 실행 경로

### 5.1 독립 실행
가장 권장하는 경로입니다.
- GitHub device flow로 로그인
- runtime token 교환
- Copilot 호출
- DLP 검사
- 민감도 라우팅
- CORS/토큰 인증
- 프록시 API 제공

### 5.2 OpenClaw 호환 fallback
기존 OpenClaw 사용자가 즉시 재인증 없이 옮겨오기 위한 경로입니다.
- standalone auth store에 프로필이 없으면
- `~/.openclaw/agents/main/agent/auth-profiles.json`
- `~/.openclaw/auth-profiles.json`
를 순서대로 검사합니다.

이 경로는 편의 기능이지 기준 운영안은 아닙니다. 장기적으로는 `~/.myagent-copilot/auth-profiles.json`으로 수렴시키는 것이 맞습니다.

## 6. 지금 반드시 기억해야 할 사실
- `GET /api/ai/health`, `POST /api/ai/chat`가 유일한 공인 HTTP 인터페이스입니다.
- 기본 모델은 `github-copilot/gpt-5-mini`입니다.
- 공개 배포에서 `MYAGENT_PROXY_AUTH_TOKEN` 없이 열어 두면 안 됩니다.
- 상태 파일은 `~/.myagent-copilot` 아래 저장됩니다.
- runtime token 캐시는 `~/.myagent-copilot/cache/github-copilot.token.json`입니다.
- 인증 저장소는 `~/.myagent-copilot/auth-profiles.json`입니다.
- `release/myagent-copilot-standalone-v0.1.0.zip`를 다른 저장소로 그대로 옮길 수 있습니다.

## 7. 어떤 문서를 언제 읽는가
- 설치 전 체크가 필요하면 `./docs/02-사전준비-체크리스트.md`
- 로컬 실행이 필요하면 `./docs/03-로컬-실행-가이드.md`
- Vercel/외부 프록시가 필요하면 `./docs/04-퍼블릭-배포-가이드.md`
- DLP와 로그 정책이 중요하면 `./docs/05-보안-운영-가이드.md`
- 장애 대응이 필요하면 `./docs/06-장애대응-런북.md`
- 새 대시보드에 붙이려면 `./docs/08-다른-프로젝트-적용-절차.md`
- 완전 독립 패키지 세부는 `./standalone-package/README.md`

## 8. 빠른 검증 명령
```bash
pnpm exec tsc -p kits/myagent-copilot-kit/standalone-package/tsconfig.json --noEmit
node kits/myagent-copilot-kit/standalone-package/dist/cli.js
node kits/myagent-copilot-kit/standalone-package/dist/cli.js health
node kits/myagent-copilot-kit/standalone-package/export-release.mjs
```

## 9. 권장 운영 문구
문서, 보고서, 운영 로그에는 아래 표현을 그대로 쓰는 것을 권장합니다.
- `Standalone 우선`
- `OpenClaw 경유는 호환 경로`
- `무차감 관측`
- `정책상 무제한 확정 불가`

## 운영 공통 블록
### 검증 명령
```bash
cd kits/myagent-copilot-kit/standalone-package
pnpm install
pnpm build
pnpm health
```

### 주의사항
- 프런트에 토큰을 심어야 하는 공개 배포는 개발 편의 목적의 임시 조치로만 사용하고, 가능하면 서버 측 세션 또는 짧은 수명의 서명 토큰으로 바꾸십시오.
- HTML 리포트에 AI를 붙일 때는 `const DATA` 전체를 보내지 말고 필터/집계 요약만 보내십시오.

### 다음에 읽을 문서
- `./docs/00-INDEX.md`

### 변경 이력/기준일
- 2026-03-10: Standalone 우선 기준으로 키트 README 전면 재작성
