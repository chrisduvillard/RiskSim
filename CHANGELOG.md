# Changelog

## [1.1.0] - 2026-02-19

### Audit & Documentation
- Added `docs/audit_report.md` with full codebase audit (blockers, majors, minors)
- Added `CHANGELOG.md`
- Improved `README.md` with setup, run, test, and lint instructions

### Bug Fixes (Blockers)
- **Removed duplicate `st.set_page_config`** from Asset Correlation page — previously crashed on navigation
- **Fixed JavaScript syntax error** in `utils/style.py` footer (trailing `.` replaced with `;`)

### Bug Fixes (Majors)
- **Removed duplicated `SLIDER_CONFIGS`** from page 1; now imports from `config.slider_configs`
- **Removed unnecessary `sys.path.append` hack** from page 1
- **Fixed malformed HTML comment** (unclosed `<!---`) in page 1
- **Added missing `utils/__init__.py`** for reliable imports
- **Cached `simulate_drawdown`** so it doesn't rerun 10,000 simulations on every slider change
- **Restructured Asset Correlation page** — wrapped all logic in functions, added "Run Simulation" button to avoid recomputing on every widget interaction
- **Removed unused functions** (`average_trade_progression`, `simulate_portfolio_risk`) from `risk_simulation.py`
- **Added footer to page 2** for consistency with page 1
- **Updated pandas** from 1.5.3 to 2.x (compatible with modern numpy/Python)

### Bug Fixes (Minors)
- **Fixed win-rate chart annotation** x-value mismatch (was `f"{value}"`, now `f"{value}%"` to match bar labels)

### Refactoring
- Extracted `_viridis_colors` and `_add_expected_return_annotation` shared helpers in page 1
- Extracted `simulate_portfolio`, `calculate_metrics`, `style_metrics_table` in page 2
- Moved drawdown simulation to `utils/risk_simulation.py` as `simulate_drawdown`
- Added type hints throughout `risk_simulation.py`
- Reduced metric display duplication with loop pattern

### Tooling & CI
- Added `pyproject.toml` with ruff and pytest configuration
- Added `tests/` with 19 tests covering `TradingSimulator`, `simulate_drawdown`, and `metric_box`
- Added `.github/workflows/ci.yml` running ruff + pytest on Python 3.10 and 3.12
- Updated `requirements.txt` to use flexible version ranges for Python 3.10-3.13 compatibility

### Verification Notes

```bash
# Run the app
streamlit run Welcome.py

# Run tests
pytest -v

# Run linter
ruff check .
```
