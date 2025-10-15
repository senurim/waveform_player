#!/usr/bin/env python3
"""
GPIO Button Controlled Waveform Player
푸시 버튼 스위치를 이용하여 파형을 변경하는 프로그램
"""

import subprocess
import sys
import time

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    print("Warning: RPi.GPIO를 가져올 수 없습니다. 시뮬레이션 모드로 실행합니다.")
    GPIO = None


# 설정
DEFAULT_FREQUENCY = 440  # A4 음계
BUTTON_GPIO_PIN = 17     # GPIO 17번 핀 사용 (물리 핀 11번)
WAVEFORMS = ['sine', 'square', 'triangle', 'sawtooth', 'trapezium', 'noise']
DEBOUNCE_TIME = 300      # 디바운스 시간 (밀리초)


class WaveformPlayer:
    """파형 재생 및 제어 클래스"""
    
    def __init__(self, frequency=DEFAULT_FREQUENCY):
        self.frequency = frequency
        self.current_waveform_index = 0
        self.process = None
        self.is_playing = False
        
    def get_current_waveform(self):
        """현재 파형 이름 반환"""
        return WAVEFORMS[self.current_waveform_index]
    
    def next_waveform(self):
        """다음 파형으로 전환"""
        self.stop()
        self.current_waveform_index = (self.current_waveform_index + 1) % len(WAVEFORMS)
        print(f"\n파형 변경: {self.get_current_waveform()}")
        self.play()
    
    def play(self):
        """현재 파형 재생 시작"""
        if self.is_playing:
            return
            
        try:
            waveform = self.get_current_waveform()
            # 무한 재생을 위해 duration을 매우 크게 설정
            cmd = ['play', '-n', 'synth', '999999', waveform, str(self.frequency)]
            
            print(f"재생 시작: {waveform} wave at {self.frequency} Hz")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_playing = True
            
        except FileNotFoundError:
            print("Error: SoX가 설치되어 있지 않습니다. 'sudo apt-get install sox'로 설치하세요.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: 재생 중 오류 발생: {str(e)}")
    
    def stop(self):
        """재생 중지"""
        if self.process and self.is_playing:
            self.process.terminate()
            self.process.wait()
            self.is_playing = False
    
    def cleanup(self):
        """리소스 정리"""
        self.stop()


def button_callback(channel, player):
    """버튼 누름 콜백 함수"""
    player.next_waveform()


def main():
    """메인 함수"""
    print("=" * 60)
    print("GPIO 버튼 제어 파형 재생기")
    print("=" * 60)
    print(f"기본 주파수: {DEFAULT_FREQUENCY} Hz")
    print(f"GPIO 핀: {BUTTON_GPIO_PIN}")
    print(f"지원 파형: {', '.join(WAVEFORMS)}")
    print("버튼을 누르면 파형이 변경됩니다.")
    print("종료하려면 Ctrl+C를 누르세요.")
    print("=" * 60)
    
    # 파형 플레이어 초기화
    player = WaveformPlayer(DEFAULT_FREQUENCY)
    
    # GPIO 사용 가능 여부 확인
    if GPIO is None:
        print("\n시뮬레이션 모드: GPIO 없이 실행 중")
        print("실제 라즈베리파이에서 실행하면 버튼 제어가 가능합니다.\n")
        
        # 시뮬레이션: 5초마다 파형 변경
        try:
            player.play()
            while True:
                time.sleep(5)
                player.next_waveform()
        except KeyboardInterrupt:
            print("\n\n종료 중...")
            player.cleanup()
            sys.exit(0)
    else:
        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # 버튼 이벤트 감지 설정
        GPIO.add_event_detect(
            BUTTON_GPIO_PIN,
            GPIO.FALLING,
            callback=lambda ch: button_callback(ch, player),
            bouncetime=DEBOUNCE_TIME
        )
        
        try:
            # 초기 파형 재생
            player.play()
            
            # 무한 대기
            while True:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n종료 중...")
        finally:
            player.cleanup()
            GPIO.cleanup()
            print("정리 완료")
            sys.exit(0)


if __name__ == '__main__':
    main()
