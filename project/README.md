# GPS 위치 오차 시뮬레이터

GPS 측정 위치의 최대 오차를 고려하여 실제 위치가 원형 영역의 내부인지,
외부인지 또는 판단이 불확실한지 계산하고 시각화하는 Streamlit 앱입니다.

## 실행 환경

- Python 3.10 이상
- Streamlit
- NumPy
- Matplotlib

## 설치 및 실행

프로젝트 폴더에서 아래 명령을 실행합니다.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

`app.py`는 직접 실행 시 Streamlit 서버를 시작합니다. Streamlit 명령으로 실행해도 됩니다.

```bash
streamlit run app.py
```

## GitHub Pages에 배포하기

브라우저에서 바로 실행할 수 있도록 정적 버전이 [`docs/index.html`](../docs/index.html)에 있습니다.
이 버전은 Python 서버나 별도 빌드 과정 없이 작동하며, 기존 `app.py` Streamlit 버전도 로컬 실행에 사용할 수 있습니다.

1. 저장소의 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 설정합니다.
2. `main` 브랜치에 변경 사항을 푸시하거나 Actions 탭에서 **Deploy static site to GitHub Pages**를 수동 실행합니다.
3. Actions 실행이 성공하면 [GitHub Pages 사이트](https://blape0123.github.io/dream_project_v.1/)에서 앱을 사용할 수 있습니다.

## 사용 방법

좌측 패널의 슬라이더에서 원의 중심 좌표, 반지름, 측정 좌표와 최대 오차 ε을 조절합니다.
슬라이더를 움직이면 같은 화면의 그래프, 판별 결과, 거리 및 수학적 조건이 즉시 갱신됩니다.
좌표는 -20~20, 반지름과 최대 오차는 0~20 범위에서 조절할 수 있습니다.
아래 실험 A~D의 오차값을 변경하면 같은 좌표와 영역에서 결과를 비교할 수 있습니다.

기본 예시는 중심 `(0, 0)`, 반지름 `5`, 측정 위치 `(3, 0)`, 오차 `1`입니다.

## 판별 기준

- 반드시 내부: `d + ε ≤ r`
- 반드시 외부: `d - ε > r`
- 판단 불확실: 위 두 조건 모두 성립하지 않음

여기서 `d = √((x-a)² + (y-b)²)`입니다. ε은 실제 위치와 측정 위치 사이
거리의 최대값이라는 가정이며, 실제 GPS 오차가 항상 이 범위 안에 있다는 뜻은 아닙니다.
