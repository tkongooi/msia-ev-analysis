# Malaysia EV car registrations (2024-2026)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tkongooi/msia-ev-analysis/blob/main/notebooks/01_ev_analysis.ipynb)

Analysis of Malaysian car registrations from [data.gov.my](https://data.gov.my) (`cars_YYYY.parquet`, ~2.3M rows, one row per registered car), focused on the EV market: monthly BEV share, top EV makers/models, Proton e.MAS and BYD trends, hybrids.

Ported from a Google Colab notebook (kept as `notebooks/00_original_colab.ipynb`).

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/01_ev_analysis.ipynb
```
Data downloads once into `data/` (gitignored). Pass `refresh=True` to `data.load()` to re-download.

## Dashboard
```bash
pip install streamlit
streamlit run app/streamlit_app.py
```
Or deploy free on [Streamlit Community Cloud](https://share.streamlit.io) (main file: `app/streamlit_app.py`).

## Published notebook
A GitHub Actions workflow (`.github/workflows/pages.yml`) renders the notebook to HTML and deploys it to GitHub Pages.
Enable it under Settings > Pages > Source: GitHub Actions. (Private repos need a paid GitHub plan for Pages.)

## Layout
- `app/streamlit_app.py` - interactive dashboard
- `src/msia_ev/data.py` - download, cache, clean
- `src/msia_ev/analysis.py` - `monthly_ev_share`, `yoy_same_period`, `top_models`, `monthly_by`
- `notebooks/01_ev_analysis.ipynb` - the analysis (outputs included, renders on GitHub)

## Fixes vs. the original notebook
- Monthly grouping no longer pools month numbers across years.
- YoY is **same-period** (Jan to latest month). The original compared full-year 2025 to partial 2026 and reported +6%; like-for-like BEV registrations are about +103% (Jan-Aug 2026 vs Jan-Aug 2025).
- Per-year copy-paste replaced by one frame with `year`/`month`/`period` columns; model/maker whitespace cleaned once.
- Dropped the `google.colab.ai` cell and the guessed-PHEV list (the data cannot separate HEV/PHEV/EREV).

## Caveats
- 2026 is a partial year (data to 2026-08-31).
- Proton e.MAS 7 appears as both `electric` and `hybrid_petrol` from Feb 2026, likely an EREV variant; no variant column exists to confirm. BEV-only e.MAS 7 counts are a lower bound.
