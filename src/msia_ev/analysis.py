"""Reusable analysis helpers. All take the frame returned by `data.load()`."""
import pandas as pd


def monthly_ev_share(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly total registrations, BEV ('electric') count and BEV share (%)."""
    g = df.groupby("period")
    out = pd.DataFrame({
        "total": g.size(),
        "ev": df[df["fuel"] == "electric"].groupby("period").size(),
    }).fillna(0)
    out["ev_share_pct"] = out["ev"] / out["total"] * 100
    out["year"] = out.index.year
    out["month"] = out.index.month
    return out


def last_full_month(df: pd.DataFrame) -> int:
    """Latest month number present in the newest year (data is partial-year)."""
    return int(df.loc[df["year"] == df["year"].max(), "month"].max())


def yoy_same_period(df: pd.DataFrame, mask=None) -> pd.DataFrame:
    """Compare Jan..latest month of the newest year against the same months of earlier years.

    Avoids the partial-year trap of comparing e.g. Jan-Aug 2026 with full-year 2025.
    `mask` optionally restricts rows (e.g. df['fuel'] == 'electric').
    """
    d = df if mask is None else df[mask]
    upto = last_full_month(df)
    d = d[d["month"] <= upto]
    res = d.groupby("year").size().rename("registrations").to_frame()
    res["yoy_pct"] = res["registrations"].pct_change() * 100
    res.attrs["months"] = f"Jan-{upto}"
    return res


def top_models(df: pd.DataFrame, year=None, fuel=None, n: int = 10) -> pd.DataFrame:
    """Top n models by registrations, optionally filtered by year and fuel."""
    d = df
    if year is not None:
        d = d[d["year"] == year]
    if fuel is not None:
        d = d[d["fuel"].isin([fuel] if isinstance(fuel, str) else fuel)]
    return (d.groupby(["maker", "model", "fuel"]).size()
            .rename("registrations").sort_values(ascending=False).head(n).reset_index())


def monthly_by(df: pd.DataFrame, **filters) -> pd.DataFrame:
    """Pivot: rows = month 1-12, cols = year, values = registrations, for given column==value filters."""
    d = df
    for col, val in filters.items():
        d = d[d[col] == val]
    return d.groupby(["month", "year"]).size().unstack("year", fill_value=0)
