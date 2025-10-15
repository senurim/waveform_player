# waveform_player
라즈베리파이의 3.5mm 오디오 잭과 SoX 프로그램을 이용하여 주어진 주파수를 가지는 5가지 이상의 파형을 출력하는 파이썬 프로그램을 구현하고자 함. 푸시 버튼 스위치를 이용하여 디폴트 주파수의 파형을 변화시킬 수 있다.

## 기능

- **6가지 파형 지원**: sine, square, triangle, sawtooth, trapezium, noise
- **CLI 모드**: 명령줄에서 주파수와 파형 종류를 지정하여 재생
- **GPIO 버튼 제어**: 푸시 버튼으로 파형 전환 (라즈베리파이 전용)

## 요구사항

### 시스템 요구사항
- Python 3.x
- SoX (Sound eXchange) 오디오 처리 프로그램
- 라즈베리파이 (GPIO 제어 기능 사용 시)

### 설치

1. SoX 설치:
```bash
sudo apt-get update
sudo apt-get install sox
```

2. Python GPIO 라이브러리 설치 (라즈베리파이에서 GPIO 제어 시):
```bash
pip install RPi.GPIO
```

## 사용법

### 1. CLI 파형 재생기 (`waveform_player.py`)

기본 사용법:
```bash
python3 waveform_player.py <주파수> <파형종류>
```

예제:
```bash
# 440Hz sine 파형을 5초간 재생
python3 waveform_player.py 440 sine

# 1000Hz square 파형을 10초간 재생
python3 waveform_player.py 1000 square -d 10

# 880Hz triangle 파형을 3초간 재생
python3 waveform_player.py 880 triangle --duration 3
```

지원하는 파형:
- `sine` - 사인파
- `square` - 구형파
- `triangle` - 삼각파
- `sawtooth` - 톱니파
- `trapezium` - 사다리꼴파
- `noise` - 노이즈

옵션:
- `-d, --duration`: 재생 시간(초) (기본값: 5초)
- `-h, --help`: 도움말 표시

### 2. GPIO 버튼 제어 파형 재생기 (`gpio_waveform_player.py`)

기본 사용법:
```bash
python3 gpio_waveform_player.py
```

특징:
- GPIO 17번 핀(물리 핀 11번)에 연결된 푸시 버튼으로 제어
- 버튼을 누를 때마다 파형이 순환 변경됨 (sine → square → triangle → sawtooth → trapezium → noise → sine ...)
- 기본 주파수: 440Hz (A4 음계)
- Ctrl+C로 종료

#### 하드웨어 연결

```
라즈베리파이 GPIO 연결:
- GPIO 17 (물리 핀 11) ----[푸시버튼]---- GND (물리 핀 9)
```

푸시 버튼 회로:
- 내부 풀업 저항 사용
- 버튼을 누르면 GPIO 17이 LOW로 변경
- 디바운스 시간: 300ms

#### 시뮬레이션 모드

라즈베리파이가 아닌 환경에서도 실행 가능:
- GPIO 라이브러리 없이 실행하면 자동으로 시뮬레이션 모드로 전환
- 5초마다 자동으로 파형이 변경됨
- 프로그램 동작 확인 및 테스트용

## 코드 구조

```
waveform_player/
├── README.md                      # 이 파일
├── waveform_player.py             # CLI 파형 재생기
└── gpio_waveform_player.py        # GPIO 버튼 제어 파형 재생기
```

## 라이선스

Apache License 2.0

## 참고사항

- 3.5mm 오디오 잭 사용 시 스피커나 헤드폰 연결 필요
- 볼륨 조절은 시스템 볼륨 또는 `alsamixer` 사용
- GPIO 핀 번호는 BCM 모드 기준
