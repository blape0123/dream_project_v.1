"""GPS 측정 오차에 따른 원형 영역 판별 시뮬레이터."""

from __future__ import annotations

import math
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import streamlit as st


INSIDE = "반드시 내부"
OUTSIDE = "반드시 외부"
UNCERTAIN = "판단 불확실"

RESULT_MESSAGES = {
    INSIDE: "측정 오차를 고려해도 실제 위치는 영역 내부에 존재합니다.",
    OUTSIDE: "측정 오차를 고려해도 실제 위치는 영역 외부에 존재합니다.",
    UNCERTAIN: "측정 오차로 인해 실제 위치가 영역 내부인지 외부인지 확정할 수 없습니다.",
}


def classify_location(
    center_x: float,
    center_y: float,
    radius: float,
    measured_x: float,
    measured_y: float,
    max_error: float,
) -> dict[str, Any]:
    """입력값을 검증하고 거리, 조건 및 판별 결과를 계산한다."""
    values = (center_x, center_y, radius, measured_x, measured_y, max_error)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("모든 입력값은 유한한 숫자여야 합니다.")
    if radius <= 0:
        raise ValueError("영역의 반지름은 0보다 커야 합니다.")
    if max_error < 0:
        raise ValueError("최대 오차 ε은 0 이상이어야 합니다.")

    distance = math.hypot(measured_x - center_x, measured_y - center_y)
    definitely_inside = distance + max_error <= radius
    definitely_outside = distance - max_error > radius
    if definitely_inside:
        result = INSIDE
    elif definitely_outside:
        result = OUTSIDE
    else:
        result = UNCERTAIN

    return {
        "distance": distance,
        "min_distance": max(0.0, distance - max_error),
        "max_distance": distance + max_error,
        "definitely_inside": definitely_inside,
        "definitely_outside": definitely_outside,
        "result": result,
    }


def _draw_plot(
    center_x: float,
    center_y: float,
    radius: float,
    measured_x: float,
    measured_y: float,
    max_error: float,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.add_patch(
        Circle(
            (center_x, center_y),
            radius,
            facecolor="#3b82f6",
            edgecolor="#1d4ed8",
            linewidth=2,
            alpha=0.2,
            label="Target region",
        )
    )
    ax.add_patch(
        Circle(
            (measured_x, measured_y),
            max_error,
            facecolor="#f59e0b",
            edgecolor="#d97706",
            linewidth=2,
            alpha=0.28,
            label="Maximum error range",
        )
    )
    ax.plot(
        [center_x, measured_x],
        [center_y, measured_y],
        color="#475569",
        linestyle="--",
        linewidth=1.5,
        label="Center-to-measurement segment",
        zorder=3,
    )
    ax.scatter(
        [center_x],
        [center_y],
        color="#1d4ed8",
        marker="x",
        s=85,
        linewidths=2.5,
        label="Region center C",
        zorder=5,
    )
    ax.scatter(
        [measured_x],
        [measured_y],
        color="#dc2626",
        edgecolors="white",
        linewidths=0.8,
        s=75,
        label="Measured position P",
        zorder=6,
    )

    x_values = (center_x - radius, center_x + radius, measured_x - max_error, measured_x + max_error)
    y_values = (center_y - radius, center_y + radius, measured_y - max_error, measured_y + max_error)
    span = max(max(x_values) - min(x_values), max(y_values) - min(y_values), 1.0)
    padding = span * 0.12
    ax.set_xlim(min(x_values) - padding, max(x_values) + padding)
    ax.set_ylim(min(y_values) - padding, max(y_values) + padding)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Measured Position and Error Range")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    return fig


def run_app() -> None:
    st.set_page_config(
        page_title="GPS 위치 오차 시뮬레이터",
        page_icon="📍",
        layout="wide",
    )
    st.title("GPS 위치 측정 오차에 따른 공간 영역 판별")
    st.markdown(
        "측정 위치와 최대 오차를 바탕으로 실제 위치가 원형 영역의 내부인지, "
        "외부인지, 또는 확정할 수 없는지 살펴봅니다."
    )

    with st.sidebar:
        st.header("좌표와 영역 설정")
        center_x = st.slider(
            "영역 중심의 X좌표 (a)",
            min_value=-20.0,
            max_value=20.0,
            value=0.0,
            step=0.1,
            key="center_x",
        )
        center_y = st.slider(
            "영역 중심의 Y좌표 (b)",
            min_value=-20.0,
            max_value=20.0,
            value=0.0,
            step=0.1,
            key="center_y",
        )
        radius = st.slider(
            "영역의 반지름 (r)",
            min_value=0.1,
            max_value=20.0,
            value=5.0,
            step=0.1,
            key="radius",
        )
        measured_x = st.slider(
            "측정 위치의 X좌표",
            min_value=-20.0,
            max_value=20.0,
            value=3.0,
            step=0.1,
            key="measured_x",
        )
        measured_y = st.slider(
            "측정 위치의 Y좌표",
            min_value=-20.0,
            max_value=20.0,
            value=0.0,
            step=0.1,
            key="measured_y",
        )
        max_error = st.slider(
            "최대 오차 (ε)",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=0.1,
            help="측정 위치와 실제 위치 사이 거리의 최대값으로 가정합니다.",
        )
        st.caption(
            "슬라이더를 움직이면 그래프와 판별 결과가 즉시 갱신됩니다. "
            "좌표 범위는 -20~20, 반지름·최대 오차는 0~20입니다."
        )

    try:
        analysis = classify_location(
            center_x, center_y, radius, measured_x, measured_y, max_error
        )
    except ValueError as error:
        st.error(str(error))
        st.info("유효한 입력값을 설정하면 그래프와 판별 결과가 표시됩니다.")
        return

    graph_column, result_column = st.columns([1.25, 1])
    with graph_column:
        st.subheader("좌표평면 시각화")
        figure = _draw_plot(center_x, center_y, radius, measured_x, measured_y, max_error)
        st.pyplot(figure, width="stretch")
        plt.close(figure)

    with result_column:
        st.subheader("판별 결과")
        if analysis["result"] == INSIDE:
            st.success(RESULT_MESSAGES[INSIDE])
        elif analysis["result"] == OUTSIDE:
            st.error(RESULT_MESSAGES[OUTSIDE])
        else:
            st.warning(RESULT_MESSAGES[UNCERTAIN])
        st.markdown(f"**최종 판별: {analysis['result']}**")

        metric_columns = st.columns(2)
        metric_columns[0].metric("중심과 측정 위치 사이 거리 d", f"{analysis['distance']:.4f}")
        metric_columns[1].metric("최대 오차 ε", f"{max_error:.4f}")
        st.write(
            "실제 위치와 중심 사이 거리의 가능한 범위: "
            f"[{analysis['min_distance']:.4f}, {analysis['max_distance']:.4f}]"
        )
        st.latex(r"d = \sqrt{(x-a)^2 + (y-b)^2}")
        inside_operator = r"\leq" if analysis["definitely_inside"] else ">"
        outside_operator = ">" if analysis["definitely_outside"] else r"\leq"
        st.latex(
            rf"d + \varepsilon = {analysis['distance']:.4f} + {max_error:.4f}"
            rf" = {analysis['distance'] + max_error:.4f}"
            rf" \; {inside_operator} \; r={radius:.4f}"
        )
        st.latex(
            rf"d - \varepsilon = {analysis['distance']:.4f} - {max_error:.4f}"
            rf" = {analysis['distance'] - max_error:.4f}"
            rf" \; {outside_operator} \; r={radius:.4f}"
        )

    st.divider()
    st.header("오차 변화 실험")
    st.write("좌표와 영역은 고정하고 오차 ε만 바꾸어 판별 결과를 비교합니다.")
    experiment_columns = st.columns(4)
    experiment_names = ("실험 A", "실험 B", "실험 C", "실험 D")
    default_errors = (0.5, 1.0, 2.0, 3.0)
    experiment_errors = [
        column.number_input(
            f"{name}: ε",
            min_value=0.0,
            value=default_error,
            step=0.5,
            key=f"experiment_error_{name[-1]}",
        )
        for column, name, default_error in zip(
            experiment_columns, experiment_names, default_errors
        )
    ]
    experiment_rows = []
    for name, error in zip(experiment_names, experiment_errors):
        experiment = classify_location(
            center_x, center_y, radius, measured_x, measured_y, error
        )
        experiment_rows.append(
            {
                "실험": name,
                "최대 오차 ε": f"{error:.2f}",
                "거리 d": f"{experiment['distance']:.4f}",
                "오차 범위 반지름": f"{error:.2f}",
                "가능한 중심 거리": (
                    f"[{experiment['min_distance']:.4f}, {experiment['max_distance']:.4f}]"
                ),
                "판별 결과": experiment["result"],
            }
        )
    st.dataframe(experiment_rows, hide_index=True, width="stretch")

    with st.expander("수학적 판별 원리"):
        st.markdown(
            """
            영역의 중심을 `C(a, b)`, 반지름을 `r`, 측정 위치를 `P(x, y)`,
            측정 오차의 최대값을 `ε`이라고 합니다. 원의 내부는
            `(x-a)² + (y-b)² ≤ r²`로 나타냅니다.

            - **반드시 내부:** `d + ε ≤ r` — 가능한 모든 실제 위치가 원 안에 있습니다.
            - **반드시 외부:** `d - ε > r` — 가능한 모든 실제 위치가 원 밖에 있습니다.
            - **판단 불확실:** 위 두 조건 모두 성립하지 않아 내부·외부를 확정할 수 없습니다.

            `ε`은 실제 위치와 측정 위치 사이 거리의 최대값이라는 가정입니다.
            실제 GPS 오차가 항상 이 범위 안에 있다는 뜻은 아닙니다.
            경계에서 `d + ε = r`이면 반드시 내부이며, `d - ε = r`이면
            반드시 외부 조건의 엄격 부등호를 만족하지 않으므로 판단 불확실입니다.
            """
        )


if __name__ == "__main__":
    run_app()