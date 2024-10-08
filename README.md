# 2022

# 딥러닝과 귓바퀴 구조를 이용한 소리의 방향 탐지 연구

이 프로젝트는 다양한 귓바퀴 모양과 인공지능 알고리즘을 이용하여 효과적인 소리 방향 탐지 장치를 개발하는 연구입니다.

## 프로젝트 개요

인간이 소리의 방향을 구분하는 세 가지 주요 방법(ILD, ITD, Monaural Spectral Cues)을 바탕으로, 기계적인 방법으로 소리의 방향을 탐지하는 시스템을 개발했습니다. 이 연구의 목적은 귓바퀴 모양을 활용하여 적은 수의 마이크로도 효과적인 방향 구분이 가능한 시스템을 만드는 것입니다.

## 주요 기능

1. 구 좌표계 상의 모든 방향에서 소리 데이터 수집
2. 딥러닝 데이터 수집기를 통한 소리 데이터 처리
3. CNN을 활용한 인공지능 알고리즘으로 소리 방향 분석

## 파일 구조

- `TSM_dataset/`: 훈련 데이터셋 폴더
- `SoundLocalization_Model_.ipynb`: 소리 위치 탐지 모델 Jupyter 노트북
- `TSM_Train_set_maker.py`: 훈련 데이터셋 생성 Python 스크립트

## 연구 방법

1. 두 개의 귓바퀴가 각각 접합된 마이크를 사용하여 구 좌표계의 각 단위 방향에서 박수 소리 수집
2. 수집된 소리 데이터를 딥러닝 데이터 수집기(TSM)로 처리
3. CNN 기반 인공지능 알고리즘을 사용하여 소리 방향 분석 (회귀 문제로 접근)

## 데이터 수집기 (TSM)

TSM(Train Set Maker)은 구 좌표계 상의 소리 데이터를 수집하기 위해 제작된 장치입니다. 

### TSM-1
- 초기 버전
- 마이크와 귓바퀴 구조물, 라즈베리 파이, L298N 스텝 모터 컨트롤러로 구성
- 문제점: 모터 토크 부족, 발열로 인한 부품 손상

### TSM-2
- 개선된 버전
- 경량화된 회전자, 핀 마이크 사용, 서보모터로 Polar angle 회전 담당
- 여전히 서보모터의 간헐적 오작동 문제 존재

## 인공지능 모델

- CNN 기반 모델 사용
- 좌우 마이크 입력을 병렬 처리
- 처리 순서: Input → STFT Transform → Resize → Normalize → Convolution
- Concatenate Layer에서 좌우 신호 병합 후 Dense Layer 처리
- 약 85.5%의 정확도로 소리 방향 구분 가능

## 결과 및 향후 계획

이 연구를 통해 귓바퀴 구조와 딥러닝을 활용한 소리 방향 탐지 시스템의 가능성을 확인했습니다. 향후 연구에서는 다음과 같은 개선을 계획하고 있습니다:

1. 데이터 수집기(TSM) 안정성 향상
2. 다양한 귓바퀴 구조 실험 및 최적화
3. 인공지능 모델 성능 개선 및 최적화

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)하에 배포됩니다.