"""Interactive dashboard for Malaysia EV registrations. Run: streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from msia_ev import analysis as a, data  # noqa: E402

st.set_page_config(page_title="Malaysia EV registrations", layout="wide")


@st.cache_data(show_spinner="Downloading data from data.gov.my (first run only)...")
def load() -> pd.DataFrame:
    return data.load()


df = load()
upto = a.last_full_month(df)
st.title("Malaysia car registrations & EV market")
st.caption(f"Source: data.gov.my. {len(df):,} registrations, "
           f"{df.date_reg.min():%Y-%m-%d} to {df.date_reg.max():%Y-%m-%d}. "
           f"{df.year.max()} is a partial year (Jan-{upto}).")

ev = a.yoy_same_period(df, df["fuel"] == "electric")
tot = a.yoy_same_period(df)
c1, c2, c3 = st.columns(3)
c1.metric(f"BEV registrations, Jan-{upto} {df.year.max()}",
          f"{int(ev.registrations.iloc[-1]):,}", f"{ev.yoy_pct.iloc[-1]:+.0f}% YoY (same period)")
c2.metric("All cars, same period",
          f"{int(tot.registrations.iloc[-1]):,}", f"{tot.yoy_pct.iloc[-1]:+.1f}% YoY")
share = ev.registrations.iloc[-1] / tot.registrations.iloc[-1] * 100
c3.metric("BEV share of registrations", f"{share:.1f}%")

st.subheader("Monthly BEV share (%)")
m = a.monthly_ev_share(df)
st.line_chart(m["ev_share_pct"].rename(lambda p: p.to_timestamp()))

left, right = st.columns(2)
with left:
    st.subheader("BEV registrations by month")
    st.bar_chart(a.monthly_by(df, fuel="electric"))
with right:
    st.subheader("Top models")
    year = st.selectbox("Year", sorted(df.year.unique(), reverse=True))
    fuel = st.selectbox("Fuel", ["electric"] + sorted(set(df.fuel.dropna()) - {"electric"}))
    st.dataframe(a.top_models(df, year=year, fuel=fuel, n=15), hide_index=True, width="stretch")

st.subheader("Explore a maker")
maker = st.selectbox("Maker", df[df.fuel == "electric"].maker.value_counts().index)
st.line_chart(a.monthly_by(df, maker=maker))
