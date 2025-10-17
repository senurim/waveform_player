#!/usr/bin/env python3
"""
Waveform Player CLI
라즈베리파이의 3.5mm 오디오 잭과 SoX 프로그램을 이용하여 파형을 출력하는 프로그램
"""

import subprocess
import argparse
import sys


# 지원하는 파형 종류
SUPPORTED_WAVEFORMS = ['sine', 'square', 'triangle', 'sawtooth', 'trapezium', 'noise']


def play_waveform(frequency, waveform_type='sine', duration=5):
    """
    SoX의 play 명령을 사용하여 지정된 주파수와 파형을 출력합니다.
    
    Parameters:
    -----------
    frequency : int or float
        출력할 주파수 (Hz)
    waveform_type : str
        파형 종류 (sine, square, triangle, sawtooth, trapezium, noise)
    duration : int or float
        재생 시간 (초)
    """
    if waveform_type not in SUPPORTED_WAVEFORMS:
        print(f"Error: 지원하지 않는 파형 종류입니다. 지원 파형: {', '.join(SUPPORTED_WAVEFORMS)}")
        return False
    
    try:
        # SoX의 play 명령을 사용하여 파형 생성 및 재생
        # synth 명령: <duration> <waveform> <frequency>
        cmd = ['play', '-n', 'synth', str(duration), waveform_type, str(frequency)]
        
        print(f"파형 재생 중: {waveform_type} wave at {frequency} Hz for {duration} seconds")
        
        # 명령 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("재생 완료!")
        return True
        
    except FileNotFoundError:
        print("Error: SoX가 설치되어 있지 않습니다. 'sudo apt-get install sox'로 설치하세요.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: 파형 재생 중 오류가 발생했습니다: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error: 예상치 못한 오류가 발생했습니다: {str(e)}")
        return False


def main():
    """CLI 메인 함수"""
    parser = argparse.ArgumentParser(
        description='SoX를 사용하여 다양한 파형을 재생합니다.',
        epilog=f'지원 파형: {", ".join(SUPPORTED_WAVEFORMS)}'
    )
    
    parser.add_argument(
        'frequency',
        type=float,
        help='재생할 주파수 (Hz)'
    )
    
    parser.add_argument(
        'waveform',
        type=str,
        choices=SUPPORTED_WAVEFORMS,
        help='파형 종류'
    )
    
    parser.add_argument(
        '-d', '--duration',
        type=float,
        default=5,
        help='재생 시간 (초, 기본값: 5)'
    )
    
    args = parser.parse_args()
    
    # 파형 재생
    success = play_waveform(args.frequency, args.waveform, args.duration)
    
    # 종료 코드 설정
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
