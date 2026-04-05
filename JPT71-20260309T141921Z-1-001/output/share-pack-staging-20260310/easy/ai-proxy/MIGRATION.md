# MIGRATION

## 메타
- 문서 목적: OpenClaw 경유 Copilot 구성에서 standalone package 중심 운영으로 옮기는 절차를 제공합니다.
- 대상 독자: 기존 OpenClaw 운영자, 이관 담당자, 문서 정비 담당자
- 기준 운영안: `kits/myagent-copilot-kit/standalone-package`
- 현재 기준 버전/산출물: `v0.1.0`, `release/myagent-copilot-standalone-v0.1.0.zip`
- 관련 문서:
  - `README.md`
  - `OPERATIONS.md`
  - `../docs/09-오픈클로-비경유-단독-실행-가이드.md`

## 1. 이관 목표
- 기본 운영 문서를 standalone package로 통일
- 인증 저장을 `~/.myagent-copilot`로 전환
- OpenClaw는 호환/비교 경로로만 유지

## 2. 사전 점검
- 현재 OpenClaw auth store 위치 확인
- 현재 대시보드 엔드포인트 확인
- 현재 프롬프트 payload 구조 확인
- 현재 CORS/origin 목록 확인

## 3. 권장 이관 절차
1. standalone package 설치
2. `pnpm build`
3. `pnpm login`
4. `pnpm health`
5. 로컬 스모크 테스트
6. 대시보드 엔드포인트를 standalone으로 전환
7. OpenClaw auth fallback 없이도 동작하는지 확인
8. 운영 문서를 standalone 기준으로 갱신

## 4. 인증 이관 전략

### 4.1 빠른 전환
- standalone auth store가 비어 있을 때 OpenClaw fallback으로 먼저 실행
- 서비스 중단 없이 전환 가능

### 4.2 권장 전환
- `pnpm login`으로 standalone store를 직접 채움
- 이후 OpenClaw fallback 의존도를 제거

## 5. 프런트 이관
- `http://127.0.0.1:3010/api/ai/chat` 또는 공개 HTTPS 엔드포인트로 변경
- request schema는 유지
- payload는 요약 JSON 유지

## 6. 문서 이관
다음 문구를 표준으로 맞춥니다.
- `Standalone 우선`
- `OpenClaw 경유는 호환 경로`
- `무차감 관측`
- `정책상 무제한 확정 불가`

## 7. 롤백
아래 중 하나면 OpenClaw 경유 경로를 임시 유지합니다.
- standalone auth login이 즉시 되지 않음
- 퍼블릭 CORS/토큰 설계가 아직 미정
- 프런트 payload 최소화가 끝나지 않음

롤백하더라도 기준 문서는 standalone package를 유지하고, OpenClaw를 임시 호환 경로로 기록하십시오.

## 운영 공통 블록
### 검증 명령
```bash
pnpm build
pnpm login
pnpm health
```

### 주의사항
- OpenClaw fallback이 동작해도 이관이 끝난 것이 아닙니다. standalone auth store와 문서 기준 전환이 끝나야 이관 완료로 보는 것이 맞습니다.

### 다음에 읽을 문서
- `../docs/07-검증-체크리스트.md`

### 변경 이력/기준일
- 2026-03-10: OpenClaw -> standalone 이관 문서 신설
