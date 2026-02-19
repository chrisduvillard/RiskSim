# RiskSim Audit Report

**Date:** 2026-02-19
**Auditor:** Claude Code
**Commit:** c16d039 (main branch, clean working tree)

---

## How the App Was Run

```bash
cd C:\Users\ChristopheDuvillard\Documents\CODING\RiskSim
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run Welcome.py
```

Navigated to all three views:
1. **Welcome** page (Welcome.py) - landing page with image and feature descriptions
2. **Risk-Return Analysis** (pages/1_risk_return_analysis.py) - Monte Carlo trading simulation
3. **Asset Correlation** (pages/2_asset_correlation.py) - synthetic portfolio simulator

---

## Issues Found

### BLOCKER

#### B1: `st.set_page_config` called in sub-page (page 2)
- **File:** `pages/2_📈_asset_correlation.py:8`
- **Symptom:** `StreamlitAPIException: set_page_config() can only be called once per app page, and must be called as the first Streamlit command.` When navigating to the Asset Correlation page, the app crashes because `set_page_config` is already called in `Welcome.py`.
- **Reproduction:** Start app, click "Asset Correlation" in sidebar.
- **Fix:** Remove the `st.set_page_config(layout="wide")` call from page 2. The main entrypoint (`Welcome.py`) already sets it.

#### B2: JavaScript syntax error in footer
- **File:** `utils/style.py:113`
- **Symptom:** `pTag.style.color = fontColor.` ends with a dot instead of a semicolon. This causes a JavaScript parse error, potentially breaking the footer's dynamic color adaptation.
- **Reproduction:** Open any page that calls `footer()` (page 1) and inspect browser console for JS errors.
- **Fix:** Replace trailing `.` with `;` on line 113.

---

### MAJOR

#### M1: Duplicated SLIDER_CONFIGS — config file never imported
- **Files:** `config/slider_configs.py`, `pages/1_🎯_risk_return_analysis.py:13-19`
- **Symptom:** `SLIDER_CONFIGS` is defined identically in both files. The `config/` module is never imported anywhere in the codebase. Any future change to one copy will silently diverge from the other.
- **Fix:** Delete the inline copy in page 1 and import from `config.slider_configs`.

#### M2: Unnecessary `sys.path.append` hack
- **File:** `pages/1_🎯_risk_return_analysis.py:9-10`
- **Symptom:** `sys.path.append(os.path.abspath(...))` is used to find `utils` and `config` modules, but Streamlit multipage apps already run from the project root, so this is unnecessary. It also runs *after* the imports that depend on it (lines 1-2 import from `utils`), so it has no effect — the imports work because Streamlit sets CWD to the repo root.
- **Fix:** Remove the `sys.path.append`, `import sys`, and `import os` lines.

#### M3: Malformed HTML comment
- **File:** `pages/1_🎯_risk_return_analysis.py:277`
- **Symptom:** `<!---<p style="font-style: italic; color: #5D6D7E;">Jason Shapiro</p>` uses `<!---` (triple dash) and is never closed. The `</div>` on the next line closes the outer div, but the unclosed comment may cause rendering issues in some browsers.
- **Fix:** Either properly comment it out or remove it entirely.

#### M4: Missing `utils/__init__.py`
- **Files:** `utils/` directory
- **Symptom:** No `__init__.py` in `utils/`. While this works in some configurations (namespace packages), it's fragile and can cause import failures depending on the Python version and execution context.
- **Fix:** Add an empty `utils/__init__.py`.

#### M5: `simulate_trades` runs 10,000 simulations on every widget interaction
- **File:** `pages/1_🎯_risk_return_analysis.py:305`
- **Symptom:** `simulate_trades(win_rate, nb_trades_per_year, risk_per_trade, simulations=10_000)` is called inside `app()` but *outside* the `if st.sidebar.button("Run Simulation")` block. Every time any slider changes, this function re-runs 10,000 Monte Carlo simulations, causing a noticeable delay on page load.
- **Fix:** Either cache this computation with `@st.cache_data` or move it behind the simulation button.

#### M6: Page 2 runs all computation at module level with no caching
- **File:** `pages/2_📈_asset_correlation.py` (entire file)
- **Symptom:** All simulation logic (multivariate normal generation, portfolio construction, metrics computation, correlation sweep) runs at the top level on every widget interaction. With 50 assets and 10 years, this is very slow and blocks the UI.
- **Fix:** Wrap heavy computation in functions and use `@st.cache_data` or a "Run Simulation" button pattern.

#### M7: Unused functions in codebase
- **Files:** `utils/risk_simulation.py:70-95` (`average_trade_progression`), `utils/risk_simulation.py:98-124` (`simulate_portfolio_risk`)
- **Symptom:** These functions are defined but never called anywhere in the app. Dead code adds confusion.
- **Fix:** Remove them or mark them for future use.

#### M8: Page 2 has no footer — inconsistent with page 1
- **File:** `pages/2_📈_asset_correlation.py`
- **Symptom:** Page 1 calls `footer()` but page 2 does not. Inconsistent UX.
- **Fix:** Add footer to page 2 or remove from page 1 (prefer consistency).

#### M9: `pandas==1.5.3` is outdated and potentially incompatible
- **File:** `requirements.txt`
- **Symptom:** pandas 1.5.3 (released 2023) may conflict with newer numpy/streamlit. It's also missing several important bug fixes.
- **Fix:** Update to pandas 2.x (compatible with numpy 1.26.4).

---

### MINOR

#### m1: Win-rate chart annotation x-value mismatch
- **File:** `pages/1_🎯_risk_return_analysis.py:202`
- **Symptom:** The annotation uses `x=f"{win_rate_value}"` but bar x-labels use `f"{rate}%"`. Since the x-axis categorical labels include `%`, the annotation may not align correctly with the intended bar.
- **Fix:** Change to `x=f"{win_rate_value}%"` to match the bar labels.

#### m2: Portfolio log-returns approximation
- **File:** `pages/2_📈_asset_correlation.py:266`
- **Symptom:** `portfolio_returns = log_returns.mean(axis=1)` computes the average of individual asset log-returns as a proxy for portfolio log-returns. This is a first-order approximation — the log-return of an equally-weighted portfolio is not exactly the mean of individual log-returns. For small returns this is fine, but for high volatility/long horizons the error grows.
- **Fix:** Document the approximation or compute exact portfolio returns from price changes.

#### m3: No type hints on core functions
- **Files:** All Python files
- **Symptom:** Functions lack type annotations, reducing IDE support and readability.
- **Fix:** Add type hints to public function signatures.

#### m4: No tests
- **Symptom:** Zero test files in the repository.
- **Fix:** Add pytest tests for `utils/risk_simulation.py` and `utils/style.py`.

#### m5: No linting or formatting configuration
- **Symptom:** No ruff/flake8/black configuration. Code style is inconsistent.
- **Fix:** Add ruff configuration.

#### m6: No CI pipeline
- **Symptom:** No GitHub Actions or other CI configuration.
- **Fix:** Add a workflow for linting and testing.

#### m7: `config/__init__.py` is empty and module is unused
- **File:** `config/__init__.py`
- **Symptom:** The config package exists but is never imported. The `SLIDER_CONFIGS` in it is duplicated inline.
- **Fix:** Make this the single source of truth for config (see M1).

---

## Architecture Notes

### Structure
- **Entrypoint:** `Welcome.py` — Streamlit multipage app entry
- **Pages:** `pages/1_*.py` (risk-return), `pages/2_*.py` (correlation)
- **Utils:** `utils/risk_simulation.py` (TradingSimulator class + unused functions), `utils/style.py` (footer + metric_box)
- **Config:** `config/slider_configs.py` (duplicated, unused)

### Logic vs. UI separation
- Page 1: Partially separated — `TradingSimulator` class is in utils, but chart-building functions and `simulate_trades` live in the page file.
- Page 2: No separation — all logic (matrix generation, simulation, metrics) is inline at module level with UI code.

### Duplication hotspots
1. `SLIDER_CONFIGS` defined twice (config/ and page 1)
2. Chart annotation logic is copy-pasted between `create_bar_chart_figure` and `create_win_rate_vs_return_chart`
3. Color normalization + Viridis scaling is duplicated in both chart functions
4. Metrics calculation and conditional formatting in page 2 is done twice (per-asset and per-correlation)

### Refactoring priorities
1. Extract page 2 simulation logic into `utils/` functions
2. Centralize config and use it everywhere
3. Extract shared chart helpers (color scaling, annotation)
4. Add caching to expensive computations
5. Wrap page 2 in a proper function structure (not module-level execution)
