# -*- coding: utf-8 -*-
"""Current VTA narrative patch authority (v113).

This wrapper intentionally delegates to the idempotent v113b implementation.
It exists so rerunning the canonical v113 entry point cannot stop after a
partially applied historical anchor.
"""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("patch_vta_causal_spine_v113b.py")), run_name="__main__")
