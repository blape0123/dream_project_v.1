"""Streamlit 실행 진입점."""

from pathlib import Path
import sys

import streamlit as st

from main import run_app


if st.runtime.exists():
    run_app()
else:
    sys.argv = [
        "streamlit",
        "run",
        str(Path(__file__).resolve()),
        *sys.argv[1:],
    ]
    from streamlit.web import cli

    raise SystemExit(cli.main())
