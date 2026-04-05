# OPERATIONS

## 메타
- 문서 목적: standalone package의 일상 운영, 점검, 재시작, 토큰 교체, 장애 대응, 업데이트 절차를 정리합니다.
- 대상 독자: 운영자, on-call 담당자, 서비스 소유자
- 기준 운영안: `kits/myagent-copilot-kit/standalone-package`
- 현재 기준 버전/산출물: `v0.1.0`, `release/myagent-copilot-standalone-v0.1.0.zip`
- 관련 문서:
  - `README.md`
  - `MIGRATION.md`
  - `../docs/06-장애대응-런북.md`

## 1. 일상 운영 체크
- 프로세스 생존 확인
- `GET /api/ai/health` 확인
- 최근 오류 로그 확인
- origin allowlist와 토큰 설정 유지 확인
- DLP 차단 비율 이상 유무 확인

## 2. 시작/정지/재시작

### 2.1 시작
```bash
node dist/cli.js serve --host 127.0.0.1 --port 3010
```

### 2.2 재시작
1. 기존 프로세스 종료
2. 환경변수 재확인
3. 동일 명령으로 재기동

### 2.3 Windows 배치
- `serve-local.bat`
- `serve-public.bat`

## 3. 정기 점검
- 하루 1회 health 확인
- 토큰 만료 또는 auth 오류 여부 확인
- `pnpm usage` 결과 보관
- zip export 재생성 여부 확인

## 4. 토큰 교체

### 4.1 GitHub 로그인 재실행
```bash
pnpm login
```

### 4.2 프록시 인증 토큰 교체
- `MYAGENT_PROXY_AUTH_TOKEN` 새 값 발급
- 프록시 재기동
- 프런트 런타임 토큰 동시 교체

## 5. 업데이트 절차
1. 새 소스 또는 새 zip 확보
2. `pnpm install --frozen-lockfile`
3. `pnpm build`
4. `node dist/cli.js health`
5. 스모크 테스트
6. 프록시 재기동

## 6. 로그 운영
- 운영 로그 스키마: `openclaw.copilot.proxy.log.v1`
- 장기 보관 시 requestId, route, dlpStatus, latency 중심으로 수집
- payload 전문 저장 금지

## 7. 권장 롤백 기준
- CORS allowlist 관리 실패
- sanitize/local 정책 충돌 반복
- 프런트 토큰 유출 의심
- GitHub auth가 불안정하여 재인증이 반복

## 운영 공통 블록
### 검증 명령
```bash
node dist/cli.js health
node dist/cli.js usage --json
```

### 주의사항
- 운영 중 변경은 문서와 설정을 같이 갱신해야 합니다. 실제 값만 바꾸고 문서를 안 바꾸면 이후 감사와 복구가 어려워집니다.

### 다음에 읽을 문서
- `MIGRATION.md`

### 변경 이력/기준일
- 2026-03-10: standalone package 운영 문서 신설
