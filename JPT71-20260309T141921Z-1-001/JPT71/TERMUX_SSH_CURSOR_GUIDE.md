Ask 모드에서는 파일을 직접 생성·수정할 수 없습니다. 아래 내용을 복사해 새 파일로 저장하시거나, Agent 모드로 전환해 주시면 제가 직접 문서를 작성하겠습니다.

---

# Termux SSH 서버 설정 및 Cursor 터미널 접속 가이드

> **범위**: Termux SSH 서버 설정 → Cursor/VS Code 원격 접속 (Wi-Fi 및 USB+ADB)
> **대상**: termux_wa_ops 및 CONVERT 프로젝트 모바일 원격 관리

---

## 1. 요약

| 항목 | 값 |
|------|-----|
| **Termux 설치** | F-Droid 또는 GitHub (Play Store 비권장) |
| **SSH 포트** | 8022 |
| **인증** | 공개키 인증 권장 |
| **접속 방식** | Wi-Fi 동일망 또는 USB+ADB 포워딩 |

---

## 2. 모바일 준비 체크리스트

| No | 항목 | 명령/값 | 리스크 |
|:--:|------|---------|--------|
| 1 | Termux 설치 | F-Droid 또는 GitHub | Play Store → 플러그인 충돌 |
| 2 | 패키지 업데이트 | `pkg update && pkg upgrade -y` | 구버전 시 설치 실패 |
| 3 | OpenSSH 설치 | `pkg install openssh` | 미설치 시 접속 불가 |
| 4 | termux-api 설치 | `pkg install termux-api` | wake-lock, IP 확인용 |
| 5 | 호스트 키 생성 | `ssh-keygen -A` | 최초 1회 |
| 6 | sshd 실행 | `sshd` (포트 8022) | 절전/백그라운드 종료 |
| 7 | Wake-lock | `termux-wake-lock` | Android 13+ 필수 |
| 8 | 공개키 인증 | `~/.ssh/authorized_keys` | 비밀번호 노출/추측 위험 |

---

## 3. 설치 및 기동 (원샷)

Termux에서 한 번에 실행:

```bash
pkg update -y && pkg upgrade -y \
&& pkg install -y openssh termux-api iproute2 net-tools jq \
&& ssh-keygen -A \
&& termux-wake-lock \
&& sshd \
&& echo -e "\n[OK] 사용자: $(whoami)   포트: 8022" \
&& echo -n "[Wi-Fi IP] " && (termux-wifi-connectioninfo 2>/dev/null | jq -r '.ip // "확인 불가"' || echo "확인 불가")
```

**정상 출력 예**: `[OK] 사용자: u0_a551   포트: 8022`  
**IP 확인**: `termux-wifi-connectioninfo` 출력의 `"ip"` 필드 사용 (Android 13+에서 `ip addr` 대신 권장)

---

## 4. 공개키 인증 설정

### 방법 A: 공개키 직접 붙여넣기

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat > ~/.ssh/authorized_keys <<'EOF'
# 여기에 PC 공개키 한 줄 전체 붙여넣기 (ssh-ed25519 ... 또는 ssh-rsa ...)
EOF
chmod 600 ~/.ssh/authorized_keys
pkill sshd 2>/dev/null; sshd
```

### 방법 B: Downloads 폴더 이용

```bash
termux-setup-storage
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat ~/storage/downloads/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
pkill sshd 2>/dev/null; sshd
```

---

## 5. Wi-Fi IP 확인 (Android 13+)

`ip addr`가 동작하지 않을 때:

```bash
termux-wifi-connectioninfo
```

출력 예: `"ip": "10.225.155.87"` → 이 값을 접속 IP로 사용

---

## 6. Cursor 터미널 접속

### 방법 ① Wi-Fi 동일망

PC와 폰이 같은 Wi-Fi에 연결된 경우:

```bash
ssh -p 8022 <사용자>@<모바일_IP>
```

예: `ssh -p 8022 u0_a551@10.225.155.87`

### 방법 ② USB + ADB 포워딩

Wi-Fi가 불안정하거나 다른 네트워크일 때 권장.

#### 6.1 폰 준비

1. 설정 → 휴대전화 정보 → 빌드 번호 7번 탭 → 개발자 옵션 활성화  
2. 설정 → 개발자 옵션 → USB 디버깅 ON  
3. USB 연결 → "USB 디버깅 허용?" → 항상 허용 후 허용

#### 6.2 PC에 ADB 설치

- **다운로드**: https://developer.android.com/tools/releases/platform-tools  
- **Windows**: ZIP 압축 해제 → `platform-tools` 경로를 PATH에 추가  
- **macOS**: `brew install android-platform-tools` 또는 수동 PATH 추가  
- **Linux**: `sudo apt install android-sdk-platform-tools`

#### 6.3 연결 확인

```bash
adb devices
# "device" 상태여야 함
```

#### 6.4 포워딩 및 접속

```bash
adb forward tcp:8022 tcp:8022
ssh -p 8022 u0_a551@localhost
```

---

## 7. 문제 해결

| 증상 | 확인 | 조치 |
|------|------|------|
| Connection refused | `ps -e \| grep sshd`, `ss -lntp \| grep 8022` | `pkill sshd; sshd` |
| 접속 후 바로 끊김 | wake-lock, 배터리 설정 | `termux-wake-lock`, 배터리 최적화 해제 |
| 키 인증 실패 | `ls -l ~/.ssh/` | `~/.ssh` 700, `authorized_keys` 600 |
| IP 확인 불가 | `termux-wifi-connectioninfo` | Wi-Fi 연결 확인, 폰 설정에서 IP 직접 확인 |
| adb devices 비어 있음 | USB 디버깅, 케이블 | USB 디버깅 허용 팝업, 케이블/포트 교체 |

---

## 8. 원샷 명령어 요약

| 용도 | 명령 |
|------|------|
| 최소 설치+기동 | `pkg update -y && pkg upgrade -y && pkg install -y openssh && ssh-keygen -A && sshd && echo "[OK] $(whoami):8022"` |
| sshd 재시작 | `pkill sshd 2>/dev/null; sshd; echo "[OK] sshd restarted"` |
| Wake-lock | `termux-wake-lock` |
| IP 확인 | `termux-wifi-connectioninfo \| jq -r '.ip'` |

---

## 9. Cursor 활용 팁

- **Remote-SSH**: Cursor/VS Code Remote-SSH로 모바일 프로젝트 직접 편집  
- **SSH config** (PC `~/.ssh/config`):

```
Host termux-phone
    HostName 192.168.1.150
    User u0_a551
    Port 8022
    ServerAliveInterval 60
```

→ `ssh termux-phone` 또는 Cursor에서 해당 Host로 접속

- **tmux**: `pkg install tmux` 후 세션 유지로 끊김 완화

---

## 10. wa_ops 연동

SSH 접속 후 wa_ops 확인·실행:

```bash
ls ~/wa_ops/
sqlite3 ~/wa_ops/ops.db "SELECT COUNT(*) FROM wa_events WHERE date(ts)=date('now');"
~/wa_ops/poll_and_ingest.sh
~/wa_ops/daily_drive.sh
```

---

## 참고 자료

- [termux/termux-app (GitHub)](https://github.com/termux/termux-app)
- [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools)
- [termux_wa_ops README](./README.md)
- [termux_wa_ops SYSTEM_ARCHITECTURE](./SYSTEM_ARCHITECTURE.md)

---

이 내용을 `termux_wa_ops/TERMUX_SSH_CURSOR_GUIDE.md` 등으로 저장해 사용하시면 됩니다. Agent 모드로 전환하시면 제가 직접 파일을 생성·수정해 드릴 수 있습니다.