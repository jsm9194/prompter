# Karaoke Prompt Demo (Windows-friendly, no external API)

노래방 기계처럼 대본이 한두 줄씩 진행되고, 마이크 인식에 맞춰 하이라이트가 이동하는 데모입니다.

- API 불필요 (로컬 STT)
- 우선은 ffmpeg 없이 동작하는 경로를 목표로 했습니다.
- STT 백엔드
  - dummy : 키보드 스페이스바/엔터로 다음 줄 진행 (모델/마이크 불필요)
  - whisper : faster-whisper + sounddevice 기반. 오프라인 인식 (모델은 최초 1회 다운로드)

## 폴더 구조
- main.py / ui.py / recognizer_base.py / recognizer_dummy.py / recognizer_whisper.py / utils.py / requirements.txt / script.txt

## 빠른 시작 (Windows)
1) Python 3.10+ 권장, 가상환경 생성
   py -3.10 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install --upgrade pip

2) 의존성 설치
   pip install -r requirements.txt

3) script.txt에 한 줄당 한 문장으로 대본 입력

4) 실행
   python main.py

기본은 dummy 모드입니다. whisper 모드로 바꾸려면 main.py 상단의 recognizer_backend 값을 whisper로 변경하세요.
