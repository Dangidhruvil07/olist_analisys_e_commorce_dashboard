import base64
import math
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG, SURFACE, SURFACE_2, BORDER = "#f4f7f6", "#ffffff", "#eef3f1", "#dce5e1"
TEXT, MUTED, GRID = "#202a32", "#64727c", "#e2e9e6"
BLUE, TEAL, AMBER = "#10b981", "#0f766e", "#f0ad3d"
PINK, PURPLE, RED = "#e879a9", "#8b83d5", "#e05b5b"
SEQ = [TEAL, BLUE, AMBER, PINK, PURPLE, RED]
SCALE = ["#d1fae5", TEAL, BLUE]

_ver = tuple(int(x) for x in st.__version__.split(".")[:2] if x.isdigit())
_header_path = Path(__file__).resolve().parent / "assets" / "header.png"
_header_data = base64.b64encode(_header_path.read_bytes()).decode("ascii") if _header_path.exists() else ""
W = {"width": "stretch"} if _ver >= (1, 50) else {"use_container_width": True}

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, .stApp, [class*="css"] {{ font-family: 'Manrope', sans-serif; }}
.stApp {{ background: radial-gradient(1200px 500px at 85% -10%, #e7f5ef 0%, {BG} 60%); color: {TEXT}; }}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding: 1.4rem 2.2rem 3rem; max-width: 1500px; }}
h1, h2, h3, h4 {{ color: #202a32; letter-spacing: -0.01em; }}

[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #171c24 0%, #101820 100%); border-right: 1px solid #2d3b42; }}
[data-testid="stSidebar"] .stButton > button {{
    justify-content: flex-start; text-align: left; width: 100%;
    background: transparent; border: 1px solid transparent; border-radius: 10px;
    color: #c5d0d5; font-weight: 600; font-size: 14px; min-height: 40px;
    transition: background .15s, color .15s;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: #26343b; color: #ffffff; border-color: #3d5550;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {{
    background: linear-gradient(90deg, rgba(16,185,129,.22), rgba(15,118,110,.18));
    border: 1px solid #285e51; border-left: 3px solid {BLUE}; color: #f2fff9;
}}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption {{ color: #aebdc3 !important; }}
.brand {{ display:flex; align-items:center; gap:12px; padding: 6px 4px 2px; }}
.brand-mark {{
    width:40px; height:40px; border-radius:12px; display:grid; place-items:center; font-size:20px;
    background: linear-gradient(135deg, {BLUE}, {TEAL});
}}
.brand-name {{ font-size:19px; font-weight:800; color:#f3f7f6; line-height:1.1; }}
.brand-tag {{ font-size:12px; color:#aebdc3; }}

.hero {{
    display:flex; justify-content:space-between; align-items:center; gap:20px; flex-wrap:wrap;
    padding: 24px 28px; border-radius: 16px; margin-bottom: 26px; min-height: 138px;
    background: linear-gradient(90deg, rgba(12,20,28,.94) 0%, rgba(12,20,28,.76) 44%, rgba(12,20,28,.24) 100%), url("data:image/jpeg;base64,{_header_data}") center 48% / cover no-repeat, #17232b;
    border: 1px solid #31434b; box-shadow: 0 10px 32px rgba(16,24,32,.18);
}}
.hero h1 {{ margin:0; font-size: 30px; font-weight: 800; color:#f5f8fa; }}
.hero p {{ margin: 4px 0 0; color:#e1e9ec; font-size:14px; }}
.chips {{ display:flex; gap:10px; flex-wrap:wrap; }}
.chip {{
    padding: 7px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 600;
    background: rgba(8,17,23,.66); border: 1px solid rgba(255,255,255,.28); color: #f5f8fa; backdrop-filter: blur(6px);
}}
.chip b {{ color: #6ee7b7; }}

.section {{ margin: 30px 0 12px; }}
.section h3 {{ margin: 0; font-size: 20px; font-weight: 700; }}
.section p {{ margin: 3px 0 0; color: {MUTED}; font-size: 13.5px; }}

.kpi {{
    position: relative; overflow: hidden; height: 100%;
    background: linear-gradient(160deg, {SURFACE_2}, {SURFACE});
    border: 1px solid {BORDER}; border-radius: 14px; padding: 18px 20px 16px;
}}
.kpi::before {{
    content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background: var(--accent);
}}
.kpi-label {{ color:{MUTED}; font-size: 13px; font-weight: 600; }}
.kpi-value {{ color:{TEXT}; font-size: 28px; font-weight: 800; margin: 6px 0 4px;
    font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }}
.kpi-sub {{ color: var(--accent); font-size: 12.5px; font-weight: 600; }}

.insight {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-left: 4px solid var(--accent);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;
}}
.insight h4 {{ margin: 0 0 6px; font-size: 15.5px; font-weight: 700; }}
.insight p {{ margin: 0; color: {MUTED}; font-size: 14px; line-height: 1.55; }}

[data-testid="stPlotlyChart"] {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 14px; padding: 6px 8px;
}}
[data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 12px; overflow: hidden; }}
.stTabs [data-baseweb="tab"] {{ color: {MUTED}; font-weight: 600; }}
.stTabs [aria-selected="true"] {{ color: {TEXT}; }}
[data-testid="stExpander"] {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; }}
hr {{ border-color: {BORDER}; }}
</style>
""",
    unsafe_allow_html=True,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


@st.cache_data(show_spinner="Loading Olist data…")
def load_data():
    read = lambda name: pd.read_csv(RAW_DIR / name)

    orders = read("olist_orders_dataset.csv")
    for col in [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    orders["delivery_days"] = (
                                      orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
                              ).dt.total_seconds() / 86400
    orders["delay_days"] = (
                                   orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
                           ).dt.total_seconds() / 86400

    customers = read("olist_customers_dataset.csv")
    orders = orders.merge(
        customers[["customer_id", "customer_unique_id", "customer_state"]],
        on="customer_id",
        how="left",
    )

    products = read("olist_products_dataset.csv")
    translation = read("product_category_name_translation.csv")
    items = (
        read("olist_order_items_dataset.csv")
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        .merge(translation, on="product_category_name", how="left")
    )
    items["category"] = (
        items["product_category_name_english"]
        .fillna("unknown")
        .str.replace("_", " ")
        .str.title()
    )

    payments = read("olist_order_payments_dataset.csv")
    payments["payment_type"] = (
        payments["payment_type"].fillna("unknown").str.replace("_", " ").str.title()
    )

    return {
        "orders": orders,
        "items": items,
        "payments": payments,
        "reviews": read("olist_order_reviews_dataset.csv"),
        "sellers": read("olist_sellers_dataset.csv"),
        "products": products,
    }


@st.cache_data(show_spinner=False)
def apply_filter(start, end):
    data = load_data()
    o = data["orders"]
    day = o["order_purchase_timestamp"].dt.date
    o = o[(day >= start) & (day <= end)]
    ids = o["order_id"]
    items = data["items"][data["items"]["order_id"].isin(ids)]
    return {
        "orders": o,
        "items": items,
        "payments": data["payments"][data["payments"]["order_id"].isin(ids)],
        "reviews": data["reviews"][data["reviews"]["order_id"].isin(ids)],
        "sellers": data["sellers"][data["sellers"]["seller_id"].isin(items["seller_id"])],
    }


def delivered_frame(o):
    return o[o["order_status"] == "delivered"].dropna(
        subset=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ).copy()


def money(v):
    if v >= 1e6:
        return f"R$ {v / 1e6:.2f}M"
    if v >= 1e3:
        return f"R$ {v / 1e3:.1f}K"
    return f"R$ {v:,.0f}"


def nz(v, default=0.0):
    return default if pd.isna(v) else v


def section(title, sub=""):
    st.markdown(
        f'<div class="section"><h3>{title}</h3>{f"<p>{sub}</p>" if sub else ""}</div>',
        unsafe_allow_html=True,
    )


def kpis(cards):
    """cards: list of (label, value, sub, color)"""
    for col, (label, value, sub, color) in zip(st.columns(len(cards)), cards):
        col.markdown(
            f'<div class="kpi" style="--accent:{color}">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div>',
            unsafe_allow_html=True,
        )


def insight(title, body, color=BLUE):
    return (
        f'<div class="insight" style="--accent:{color}"><h4>{title}</h4><p>{body}</p></div>'
    )


def style(fig, h=380, legend=False):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=h,
        font=dict(family="Manrope, sans-serif", color=TEXT, size=12),
        title=dict(font=dict(size=15, color=TEXT), x=0.01, xanchor="left"),
        margin=dict(l=12, r=12, t=58, b=14),
        showlegend=legend,
        colorway=SEQ,
        hoverlabel=dict(bgcolor="#ffffff", bordercolor=BORDER, font_color=TEXT, font_size=12),
        legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center", title_text=""),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    return fig


def show(fig, h=380, legend=False):
    st.plotly_chart(style(fig, h, legend), theme=None, config={"displayModeBar": False}, **W)


def donut(df, names, values, title, colors=SEQ, h=360):
    fig = px.pie(df, names=names, values=values, hole=0.62, title=title, color_discrete_sequence=colors)
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        marker=dict(line=dict(color=SURFACE, width=3)),
    )
    show(fig, h, legend=True)


def hbar(df, x, y, title, labels=None, scale=SCALE, h=420, text=None):
    fig = px.bar(
        df, x=x, y=y, orientation="h", title=title, labels=labels or {},
        color=x, color_continuous_scale=scale, text=text,
    )
    fig.update_layout(coloraxis_showscale=False, yaxis_title=None)
    fig.update_traces(marker_line_width=0)
    show(fig, h)


def table(df, **kwargs):
    st.dataframe(df, hide_index=True, **W, **kwargs)


def page_overview(D):
    o, it, pay, rev = D["orders"], D["items"], D["payments"], D["reviews"]

    revenue = it["price"].sum()
    order_total = it.groupby("order_id")["price"].sum()
    aov = order_total.mean()
    customer_orders = o.groupby("customer_unique_id")["customer_id"].nunique()
    delivered_pct = (o["order_status"] == "delivered").mean() * 100
    positive = (rev["review_score"] >= 4).mean() * 100

    section("Executive overview", "The headline numbers for the selected period")
    kpis([
        ("Total revenue", money(revenue), "Item prices, excl. freight", TEAL),
        ("Orders", f"{o['order_id'].nunique():,}", f"{delivered_pct:.1f}% delivered", BLUE),
        ("Unique customers", f"{o['customer_unique_id'].nunique():,}",
         f"{(customer_orders > 1).mean() * 100:.1f}% ordered again", PURPLE),
        ("Average order value", f"R$ {nz(aov):,.2f}", "Item prices per order", AMBER),
        ("Review score", f"{nz(rev['review_score'].mean()):.2f} / 5", f"{positive:.0f}% rated 4–5", PINK),
    ])

    m = it.merge(o[["order_id", "order_purchase_timestamp"]], on="order_id", how="left")
    m["month"] = m["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly = m.groupby("month", as_index=False).agg(
        revenue=("price", "sum"), orders=("order_id", "nunique")
    ).sort_values("month")

    monthly = monthly[monthly["orders"] > 1].copy()

    cat = (
        it.groupby("category", as_index=False)
        .agg(price=("price", "sum"), order_id=("order_id", "nunique"))
        .sort_values("price", ascending=False)
    )
    cat = cat.head(10).sort_values("price")

    section("Revenue and product performance")
    left, right = st.columns([1.6, 1])
    with left:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(
            x=monthly["month"], y=monthly["orders"], name="Orders",
            marker_color="rgba(76,141,255,0.28)", secondary_y=True,
        )
        fig.add_scatter(
            x=monthly["month"], y=monthly["revenue"], name="Revenue (R$)",
            mode="lines+markers", line=dict(color=TEAL, width=3), marker=dict(size=6),
            fill="tozeroy", fillcolor="rgba(45,212,176,0.10)", secondary_y=False,
        )
        fig.update_layout(title="Monthly revenue and order volume")
        style(fig, 400, legend=True)
        fig.update_yaxes(showgrid=False, secondary_y=True)
        st.plotly_chart(fig, theme=None, config={"displayModeBar": False}, **W)
    with right:
        hbar(cat, "price", "category", "Top 10 categories by revenue",
             {"price": "Revenue (R$)"}, h=400)

    section("Orders, payments and customers")
    c1, c2, c3 = st.columns(3)
    with c1:
        status = o["order_status"].value_counts().rename_axis("status").reset_index(name="orders")
        donut(status, "status", "orders", "Order status")
    with c2:
        ps = pay.groupby("payment_type", as_index=False)["payment_value"].sum()
        donut(ps, "payment_type", "payment_value", "Payment value by method", [BLUE, AMBER, TEAL, RED, PURPLE])
    with c3:
        customer_type = customer_orders.map(lambda count: "One-time" if count == 1 else "Repeat")
        ct = customer_type.value_counts().rename_axis("type").reset_index(name="customers")
        fig = px.bar(
            ct, x="type", y="customers", color="type", title="One-time vs repeat customers",
            color_discrete_map={"One-time": BLUE, "Repeat": PURPLE},
        )
        fig.update_traces(texttemplate="%{y:,}", textposition="outside", cliponaxis=False)
        show(fig, 360)

    section("When customers buy", "Orders by weekday and hour of purchase")
    t = o.dropna(subset=["order_purchase_timestamp"])
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat = (
        t.groupby([t["order_purchase_timestamp"].dt.day_name(), t["order_purchase_timestamp"].dt.hour])
        .size().unstack(fill_value=0).reindex(days).reindex(columns=range(24)).fillna(0)
    )
    fig = px.imshow(
        heat, aspect="auto", color_continuous_scale=["#e1eee2", BLUE, TEAL, AMBER],
        labels=dict(x="Hour of day", y="", color="Orders"),
    )
    fig.update_layout(title="Purchase activity heatmap")
    show(fig, 340)


def page_delivery(D):
    o = D["orders"].copy()
    d = delivered_frame(o)
    section("Orders and delivery", "Order status, delivery speed and performance against estimates")
    if d.empty:
        st.warning("No delivered orders in the selected period.")
        return

    late = (d["delay_days"] > 0).mean() * 100
    kpis([
        ("Total orders", f"{o['order_id'].nunique():,}", "In selected period", BLUE),
        ("Delivered orders", f"{len(d):,}", "With valid dates", TEAL),
        ("Avg. delivery time", f"{d['delivery_days'].mean():.1f} days",
         f"Median {d['delivery_days'].median():.1f} days", AMBER),
        ("Late delivery rate", f"{late:.1f}%", "Delivered after estimate", RED),
    ])

    d["result"] = d["delay_days"].apply(lambda value: "Late" if value > 0 else "On time / early")
    section("Delivery performance")
    c1, c2 = st.columns(2)
    with c1:
        res = d["result"].value_counts().rename_axis("result").reset_index(name="orders")
        fig = px.pie(
            res, names="result", values="orders", hole=0.62, title="On time / early vs late",
            color="result", color_discrete_map={"On time / early": TEAL, "Late": RED},
        )
        fig.update_traces(textinfo="percent", marker=dict(line=dict(color=SURFACE, width=3)))
        show(fig, 400, legend=True)
    with c2:
        sc = o["order_status"].value_counts().rename_axis("status").reset_index(name="orders")
        fig = px.bar(sc, x="status", y="orders", title="Order status breakdown",
                     color="orders", color_continuous_scale=SCALE)
        fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30, xaxis_title=None)
        show(fig, 400)

    section("Delivery time and trends")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            d[d["delivery_days"] <= 60], x="delivery_days", nbins=45,
            title="How many days do deliveries take?",
            labels={"delivery_days": "Delivery time (days)"}, color_discrete_sequence=[BLUE],
        )
        fig.add_vline(
            x=d["delivery_days"].median(), line_dash="dash", line_color=AMBER,
            annotation_text="Median", annotation_font_color=AMBER,
        )
        fig.update_layout(yaxis_title="Orders", bargap=0.04)
        show(fig, 380)
    with c2:
        d["month"] = d["order_purchase_timestamp"].dt.to_period("M").astype(str)
        trend = d.groupby("month", as_index=False).agg(
            late_rate=("delay_days", lambda values: (values > 0).mean() * 100),
            n=("order_id", "size"),
        )
        trend = trend[trend["n"] >= 50]
        fig = px.line(
            trend, x="month", y="late_rate", markers=True, title="Late delivery rate by month",
            labels={"month": "", "late_rate": "Late deliveries (%)"},
        )
        fig.update_traces(line=dict(color=RED, width=3))
        show(fig, 380)

    state = d.groupby("customer_state", as_index=False).agg(
        avg_days=("delivery_days", "mean"), n=("order_id", "size")
    )
    state = state[state["n"] >= 50].nlargest(12, "avg_days").sort_values("avg_days")
    hbar(state, "avg_days", "customer_state", "Slowest states: average delivery time (days)",
         {"avg_days": "Avg. days", "customer_state": "State"}, scale=[AMBER, RED], h=420)

    section("Delivery table", "Orders delivered 0–60 days after purchase")
    cols = {
        "order_id": "Order ID", "order_purchase_timestamp": "Purchased",
        "order_delivered_customer_date": "Delivered", "order_estimated_delivery_date": "Estimated",
        "delivery_days": "Delivery days", "delay_days": "Vs. estimate (days)",
    }
    base = d[(d["delivery_days"] >= 0) & (d["delivery_days"] <= 60)][list(cols)].rename(columns=cols)
    base = base.round({"Delivery days": 1, "Vs. estimate (days)": 1})
    cfg = {"Vs. estimate (days)": st.column_config.NumberColumn(format="%+.1f")}
    tab1, tab2 = st.tabs(["Earliest vs estimate", "Most delayed"])
    with tab1:
        table(base.sort_values("Vs. estimate (days)").head(10), column_config=cfg)
    with tab2:
        table(base.sort_values("Vs. estimate (days)", ascending=False).head(10), column_config=cfg)
    st.caption("Negative values mean the order arrived earlier than estimated.")


def page_products(D):
    it = D["items"]
    section("Product and category analysis", "Category revenue, demand and pricing")

    cat = it.groupby("category", as_index=False).agg(
        revenue=("price", "sum"),
        items_sold=("order_id", "count"),
        orders=("order_id", "nunique"),
        avg_price=("price", "mean"),
        unique_products=("product_id", "nunique"),
    )
    cat["Avg_sels_values_per_order"] = cat["revenue"] / cat["orders"].replace(0, float("nan"))
    avg_sales = cat["revenue"].mean()
    avg_orders = cat["orders"].mean()

    def category_classfication(row):
        if row["revenue"] > avg_sales and row["orders"] > avg_orders:
            return "High + High"
        elif row["revenue"] < avg_sales and row["orders"] < avg_orders:
            return "Low + Low"
        elif row["revenue"] > avg_sales and row["orders"] < avg_orders:
            return "High + Low"
        else:
            return "Low + High"

    cat["segment"] = cat.apply(category_classfication, axis=1)
    total = cat["revenue"].sum()
    kpis([
        ("Categories", f"{len(cat):,}", "With at least one sale", BLUE),
        ("Unique products", f"{it['product_id'].nunique():,}", "Sold in period", PURPLE),
        ("Items sold", f"{int(cat['items_sold'].sum()):,}", "Order lines", TEAL),
        ("Product revenue", money(total), "Item prices, excl. freight", AMBER),
    ])

    section("Category performance")
    c1, c2 = st.columns([1, 1])
    with c1:
        top = cat.nlargest(10, "revenue").sort_values("revenue")
        hbar(top, "revenue", "category", "Top 10 categories by revenue",
             {"revenue": "Revenue (R$)"}, h=460)
    with c2:
        fig = px.treemap(
            cat.nlargest(20, "revenue"), path=[px.Constant("All categories"), "category"],
            values="revenue", color="avg_price", color_continuous_scale=SCALE,
            title="Revenue share (top 20), colored by average price",
        )
        fig.update_traces(marker=dict(line=dict(color=BG, width=2)), textinfo="label+percent root")
        fig.update_layout(coloraxis_showscale=False)
        show(fig, 460)

    fig = px.scatter(
        cat, x="items_sold", y="revenue", size="unique_products", color="avg_price",
        hover_name="category", title="Demand vs revenue (bubble size = unique products)",
        labels={"items_sold": "Items sold", "revenue": "Revenue (R$)", "avg_price": "Avg. price (R$)"},
        color_continuous_scale=[TEAL, BLUE, PINK], size_max=45,
    )
    show(fig, 460)

    section("Category table")
    tbl = cat.sort_values("revenue", ascending=False).copy()
    tbl["share"] = (tbl["revenue"] / total * 100).clip(lower=0) if total > 0 else 0
    tbl = tbl.rename(columns={
        "category": "Category", "revenue": "Revenue (R$)", "orders": "Unique orders",
        "items_sold": "Items sold", "avg_price": "Avg. price (R$)",
        "unique_products": "Unique products", "share": "Revenue share",
    }).round({"Revenue (R$)": 2, "Avg. price (R$)": 2, "Avg_sels_values_per_order": 2})
    table(tbl[[
        "Category", "Revenue (R$)", "Items sold",
        "Avg. price (R$)", "Unique products", "Revenue share"
    ]], column_config={
        "Revenue share": st.column_config.ProgressColumn(
            format="%.1f%%", min_value=0, max_value=100),
    })


def page_customers(D):
    o = D["orders"].dropna(subset=["customer_unique_id"]).copy()
    section("Customer analysis", "Behavior, repeat purchases and geography")

    cs = o.groupby("customer_unique_id", as_index=False).agg(
        total_orders=("customer_id", "nunique"), state=("customer_state", "first")
    )
    cs["type"] = cs["total_orders"].apply(lambda count: "One-time" if count == 1 else "Repeat")
    n = len(cs)
    repeat = int((cs["type"] == "Repeat").sum())
    kpis([
        ("Unique customers", f"{n:,}", "Distinct people", BLUE),
        ("Repeat customers", f"{repeat:,}", "More than one order", TEAL),
        ("Repeat rate", f"{repeat / n * 100 if n else 0:.1f}%", "Observed in this dataset", AMBER),
        ("Orders per customer", f"{nz(cs['total_orders'].mean()):.2f}", "Average", PURPLE),
    ])

    customer_revenue = o[["customer_id", "customer_unique_id", "order_id"]].merge(
        D["items"][["order_id", "price"]], on="order_id", how="inner"
    ).merge(cs[["customer_unique_id", "type"]], on="customer_unique_id", how="left")
    order_total = customer_revenue.groupby(["order_id", "type"], as_index=False)["price"].sum()

    section("Retention overview")
    c1, c2 = st.columns(2)
    with c1:
        td = cs["type"].value_counts().rename_axis("type").reset_index(name="customers")
        fig = px.pie(
            td, names="type", values="customers", hole=0.62, title="One-time vs repeat customers",
            color="type", color_discrete_map={"One-time": BLUE, "Repeat": TEAL},
        )
        fig.update_traces(textinfo="percent", marker=dict(line=dict(color=SURFACE, width=3)))
        show(fig, 400, legend=True)
    with c2:
        fq = cs["total_orders"].clip(upper=5).map(lambda value: "5+" if value >= 5 else str(value))
        fq = fq.value_counts().reindex(["1", "2", "3", "4", "5+"]).fillna(0).reset_index()
        fq.columns = ["orders", "customers"]
        fig = px.bar(
            fq, x="orders", y="customers", title="Customers by number of orders", text="customers",
            color="customers", color_continuous_scale=SCALE,
            labels={"orders": "Orders per customer", "customers": "Customers"},
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        show(fig, 400)

    section("Where customers live")
    st_data = cs.groupby("state", as_index=False).agg(
        customers=("customer_unique_id", "nunique")
    ).nlargest(10, "customers").sort_values("customers")
    hbar(st_data, "customers", "state", "Top 10 states by customers",
         {"customers": "Unique customers", "state": "State"}, h=440)

    section("Customer table", "Customers with the most orders")
    t = cs.sort_values(["total_orders", "state"], ascending=[False, True]).head(20)
    customer_table = t[["customer_unique_id", "state", "total_orders", "type"]].rename(columns={
        "customer_unique_id": "Customer ID", "state": "State",
        "total_orders": "Total orders", "type": "Customer type",
    })
    table(customer_table)


def page_sellers(D):
    it, sellers = D["items"], D["sellers"]
    section("Seller performance", "Revenue, order volume and seller location")

    seller_orders = it[["seller_id", "order_id"]].drop_duplicates()
    sd = seller_orders.groupby("seller_id", as_index=False).agg(
        orders=("order_id", "nunique")
    )
    revenue = it.groupby("seller_id", as_index=False)["price"].sum().rename(columns={"price": "revenue"})
    item_count = it.groupby("seller_id", as_index=False)["order_id"].count().rename(columns={"order_id": "items"})
    sd = sd.merge(revenue, on="seller_id", how="left").merge(item_count, on="seller_id", how="left")
    delivery = delivered_frame(D["orders"])[["order_id", "delivery_days"]]
    seller_delivery = seller_orders.merge(delivery, on="order_id", how="left")
    seller_avg_delivery = seller_delivery.groupby("seller_id", as_index=False)["delivery_days"].mean()
    sd = sd.merge(seller_avg_delivery, on="seller_id", how="left")
    sd = sd.merge(sellers, on="seller_id", how="left")
    sd["city"] = sd["seller_city"].fillna("Unknown").str.title()
    sd["state"] = sd["seller_state"].fillna("N/A").str.upper()
    sd["label"] = sd["city"] + ", " + sd["state"] + " · " + sd["seller_id"].str[-6:]

    ranked = sd.sort_values("revenue", ascending=False)
    k = max(1, math.ceil(len(ranked) * 0.10))
    top_share = ranked["revenue"].head(k).sum() / ranked["revenue"].sum() * 100 if len(ranked) and ranked[
        "revenue"].sum() else 0

    kpis([
        ("Active sellers", f"{len(sd):,}", "With sales in period", BLUE),
        ("Seller revenue", money(sd["revenue"].sum()), "Item prices", TEAL),
        ("Avg. revenue per seller", f"R$ {nz(sd['revenue'].mean()):,.0f}", "Mean", AMBER),
        ("Top 10% of sellers", f"{top_share:.0f}%", "Share of revenue", PINK),
    ])

    section("Top 10 sellers")
    c1, c2 = st.columns(2)
    with c1:
        t = sd.nlargest(10, "revenue").sort_values("revenue")
        hbar(t, "revenue", "label", "By revenue", {"revenue": "Revenue (R$)", "label": ""}, h=460)
    with c2:
        t = sd.nlargest(10, "orders").sort_values("orders")
        hbar(t, "orders", "label", "By order volume", {"orders": "Unique orders", "label": ""},
             scale=["#e8e2f5", PURPLE, BLUE], h=460)

    section("Revenue by seller state")
    ss = sd.groupby("state", as_index=False).agg(
        revenue=("revenue", "sum"), sellers=("seller_id", "nunique")
    ).nlargest(10, "revenue").sort_values("revenue")
    hbar(ss, "revenue", "state", "Top 10 seller states by revenue",
         {"revenue": "Revenue (R$)", "state": ""}, h=420)

    section("Seller table", "Top 20 sellers by revenue")
    tbl = ranked.head(20).rename(columns={
        "seller_id": "Seller ID", "city": "City", "state": "State",
        "revenue": "Revenue (R$)", "orders": "Unique orders", "items": "Items sold",
    })
    tbl["Revenue (R$)"] = tbl["Revenue (R$)"].round(2)
    table(tbl[["Seller ID", "City", "State", "Revenue (R$)", "Unique orders", "Items sold"]])


def page_payments(D):
    p = D["payments"].copy()
    p["payment_value"] = pd.to_numeric(p["payment_value"], errors="coerce")
    p["payment_installments"] = pd.to_numeric(p["payment_installments"], errors="coerce")
    p = p.dropna(subset=["payment_value"])

    section("Payment analysis", "Methods, transaction value and installment behavior")
    kpis([
        ("Total payment value", money(p["payment_value"].sum()), "Includes freight", TEAL),
        ("Payment records", f"{len(p):,}", "Transactions", BLUE),
        ("Average payment", f"R$ {nz(p['payment_value'].mean()):,.2f}", "Per record", AMBER),
        ("Avg. installments", f"{nz(p['payment_installments'].mean()):.1f}", "Per record", PURPLE),
    ])

    summary = p.groupby("payment_type", as_index=False).agg(
        value=("payment_value", "sum"),
        records=("payment_value", "size"),
        avg=("payment_value", "mean"),
        installments=("payment_installments", "mean"),
    ).sort_values("value", ascending=False)
    total_payment_amount = p["payment_value"].sum()
    summary["share"] = summary["value"] / total_payment_amount * 100 if total_payment_amount else 0

    section("Payment methods")
    c1, c2 = st.columns(2)
    with c1:
        hbar(summary.sort_values("value"), "value", "payment_type", "Payment value by method",
             {"value": "Payment value (R$)", "payment_type": ""}, h=400)
    with c2:
        donut(summary, "payment_type", "value", "Share of payment value", h=400)

    section("Installments")
    inst = p.dropna(subset=["payment_installments"]).groupby(
        "payment_installments", as_index=False
    ).agg(records=("payment_value", "size"), value=("payment_value", "mean"))
    inst = inst[inst["payment_installments"] >= 1]
    fig = px.bar(
        inst, x="payment_installments", y="records", title="Payment records by number of installments",
        labels={"payment_installments": "Installments", "records": "Payment records"},
        color="records", color_continuous_scale=SCALE,
    )
    fig.update_layout(coloraxis_showscale=False)
    show(fig, 400)

    section("Payment summary")
    t = summary.rename(columns={
        "payment_type": "Payment method", "value": "Total value (R$)", "records": "Records",
        "avg": "Average payment (R$)", "installments": "Avg. installments", "share": "Payment share (%)",
    }).round(2)
    table(t)


def page_geo(D):
    o, it, sellers = D["orders"], D["items"], D["sellers"]
    section("Geographic analysis", "Where customers and sellers are across Brazil")

    customer_state_count = o["customer_state"].value_counts().sort_values(ascending=False)
    customer_state_per = customer_state_count / customer_state_count.sum() * 100
    orders_customers_order_items = o[["customer_id", "customer_state", "order_id"]].merge(
        it[["order_id", "price"]], on="order_id", how="inner"
    )
    state_revenue = orders_customers_order_items.groupby("customer_state")["price"].sum()
    revenue_share = state_revenue / state_revenue.sum() * 100 if state_revenue.sum() else state_revenue
    state_comparison = pd.DataFrame({
        "customer_share": customer_state_per,
        "revenue_share": revenue_share,
    }).fillna(0)
    state_comparison["difference"] = state_comparison["revenue_share"] - state_comparison["customer_share"]
    state_comparison = state_comparison.sort_values("difference", ascending=False)
    state_aov = orders_customers_order_items.groupby("customer_state").agg(
        total_revenue=("price", "sum"), unique_order=("order_id", "nunique")
    ).reset_index()
    state_aov["Aov"] = state_aov["total_revenue"] / state_aov["unique_order"]
    revenue_per_customer = (
            state_revenue / customer_state_count
    ).sort_values(ascending=False).reset_index()
    revenue_per_customer.columns = ["State", "Revenue per Customer"]

    sg = sellers.groupby("seller_state", as_index=False).agg(sellers=("seller_id", "nunique"))
    sg.columns = ["state", "sellers"]
    cg = customer_state_count.rename_axis("state").reset_index(name="customers")
    both = cg.merge(sg, on="state", how="outer").fillna(0)

    kpis([
        ("Unique customers", f"{o['customer_unique_id'].nunique():,}", "In period", BLUE),
        ("Active sellers", f"{sellers['seller_id'].nunique():,}", "In period", TEAL),
        ("Customer states", f"{customer_state_count.index.nunique():,}", "Across Brazil", AMBER),
        ("Seller cities", f"{sellers['seller_city'].nunique():,}", "Distinct cities", PURPLE),
    ])

    section("Top states")
    c1, c2 = st.columns(2)
    with c1:
        hbar(cg.nlargest(10, "customers").sort_values("customers"), "customers", "state",
             "Top 10 states by customers", {"customers": "Unique customers", "state": ""}, h=440)
    with c2:
        hbar(sg.nlargest(10, "sellers").sort_values("sellers"), "sellers", "state",
             "Top 10 states by sellers", {"sellers": "Unique sellers", "state": ""},
             scale=["#e8e2f5", PURPLE, BLUE], h=440)

    section("Demand vs supply", "Customers and sellers in the 15 largest customer states")
    top = both.nlargest(15, "customers").melt(
        id_vars="state", value_vars=["customers", "sellers"], var_name="entity", value_name="count"
    )
    top["entity"] = top["entity"].str.title()
    fig = px.bar(
        top, x="state", y="count", color="entity", barmode="group",
        title="Customers vs sellers by state",
        color_discrete_map={"Customers": BLUE, "Sellers": TEAL},
        labels={"state": "State", "count": "Count"},
    )
    show(fig, 420, legend=True)

    section("Revenue and market concentration")
    c1, c2 = st.columns(2)
    with c1:
        rs = (
            orders_customers_order_items.groupby("customer_state", as_index=False)["price"].sum()
            .nlargest(10, "price").sort_values("price")
        )
        hbar(rs, "price", "customer_state", "Revenue by customer state",
             {"price": "Revenue (R$)", "customer_state": ""}, scale=[AMBER, PINK], h=460)
    with c2:
        fig = px.treemap(
            cg[cg["customers"] > 0], path=[px.Constant("Brazil"), "state"], values="customers",
            color="customers", color_continuous_scale=SCALE, title="Customer share by state",
        )
        fig.update_traces(
            texttemplate="%{label}<br>%{value:,}<br>%{percentRoot:.1%}",
            marker=dict(line=dict(color=BG, width=2)),
        )
        fig.update_layout(coloraxis_showscale=False)
        show(fig, 460)


def page_reviews(D):
    rev = D["reviews"].copy()
    rev["review_score"] = pd.to_numeric(rev["review_score"], errors="coerce")
    rev = rev.dropna(subset=["review_score"])
    section("Reviews and satisfaction", "Scores, patterns and customer feedback")
    if rev.empty:
        st.warning("No reviews in the selected period.")
        return

    n = len(rev)
    kpis([
        ("Total reviews", f"{n:,}", "Scored reviews", BLUE),
        ("Average score", f"{rev['review_score'].mean():.2f} / 5", "Mean rating", AMBER),
        ("Positive (4–5)", f"{(rev['review_score'] >= 4).mean() * 100:.1f}%", "Happy customers", TEAL),
        ("Low (1–2)", f"{(rev['review_score'] <= 2).mean() * 100:.1f}%", "Needs attention", RED),
    ])

    dist = rev["review_score"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).rename_axis(
        "score"
    ).reset_index(name="count")
    dist["label"] = dist["score"].astype(int).astype(str) + " star"
    cmap = {"1 star": RED, "2 star": AMBER, "3 star": PURPLE, "4 star": BLUE, "5 star": TEAL}

    section("Score distribution")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig = px.bar(
            dist, x="label", y="count", text="count", color="label", color_discrete_map=cmap,
            title="Reviews by score", labels={"label": "", "count": "Reviews"},
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
        show(fig, 400)
    with c2:
        fig = px.pie(
            dist, names="label", values="count", hole=0.62, title="Share of reviews",
            color="label", color_discrete_map=cmap,
        )
        fig.update_traces(textinfo="percent", marker=dict(line=dict(color=SURFACE, width=3)))
        show(fig, 400, legend=True)

    d = delivered_frame(D["orders"])
    if not d.empty:
        section("Delivery vs satisfaction", "Average review score by how late the order arrived")
        delivery_dates = D["orders"][[
            "order_id", "order_delivered_customer_date", "order_estimated_delivery_date"
        ]].copy()
        delivery_dates["delivery_status"] = delivery_dates.apply(
            lambda row: "On Time" if row["order_delivered_customer_date"] <= row[
                "order_estimated_delivery_date"] else "Late",
            axis=1,
        )
        review_delivery = rev.merge(
            delivery_dates[["order_id", "delivery_status"]], on="order_id", how="inner"
        )
        if not review_delivery.empty:
            b = review_delivery.groupby("delivery_status").agg(
                score=("review_score", "mean"), reviews=("review_score", "size")
            ).reset_index()
            fig = px.bar(
                b, x="delivery_status", y="score", text=b["score"].round(2), title="Late deliveries hurt ratings",
                color="score", color_continuous_scale=[RED, AMBER, TEAL],
                labels={"delivery_status": "", "score": "Average review score"}, hover_data={"reviews": ":,"},
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(coloraxis_showscale=False, yaxis_range=[0, 5.3])
            show(fig, 380)

    section("Low-scoring reviews", "Most recent reviews rated 1–2 stars")
    low = rev[rev["review_score"] <= 2].merge(
        D["orders"][["order_id", "order_status", "order_purchase_timestamp"]], on="order_id", how="left"
    )
    cols = ["order_id", "review_score", "order_status", "order_purchase_timestamp"]
    if "review_comment_message" in low.columns:
        low["review_comment_message"] = low["review_comment_message"].fillna("")
        low = low[low["review_comment_message"] != ""]
        cols.append("review_comment_message")
    low = low.sort_values("order_purchase_timestamp", ascending=False).head(20)
    table(low[cols].rename(columns={
        "order_id": "Order ID", "review_score": "Score", "order_status": "Status",
        "order_purchase_timestamp": "Purchased", "review_comment_message": "Customer comment",
    }))


def page_insights(D):
    o, it, pay, rev, sellers = D["orders"], D["items"], D["payments"], D["reviews"], D["sellers"]
    section("Business insights", "Findings, risks and recommended next steps, calculated from the selected period")

    revenue = it["price"].sum()
    customer_orders = o.dropna(subset=["customer_unique_id"]).groupby("customer_unique_id")["customer_id"].nunique()
    repeat = (customer_orders > 1).mean() * 100 if len(customer_orders) else 0
    d = delivered_frame(o)
    late = (d["delay_days"] > 0).mean() * 100 if len(d) else 0
    median_delay = nz(d["delay_days"].median()) if len(d) else 0

    kpis([
        ("Product revenue", money(revenue), "Item prices, excl. freight", TEAL),
        ("Total orders", f"{o['order_id'].nunique():,}", "In period", BLUE),
        ("Late delivery rate", f"{late:.1f}%", "Delivered after estimate", RED),
        ("Repeat customers", f"{repeat:.1f}%", "Placed 2+ orders", AMBER),
    ])

    category_revenue = it.groupby("category", as_index=False).agg(
        price=("price", "sum"), order_id=("order_id", "nunique")
    )
    category_revenue["avg_revenue_per_order"] = (
            category_revenue["price"] / category_revenue["order_id"].replace(0, float("nan"))
    )
    avg_sales = category_revenue["price"].mean()
    avg_orders = category_revenue["order_id"].mean()

    def category_classfication(row):
        if row["price"] > avg_sales and row["order_id"] > avg_orders:
            return "High + High"
        elif row["price"] < avg_sales and row["order_id"] < avg_orders:
            return "Low + Low"
        elif row["price"] > avg_sales and row["order_id"] < avg_orders:
            return "High + Low"
        else:
            return "Low + High"

    category_revenue["segment"] = category_revenue.apply(category_classfication, axis=1)
    cat = category_revenue.sort_values("price", ascending=False)
    top_cat = cat.iloc[0]["category"] if len(cat) else "n/a"
    top_cat_share = cat.iloc[0]["price"] / cat["price"].sum() * 100 if len(cat) and cat["price"].sum() else 0
    top5_share = cat.head(5)["price"].sum() / cat["price"].sum() * 100 if len(cat) and cat["price"].sum() else 0

    ps = pay.groupby("payment_type")["payment_value"].sum().sort_values(ascending=False)
    top_pay = ps.index[0] if len(ps) else "n/a"
    top_pay_share = ps.iloc[0] / ps.sum() * 100 if len(ps) and ps.sum() else 0

    sc = o.groupby("customer_state")["customer_unique_id"].nunique().sort_values(ascending=False)
    top_state = sc.index[0] if len(sc) else "n/a"
    top_state_share = sc.iloc[0] / sc.sum() * 100 if len(sc) and sc.sum() else 0

    seller_revenue = it.groupby("seller_id")["price"].sum().sort_values(ascending=False)
    k = max(1, math.ceil(len(seller_revenue) * 0.10))
    seller_share = seller_revenue.head(k).sum() / seller_revenue.sum() * 100 if len(
        seller_revenue) and seller_revenue.sum() else 0

    review_delivery = rev.merge(d[["order_id", "delay_days"]], on="order_id", how="inner") if len(d) else pd.DataFrame()
    score_late = review_delivery.loc[
        review_delivery["delay_days"] > 0, "review_score"].mean() if not review_delivery.empty else float("nan")
    score_ok = review_delivery.loc[
        review_delivery["delay_days"] <= 0, "review_score"].mean() if not review_delivery.empty else float("nan")

    cards = [
        insight("Retention is the biggest opportunity",
                f"Only {repeat:.1f}% of customers placed a second order. Many products are bought rarely, "
                "so this is not proof of a poor experience, but it shows how much growth depends on "
                "acquiring new customers.", RED if repeat < 10 else AMBER),
        insight("Late deliveries cost reviews",
                f"{late:.1f}% of orders arrive after the estimate (median {median_delay:+.1f} days vs estimate). "
                f"Late orders average {nz(score_late):.2f} stars against {nz(score_ok):.2f} for on-time orders.",
                RED if late > 10 else AMBER),
        insight(f"{top_cat} leads on revenue",
                f"It brings in {top_cat_share:.1f}% of item revenue, and the top 5 categories together "
                f"account for {top5_share:.1f}%.", TEAL),
        insight("A few sellers drive most sales",
                f"The top 10% of sellers generate {seller_share:.0f}% of revenue. Losing one of them would "
                "be felt across the marketplace.", AMBER),
        insight(f"{top_state} dominates demand",
                f"{top_state_share:.1f}% of customers live in {top_state}. Other regions are under-served "
                "and are where delivery speed matters most.", BLUE),
        insight(f"{top_pay} is the preferred payment method",
                f"It carries {top_pay_share:.1f}% of payment value, so checkout reliability for this "
                "method is critical.", PURPLE),
    ]
    section("Key findings")
    left, right = st.columns(2)
    for i, c in enumerate(cards):
        (left if i % 2 == 0 else right).markdown(c, unsafe_allow_html=True)

    section("Recommended actions")
    a1, a2 = st.columns(2)
    with a1:
        st.markdown(insight("Win back customers",
                            "Analyze repeat purchases by category, study the time to a second order, and test "
                            "targeted offers and recommendations while measuring the results.", TEAL),
                    unsafe_allow_html=True)
    with a2:
        st.markdown(insight("Fix delivery promises",
                            "Review estimates in the slowest states, work with carriers and sellers that cause "
                            "delays, and track the link between delay and review score every month.", AMBER),
                    unsafe_allow_html=True)

    top = cat.head(10).sort_values("price")
    hbar(top, "price", "category", "Top 10 categories by item revenue", {"price": "Item revenue (R$)"}, h=450)

    with st.expander("Metric definitions and limitations"):
        st.markdown(
            "- **Repeat customers:** share of unique customers with more than one recorded order.\n"
            "- **Late delivery rate:** share of delivered orders that arrived after the estimated date.\n"
            "- **Revenue:** sum of item prices. It excludes freight and is not profit.\n"
            "- **Top 10% of sellers:** their combined share of item revenue."
        )
        st.caption(
            "These are historical observations, not proof of causation. Repeat share is not a formal "
            "cohort retention rate, and the data cannot explain why a customer did not return."
        )


PAGES = {
    "Overview": ("⌂", page_overview),
    "Orders & Delivery": ("▣", page_delivery),
    "Product & Category": ("◇", page_products),
    "Customer Analysis": ("♙", page_customers),
    "Seller Analysis": ("▤", page_sellers),
    "Payment Analysis": ("▱", page_payments),
    "Geographic Analysis": ("◎", page_geo),
    "Review Analysis": ("☆", page_reviews),
    "Business Insights": ("✧", page_insights),
}

try:
    data = load_data()
except FileNotFoundError as e:
    st.error(f"CSV file not found: {e}. Expected the Olist files in {RAW_DIR}.")
    st.stop()

purchase = data["orders"]["order_purchase_timestamp"].dropna()
min_d, max_d = purchase.min().date(), purchase.max().date()

if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"

with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">🛒</div><div>'
        '<div class="brand-name">Olist Analytics</div>'
        '<div class="brand-tag">Brazilian e-commerce</div></div></div>',
        unsafe_allow_html=True,
    )
    st.divider()

    for name, (icon, _) in PAGES.items():
        if st.button(
                f"{icon}   {name}",
                key=f"nav_{name}",
                type="primary" if st.session_state.active_page == name else "secondary",
                **W,
        ):
            st.session_state.active_page = name

    st.divider()
    picked = st.date_input(
        "Purchase period", value=(min_d, max_d), min_value=min_d, max_value=max_d,
        help="Filters every page by the order purchase date.",
    )
    st.caption("Source: Olist public dataset")

if isinstance(picked, (tuple, list)):
    start = picked[0]
    end = picked[1] if len(picked) > 1 else max_d
else:
    start, end = picked, max_d

page = st.session_state.active_page
filtered = apply_filter(start, end)

st.markdown(
    f"""
<div class="hero">
  <div>
    <h1>{page}</h1>
    <p>Data-driven insights for a Brazilian e-commerce marketplace</p>
  </div>
  <div class="chips">
    <span class="chip">{start:%d %b %Y} to {end:%d %b %Y}</span>
    <span class="chip"><b>{filtered['orders']['order_id'].nunique():,}</b> orders</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

if filtered["orders"].empty:
    st.warning("No orders in this period. Choose a wider date range in the sidebar.")
    st.stop()

try:
    PAGES[page][1](filtered)
except KeyError as e:
    st.error(f"Expected column missing from CSV: {e}")