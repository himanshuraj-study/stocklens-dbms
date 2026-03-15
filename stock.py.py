import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="StockLens DBMS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  — dark financial dashboard
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0e1a !important;
    color: #e2e8f0 !important;
}

#  Hide default streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f1629 !important;
    border-right: 1px solid #1e2d4a;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* Sidebar logo area */
.sidebar-logo {
    font-family: 'Space Mono', monospace;
    font-size: 1.35rem;
    font-weight: 700;
    color: #38bdf8 !important;
    letter-spacing: -0.5px;
    padding: 0.5rem 0 1.5rem;
    border-bottom: 1px solid #1e2d4a;
    margin-bottom: 1.2rem;
}
.sidebar-logo span { color: #818cf8 !important; }

/* Radio buttons in sidebar */
div[role="radiogroup"] label {
    background: transparent !important;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.5rem 0.75rem !important;
    margin-bottom: 4px;
    transition: all 0.2s;
    font-size: 0.88rem !important;
    color: #94a3b8 !important;
}
div[role="radiogroup"] label:hover {
    background: #1e2d4a !important;
    color: #e2e8f0 !important;
    border-color: #334155;
}
div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(90deg, #1e3a5f, #1e2d4a) !important;
    color: #38bdf8 !important;
    border-color: #38bdf8 !important;
}

/* ── Page title ── */
.page-header {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -1px;
    margin-bottom: 0.25rem;
}
.page-subtitle {
    font-size: 0.82rem;
    color: #64748b;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Cards / form containers ── */
.card {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}
.card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 1.2rem;
}

/* ── Inputs ── */
input, textarea, select, .stTextInput input, .stNumberInput input {
    background: #0f1629 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
input:focus, .stTextInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.12) !important;
}

/* ── Primary Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #818cf8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.75rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Danger button (delete) ── */
.danger-btn .stButton > button {
    background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #0f1629 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── DataFrames / Tables ── */
.stDataFrame, .stTable {
    background: #111827 !important;
    border-radius: 12px !important;
    border: 1px solid #1e2d4a !important;
    overflow: hidden !important;
}
.stDataFrame thead tr th {
    background: #0f1629 !important;
    color: #38bdf8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.stDataFrame tbody tr td { color: #cbd5e1 !important; }
.stDataFrame tbody tr:hover td { background: #1e2d4a !important; }

/* ── Success / Warning / Error ── */
.stAlert { border-radius: 10px !important; border: none !important; }

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 150px;
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
}
.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #64748b;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
}
.metric-value.green { color: #34d399; }
.metric-value.blue  { color: #38bdf8; }
.metric-value.purple{ color: #a78bfa; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="stock_market_v2"
    )

conn = get_connection()
cursor = conn.cursor()

# ─────────────────────────────────────────────
#  MATPLOTLIB DARK THEME
# ─────────────────────────────────────────────
def apply_chart_style(ax, fig):
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#0a0e1a")
    ax.tick_params(colors="#64748b", labelsize=9)
    ax.xaxis.label.set_color("#94a3b8")
    ax.yaxis.label.set_color("#94a3b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e2d4a")
    ax.grid(color="#1e2d4a", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    plt.xticks(rotation=35, ha="right")

COLORS = ["#38bdf8", "#818cf8", "#34d399", "#fb923c", "#f472b6"]

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">Stock<span>Lens</span> ↗</div>', unsafe_allow_html=True)
    menu = st.radio(
        "",
        [
            "🏠  Dashboard",
            "🏢  Add Company",
            "📌  Add Stock",
            "💹  Add Daily Price",
            "📋  View Data",
            "📊  Analytics",
            "⚖️  Compare Stocks",
            "📈  Price Trends",
            "🗑️  Delete Stock",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown('<p style="font-size:0.72rem;color:#334155;text-align:center;">DBMS Mini Project · 2025</p>', unsafe_allow_html=True)

# strip the emoji prefix for logic checks
page = menu.split("  ", 1)[-1].strip()

# ─────────────────────────────────────────────
#  HELPER: section header
# ─────────────────────────────────────────────
def page_header(title, subtitle=""):
    st.markdown(f'<div class="page-header">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DASHBOARD (home)
# ─────────────────────────────────────────────
if page == "Dashboard":
    page_header("Market Overview", "Real-time snapshot of your database")

    # Quick counts
    cursor.execute("SELECT COUNT(*) FROM Company")
    num_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Stock")
    num_stocks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Daily_Price")
    num_prices = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(close_price) FROM Daily_Price")
    max_price = cursor.fetchone()[0] or 0

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">Companies</div>
            <div class="metric-value blue">{num_companies}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Stocks Listed</div>
            <div class="metric-value purple">{num_stocks}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Price Records</div>
            <div class="metric-value">{num_prices}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">All-Time High</div>
            <div class="metric-value green">₹{max_price:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recent records table
    st.markdown('<div class="card"><div class="card-title">Recent Trades</div>', unsafe_allow_html=True)
    cursor.execute("""
        SELECT s.symbol, d.trade_date, d.open_price, d.close_price, d.high_price, d.low_price, d.volume
        FROM Stock s JOIN Daily_Price d ON s.stock_id = d.stock_id
        ORDER BY d.trade_date DESC LIMIT 10
    """)
    rows = cursor.fetchall()
    if rows:
        df_recent = pd.DataFrame(rows, columns=["Symbol", "Date", "Open", "Close", "High", "Low", "Volume"])
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("No trade data yet. Add some daily prices to get started.")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADD COMPANY
# ─────────────────────────────────────────────
elif page == "Add Company":
    page_header("Add Company", "Register a new listed company")

    st.markdown('<div class="card"><div class="card-title">Company Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Company Name", placeholder="e.g. Reliance Industries")
    with col2:
        sector = st.text_input("Sector", placeholder="e.g. Energy")

    if st.button("➕  Insert Company"):
        if name and sector:
            cursor.execute(
                "INSERT INTO Company (company_name, sector) VALUES (%s,%s)",
                (name, sector)
            )
            conn.commit()
            st.success(f"✅ **{name}** added to the database.")
        else:
            st.warning("Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADD STOCK
# ─────────────────────────────────────────────
elif page == "Add Stock":
    page_header("Add Stock", "List a stock symbol for a company")

    cursor.execute("SELECT company_id, company_name FROM Company")
    companies = cursor.fetchall()

    if companies:
        st.markdown('<div class="card"><div class="card-title">Stock Details</div>', unsafe_allow_html=True)
        company_dict = {c[1]: c[0] for c in companies}
        col1, col2 = st.columns(2)
        with col1:
            selected_company = st.selectbox("Select Company", list(company_dict.keys()))
        with col2:
            symbol = st.text_input("Stock Symbol", placeholder="e.g. RELIANCE")

        if st.button("➕  Insert Stock"):
            if symbol:
                cursor.execute(
                    "INSERT INTO Stock (symbol, company_id) VALUES (%s,%s)",
                    (symbol.upper(), company_dict[selected_company])
                )
                conn.commit()
                st.success(f"✅ Stock **{symbol.upper()}** listed successfully.")
            else:
                st.warning("Enter a stock symbol.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Add a company first before listing stocks.")


# ─────────────────────────────────────────────
#  ADD DAILY PRICE
# ─────────────────────────────────────────────
elif page == "Add Daily Price":
    page_header("Add Daily Price", "Log OHLCV data for a stock")

    cursor.execute("SELECT stock_id, symbol FROM Stock")
    stocks = cursor.fetchall()

    if stocks:
        stock_dict = {s[1]: s[0] for s in stocks}
        st.markdown('<div class="card"><div class="card-title">Trade Data</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            selected_stock = st.selectbox("Stock Symbol", list(stock_dict.keys()))
            date = st.date_input("Trade Date")
            open_price = st.number_input("Open Price (₹)", min_value=0.0, step=0.5)
            close_price = st.number_input("Close Price (₹)", min_value=0.0, step=0.5)
        with col2:
            st.write("")  # spacer
            st.write("")
            high_price = st.number_input("High Price (₹)", min_value=0.0, step=0.5)
            low_price = st.number_input("Low Price (₹)", min_value=0.0, step=0.5)
            volume = st.number_input("Volume", min_value=0, step=100)

        if st.button("💹  Insert Price Record"):
            cursor.execute(
                """INSERT INTO Daily_Price
                   (stock_id, trade_date, open_price, close_price, high_price, low_price, volume)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (stock_dict[selected_stock], date, open_price, close_price, high_price, low_price, volume)
            )
            conn.commit()
            st.success(f"✅ Price record for **{selected_stock}** on **{date}** saved.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Add a stock first.")


# ─────────────────────────────────────────────
#  VIEW DATA
# ─────────────────────────────────────────────
elif page == "View Data":
    page_header("Price Records", "All daily OHLCV entries")

    cursor.execute("""
        SELECT s.symbol, d.trade_date, d.open_price, d.close_price,
               d.high_price, d.low_price, d.volume
        FROM Stock s JOIN Daily_Price d ON s.stock_id = d.stock_id
        ORDER BY d.trade_date DESC
    """)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Symbol", "Date", "Open", "Close", "High", "Low", "Volume"])

    # Search filter
    search = st.text_input("🔍  Filter by symbol", placeholder="e.g. INFY")
    if search:
        df = df[df["Symbol"].str.contains(search.upper())]

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"{len(df)} records shown")


# ─────────────────────────────────────────────
#  ANALYTICS
# ─────────────────────────────────────────────
elif page == "Analytics":
    page_header("Analytics", "Aggregated stock performance")

    cursor.execute("""
        SELECT s.symbol,
               MAX(d.close_price),
               ROUND(AVG(d.close_price), 2),
               MAX(d.volume)
        FROM Stock s JOIN Daily_Price d ON s.stock_id = d.stock_id
        GROUP BY s.symbol
    """)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Symbol", "Highest Price", "Avg Price", "Max Volume"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🏆 Top 3 Stocks by All-Time High")

    cursor.execute("""
        SELECT s.symbol, MAX(d.close_price) AS highest_price
        FROM Stock s JOIN Daily_Price d ON s.stock_id = d.stock_id
        GROUP BY s.symbol ORDER BY highest_price DESC LIMIT 3
    """)
    data2 = cursor.fetchall()
    if data2:
        df2 = pd.DataFrame(data2, columns=["Stock", "Highest Price (₹)"])

        fig, ax = plt.subplots(figsize=(8, 2.8))
        bar_colors = ["#38bdf8", "#818cf8", "#34d399"]
        bars = ax.barh(
            df2["Stock"], df2["Highest Price (₹)"],
            color=bar_colors[:len(df2)],
            height=0.35,
            edgecolor="none"
        )
        ax.bar_label(bars, fmt="₹%.2f", color="#94a3b8", fontsize=8.5, padding=8)
        ax.set_xlim(0, float(df2["Highest Price (₹)"].max()) * 1.2)
        apply_chart_style(ax, fig)
        ax.set_xlabel("Highest Close Price (₹)", fontsize=9)
        ax.tick_params(axis='y', labelsize=10, labelcolor="#e2e8f0")
        ax.invert_yaxis()
        fig.tight_layout()
        st.pyplot(fig)


# ─────────────────────────────────────────────
#  COMPARE STOCKS
# ─────────────────────────────────────────────
elif page == "Compare Stocks":
    page_header("Compare Stocks", "Side-by-side closing price comparison")

    cursor.execute("SELECT stock_id, symbol FROM Stock")
    stocks = cursor.fetchall()

    if len(stocks) >= 2:
        stock_dict = {s[1]: s[0] for s in stocks}
        col1, col2 = st.columns(2)
        with col1:
            stock1 = st.selectbox("First Stock", list(stock_dict.keys()), index=0)
        with col2:
            stock2 = st.selectbox("Second Stock", list(stock_dict.keys()), index=1)

        if st.button("📊  Compare"):
            query = "SELECT trade_date, close_price FROM Daily_Price WHERE stock_id=%s ORDER BY trade_date"
            cursor.execute(query, (stock_dict[stock1],))
            d1 = pd.DataFrame(cursor.fetchall(), columns=["Date", "Close"])
            cursor.execute(query, (stock_dict[stock2],))
            d2 = pd.DataFrame(cursor.fetchall(), columns=["Date", "Close"])

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(d1["Date"], d1["Close"], color=COLORS[0], linewidth=2, label=stock1, marker="o", markersize=3)
            ax.plot(d2["Date"], d2["Close"], color=COLORS[1], linewidth=2, label=stock2, marker="o", markersize=3)
            ax.fill_between(d1["Date"], d1["Close"], alpha=0.08, color=COLORS[0])
            ax.fill_between(d2["Date"], d2["Close"], alpha=0.08, color=COLORS[1])
            legend = ax.legend(facecolor="#111827", edgecolor="#1e2d4a", labelcolor="#e2e8f0", fontsize=10)
            apply_chart_style(ax, fig)
            ax.set_ylabel("Close Price (₹)")
            st.pyplot(fig)
    else:
        st.warning("⚠️ Add at least two stocks to compare.")


# ─────────────────────────────────────────────
#  PRICE TRENDS
# ─────────────────────────────────────────────
elif page == "Price Trends":
    page_header("Price Trends", "Historical closing price for all stocks")

    cursor.execute("""
        SELECT s.symbol, d.trade_date, d.close_price
        FROM Stock s JOIN Daily_Price d ON s.stock_id = d.stock_id
        ORDER BY d.trade_date
    """)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Stock", "Date", "Close"])

    if not df.empty:
        fig, ax = plt.subplots(figsize=(11, 4.5))
        for i, stock in enumerate(df["Stock"].unique()):
            sdf = df[df["Stock"] == stock]
            ax.plot(sdf["Date"], sdf["Close"],
                    color=COLORS[i % len(COLORS)], linewidth=2,
                    label=stock, marker="o", markersize=3)
            ax.fill_between(sdf["Date"], sdf["Close"], alpha=0.06, color=COLORS[i % len(COLORS)])

        legend = ax.legend(facecolor="#111827", edgecolor="#1e2d4a",
                           labelcolor="#e2e8f0", fontsize=9, ncol=4)
        apply_chart_style(ax, fig)
        ax.set_ylabel("Close Price (₹)")
        st.pyplot(fig)
    else:
        st.info("No data available yet.")


# ─────────────────────────────────────────────
#  DELETE STOCK
# ─────────────────────────────────────────────
elif page == "Delete Stock":
    page_header("Delete Stock", "Remove a stock and its price data")

    cursor.execute("SELECT stock_id, symbol FROM Stock")
    stocks = cursor.fetchall()

    if stocks:
        stock_dict = {s[1]: s[0] for s in stocks}

        st.markdown('<div class="card"><div class="card-title" style="color:#f87171;">⚠️ Danger Zone</div>', unsafe_allow_html=True)
        selected_stock = st.selectbox("Select Stock to Delete", list(stock_dict.keys()))
        st.caption("This will permanently remove the stock and all its daily price records.")

        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("🗑️  Delete Stock"):
            cursor.execute("DELETE FROM Daily_Price WHERE stock_id=%s", (stock_dict[selected_stock],))
            cursor.execute("DELETE FROM Stock WHERE stock_id=%s", (stock_dict[selected_stock],))
            conn.commit()
            st.success(f"✅ **{selected_stock}** deleted successfully.")
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.warning("No stocks available to delete.")