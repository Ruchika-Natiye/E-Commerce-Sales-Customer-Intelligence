import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# PAGE CONFIGURATION

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded")


# CUSTOM CSS - IVORY, FOREST GREEN & CORAL THEME

st.markdown("""
<style>
/* =====================================================
   MAIN BACKGROUND
   ===================================================== */
.stApp {
    background: #F4F7F5;
    color: #24332F;}
[data-testid="stMain"] {
    background: #F4F7F5;}
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5,
[data-testid="stMain"] label {
    color: #24332F;}

/* Main headings */
[data-testid="stMain"] h1 {
    color: #123C35 !important;
    font-weight: 800 !important;
    letter-spacing: -0.6px;}
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    color: #1B554A !important;
    font-weight: 700 !important;}
/* =====================================================
   SIDEBAR
   ===================================================== */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #123C35 0%,
        #1B554A 100%
    ) !important;
    border-right: 1px solid #D7E3DD;}

[data-testid="stSidebar"] * {
    color: #F7FBF8 !important;}
/* Sidebar navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.07);
    border-radius: 9px;
    padding: 7px 10px;
    margin: 3px 0;}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.16);
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.2) !important;}

/* Sidebar caption */

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #D8E9E1 !important;}
/* =====================================================
   FILE UPLOADER
   ===================================================== */
[data-testid="stFileUploader"] section {
    background: #FFFFFF !important;
    border: 1px dashed #91B5A7 !important;
    border-radius: 12px !important;}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] section * {color: #24332F !important;}
[data-testid="stFileUploader"] label {color: #F7FBF8 !important;}

[data-testid="stFileUploader"] button {background: #E8F2ED !important;
color: #123C35 !important;border: 1px solid #B8D0C5 !important;
border-radius: 8px !important;}
/* =====================================================
   INPUT LABELS
   ===================================================== */
[data-testid="stDateInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label {
    color: #F7FBF8 !important;
    font-weight: 600 !important;}

/* Main-area labels */

[data-testid="stMain"] [data-testid="stDateInput"] label,
[data-testid="stMain"] [data-testid="stTextInput"] label,
[data-testid="stMain"] [data-testid="stNumberInput"] label,
[data-testid="stMain"] [data-testid="stTextArea"] label,
[data-testid="stMain"] [data-testid="stSelectbox"] label,
[data-testid="stMain"] [data-testid="stMultiSelect"] label {
    color: #24332F !important;}

/* =====================================================
   DATE PICKER AND TEXT INPUTS
   ===================================================== */

[data-testid="stDateInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #24332F !important;
    -webkit-text-fill-color: #24332F !important;
    border: 1px solid #C8D8D0 !important;
    border-radius: 9px !important;
}

[data-testid="stDateInput"] button {
    background: #FFFFFF !important;
    color: #123C35 !important;
}

/* =====================================================
   SELECT BOX AND MULTISELECT
   ===================================================== */

[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #C8D8D0 !important;
    border-radius: 9px !important;
}

[data-testid="stSelectbox"] input,
[data-testid="stMultiSelect"] input {
    color: #24332F !important;
    -webkit-text-fill-color: #24332F !important;
}

/* Selected multiselect tags */

[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: #DCECE4 !important;
    border-radius: 6px !important;}

[data-testid="stMultiSelect"] [data-baseweb="tag"] * {
    color: #123C35 !important;}

/* =====================================================
   DROPDOWN MENUS AND CALENDAR
   ===================================================== */

[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="list"],
[data-baseweb="calendar"] {
    background: #FFFFFF !important;}

[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[data-baseweb="list"] *,
[data-baseweb="calendar"] * {
    color: #24332F !important;}

/* =====================================================
   RADIO BUTTONS AND CHECKBOXES
   ===================================================== */

[data-testid="stMain"] [data-testid="stRadio"] label,
[data-testid="stMain"] [data-testid="stRadio"] p,
[data-testid="stMain"] [data-testid="stRadio"] span,
[data-testid="stMain"] [data-testid="stCheckbox"] label,
[data-testid="stMain"] [data-testid="stCheckbox"] span {
    color: #24332F !important;
}

/* =====================================================
   METRIC CARDS
   ===================================================== */

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 20px 16px !important;
    border: 1px solid #DCE7E1 !important;
    border-left: 4px solid #1B8069 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(18, 60, 53, 0.07) !important;
    text-align: center !important;}

/* Metric labels */

[data-testid="stMetricLabel"] {
    color: #60746B !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;}

[data-testid="stMetricLabel"] * {
    color: #60746B !important;
    font-weight: 700 !important;}

/* Metric values */

[data-testid="stMetricValue"] {
    color: #123C35 !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;}

[data-testid="stMetricValue"] * {
    color: #123C35 !important;
    font-weight: 800 !important;}

/* Metric delta */

[data-testid="stMetricDelta"] {
    justify-content: center !important;}

/* =====================================================
   TABS
   ===================================================== */

button[data-baseweb="tab"] {
    color: #60746B !important;
    font-weight: 650 !important;}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #14745E !important;
    border-bottom-color: #E4775D !important;}

/* =====================================================
   BUTTONS
   ===================================================== */

.stButton button,
.stDownloadButton button {
    background: #16745E !important;
    color: #FFFFFF !important;
    border: 1px solid #16745E !important;
    border-radius: 9px !important;
    padding: 7px 16px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease-in-out;}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #E4775D !important;
    border-color: #E4775D !important;
    color: #FFFFFF !important;}

/* =====================================================
   EXPANDERS
   ===================================================== */

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE7E1 !important;
    border-radius: 12px !important;}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #123C35 !important;
    font-weight: 650 !important;}

/* =====================================================
   DATA TABLES
   ===================================================== */

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE7E1 !important;
    border-radius: 10px !important;}

/* =====================================================
   ALERTS AND STATUS MESSAGES
   ===================================================== */

[data-testid="stAlert"] {
    border-radius: 10px !important;}

/* =====================================================
   LINKS
   ===================================================== */

a {
    color: #16745E !important;
    font-weight: 600;
}

/* =====================================================
   CAPTIONS
   ===================================================== */

[data-testid="stCaptionContainer"],
.stCaption {
    color: #71837A !important;
}

/* =====================================================
   DIVIDERS
   ===================================================== */

hr {
    border-color: #DCE7E1 !important;
}

/* =====================================================
   PLOTLY CHART CONTAINERS
   ===================================================== */

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 2px solid #C8D8D0 !important;
    border-radius: 14px !important;
    padding: 10px !important;
    box-shadow: 0 4px 14px rgba(18, 60, 53, 0.10) !important;
    overflow:hidden !important;
    box-sizing: border-box !important;
}

/* =====================================================
   RESPONSIVE METRIC SIZING
   ===================================================== */

@media (max-width: 768px) {

    [data-testid="stMetricValue"] {
        font-size: 21px !important;
    }

    [data-testid="stMetric"] {
        padding: 14px 10px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# PROJECT PATHS
# =====================================================

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "processed" / "cleaned_sales.csv"
OUTPUT_PATH = ROOT / "outputs"
RFM_PATH = OUTPUT_PATH / "rfm_segments.csv"
FORECAST_PATH = OUTPUT_PATH / "sales_forecast.csv"
CHURN_PATH = OUTPUT_PATH / "churn_risk.csv"
BASKET_PATH = OUTPUT_PATH / "market_basket_rules.csv"


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def format_currency(value):
    return f"£{value:,.2f}"
def style_chart(fig, title=None):
    fig.update_layout(
        template="plotly_white",
        title=title,
        font=dict(color="#24332F", size=13),
        title_font=dict(color="#123C35", size=20),
        paper_bgcolor="#FFFDF0",
        plot_bgcolor="#FFF8DC",
        colorway=["#16745E"],
        autosize=True,
        margin=dict(l=30, r=20, t=60, b=80),
        legend=dict(font=dict(color="#40554B")),)
    for trace in fig.data:
       if trace.type == "bar":
          trace.marker.color = "#123C35"
       elif trace.type == "scatter":
          trace.line.color = "#123C35"
          trace.marker.color = "#123C35"  
    fig.update_xaxes(
        color="#40554B",
        gridcolor="#E7EEEA",
        zerolinecolor="#D4E0D9")
    fig.update_yaxes(
        color="#40554B",
        gridcolor="#E7EEEA",
        zerolinecolor="#D4E0D9")
    return fig
def load_optional_csv(path):
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()
@st.cache_data
def load_data(file_bytes=None, file_name=None):
    if file_bytes is not None:
        if file_name.lower().endswith(".xlsx"):
            df = pd.read_excel(file_bytes)
        else:
            df = pd.read_csv(file_bytes)
    else:
        if not DATA_PATH.exists():
            return pd.DataFrame()
        df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    required = [
        "InvoiceNo",
        "StockCode",
        "Quantity",
        "InvoiceDate",
        "UnitPrice"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"], errors="coerce")
    if "CustomerID" not in df.columns:
        df["CustomerID"] = "Unknown"
    df["CustomerID"] = (
        df["CustomerID"]
        .fillna("Unknown")
        .astype(str)
        .str.replace(r"\.0$", "", regex=True))
    if "Description" not in df.columns:
        df["Description"] = df["StockCode"].astype(str)
    if "Country" not in df.columns:
        df["Country"] = "Unknown"
    if "Revenue" not in df.columns:
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["Revenue"] = pd.to_numeric(
        df["Revenue"], errors="coerce")
    df = df.dropna(
        subset=[
            "InvoiceDate",
            "Quantity",
            "UnitPrice",
            "Revenue" ])
    df = df[
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0) &
        (df["Revenue"] > 0)].copy()
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["Weekday"] = df["InvoiceDate"].dt.day_name()
    return df


# =====================================================
# SIDEBAR AND DATA LOADING
# =====================================================

st.sidebar.title("🛒 E-Commerce Analytics")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(
    "Upload Sales Dataset",
    type=["csv", "xlsx"])
try:
    if uploaded_file is not None:
        df = load_data(
            uploaded_file,
            uploaded_file.name)
    else:
        df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()
if df.empty:
    st.title("🛒 E-Commerce Analytics")
    st.warning(
        "Please upload your sales dataset or place "
        "cleaned_sales.csv inside data/processed/.")
    st.stop()
# =====================================================
# FILTERS
# =====================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")
min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[
        (df["InvoiceDate"].dt.date >= start_date) &
        (df["InvoiceDate"].dt.date <= end_date)].copy()

else:
    filtered_df = df.copy()
countries = sorted(
    filtered_df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=countries,
    default=countries)
filtered_df = filtered_df[
    filtered_df["Country"].isin(selected_countries)].copy()

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()
# =====================================================
# NAVIGATION
# =====================================================

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard Overview",
        "Sales Analysis",
        "Customer Intelligence",
        "Product Analysis",
        "Forecast & Churn",
        "Market Basket Analysis"
    ])
st.sidebar.markdown("---")
st.sidebar.caption(
    "Python | Pandas | Plotly | Machine Learning")
# =====================================================
# COMMON KPIs
# =====================================================
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
customer_data = filtered_df[
    filtered_df["CustomerID"] != "Unknown"]
total_customers = customer_data["CustomerID"].nunique()
total_products = filtered_df["StockCode"].nunique()
total_quantity = filtered_df["Quantity"].sum()
average_order_value = (
    total_revenue / total_orders
    if total_orders else 0)
# =====================================================
# PAGE 1: DASHBOARD OVERVIEW
# =====================================================

if page == "Dashboard Overview":
    st.title("🛒 E-Commerce Analytics")
    st.subheader("Sales Performance & Business Intelligence")
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", format_currency(total_revenue))
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Total Customers", f"{total_customers:,}")
    c4.metric("Total Products", f"{total_products:,}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Quantity Sold", f"{total_quantity:,.0f}")
    c2.metric("Average Order Value", format_currency(average_order_value))
    avg_customer_revenue = (
        total_revenue / total_customers
        if total_customers else 0
    )
    c3.metric(
        "Revenue per Customer",
        format_currency(avg_customer_revenue)
    )
    st.markdown("---")
    monthly = (
        filtered_df.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )
    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(
            monthly,
            x="Month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue Trend"
        )
        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:
        country_sales = (
            filtered_df.groupby("Country")["Revenue"]
            .sum()
            .reset_index()
            .nlargest(10, "Revenue")
        )
        fig = px.bar(
            country_sales,
            x="Country",
            y="Revenue",
            title="Top 10 Countries by Revenue"
        )
        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    c1, c2 = st.columns(2)
    with c1:
        products = (
            filtered_df.groupby(
                ["StockCode", "Description"],
                dropna=False
            )["Revenue"]
            .sum()
            .reset_index()
            .nlargest(10, "Revenue")
        )

        products["Product"] = (
            products["StockCode"].astype(str)
            + " - "
            + products["Description"].fillna("")
        )

        fig = px.bar(
            products.sort_values("Revenue"),
            x="Revenue",
            y="Product",
            orientation="h",
            title="Top 10 Products"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        weekday = (
            filtered_df.groupby("Weekday")["Revenue"]
            .sum()
            .reset_index()
        )

        order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        weekday["Weekday"] = pd.Categorical(
            weekday["Weekday"],
            categories=order,
            ordered=True
        )

        weekday = weekday.sort_values("Weekday")

        fig = px.bar(
            weekday,
            x="Weekday",
            y="Revenue",
            title="Revenue by Weekday"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.markdown("---")
    st.subheader("Recent Sales Records")

    st.dataframe(
        filtered_df.sort_values(
            "InvoiceDate", ascending=False
        ).head(20),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# PAGE 2: SALES ANALYSIS
# =====================================================

elif page == "Sales Analysis":

    st.title("📈 Sales Analysis")

    monthly = (
        filtered_df.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    monthly["Growth_Percentage"] = (
        monthly["Revenue"].pct_change() * 100
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = px.line(
            monthly,
            x="Month",
            y="Revenue",
            markers=True,
            title="Monthly Sales"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        fig = px.bar(
            monthly.dropna(),
            x="Month",
            y="Growth_Percentage",
            title="Monthly Growth Percentage"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.markdown("---")

    country = (
        filtered_df.groupby("Country")["Revenue"]
        .sum()
        .reset_index()
        .nlargest(15, "Revenue")
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            country,
            x="Country",
            y="Revenue",
            title="Country-wise Sales"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        fig = px.pie(
            country.head(10),
            names="Country",
            values="Revenue",
            hole=0.45,
            title="Revenue Share by Country"
        )

        fig.update_traces(
            textfont_color="#24332F"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.subheader("Monthly Sales Details")

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Monthly Sales",
        monthly.to_csv(index=False),
        "monthly_sales.csv",
        "text/csv"
    )


# =====================================================
# PAGE 3: CUSTOMER INTELLIGENCE
# =====================================================

elif page == "Customer Intelligence":

    st.title("👥 Customer Intelligence")

    customers = filtered_df[
        filtered_df["CustomerID"] != "Unknown"
    ].copy()

    if customers.empty:

        st.warning("No identified customers found.")

    else:

        customer_sales = (
            customers.groupby("CustomerID")
            .agg(
                Total_Revenue=("Revenue", "sum"),
                Total_Orders=("InvoiceNo", "nunique"),
                Total_Quantity=("Quantity", "sum"),
                Last_Purchase=("InvoiceDate", "max")
            )
            .reset_index()
        )

        customer_sales["Average_Order_Value"] = (
            customer_sales["Total_Revenue"] /
            customer_sales["Total_Orders"]
        )

        customer_sales["Customer_Type"] = np.where(
            customer_sales["Total_Orders"] > 1,
            "Repeat Customer",
            "One-Time Customer"
        )

        repeat = (
            customer_sales["Customer_Type"] ==
            "Repeat Customer"
        ).sum()

        one_time = (
            customer_sales["Customer_Type"] ==
            "One-Time Customer"
        ).sum()

        c1, c2, c3 = st.columns(3)

        c1.metric("Customers", len(customer_sales))
        c2.metric("Repeat Customers", repeat)
        c3.metric("One-Time Customers", one_time)

        c1, c2 = st.columns(2)

        with c1:

            fig = px.pie(
                customer_sales,
                names="Customer_Type",
                values="CustomerID",
                hole=0.45,
                title="Repeat vs One-Time Customers"
            )

            fig.update_traces(
                textfont_color="#24332F"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        with c2:

            top = customer_sales.nlargest(
                10, "Total_Revenue"
            )

            fig = px.bar(
                top.sort_values("Total_Revenue"),
                x="Total_Revenue",
                y="CustomerID",
                orientation="h",
                title="Top 10 Customers"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        st.subheader("Customer Purchase Details")

        st.dataframe(
            customer_sales.sort_values(
                "Total_Revenue",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Customer Analysis",
            customer_sales.to_csv(index=False),
            "customer_analysis.csv",
            "text/csv"
        )

        st.markdown("---")
        st.subheader("🎯 RFM Segmentation")

        rfm = load_optional_csv(RFM_PATH)

        if not rfm.empty:

            st.dataframe(
                rfm,
                use_container_width=True,
                hide_index=True
            )

            if "Segment" in rfm.columns:

                counts = (
                    rfm["Segment"]
                    .value_counts()
                    .reset_index()
                )

                counts.columns = ["Segment", "Customers"]

                fig = px.bar(
                    counts,
                    x="Segment",
                    y="Customers",
                    title="Customer Segments"
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True
                )

        else:

            st.info(
                "Run src/rfm_segmentation.py to generate RFM results."
            )


# =====================================================
# PAGE 4: PRODUCT ANALYSIS
# =====================================================

elif page == "Product Analysis":

    st.title("📦 Product Analysis")

    product_sales = (
        filtered_df.groupby(
            ["StockCode", "Description"],
            dropna=False
        )
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Total_Orders=("InvoiceNo", "nunique")
        )
        .reset_index()
    )

    c1, c2 = st.columns(2)

    with c1:

        top = product_sales.nlargest(
            10, "Total_Revenue"
        )

        fig = px.bar(
            top.sort_values("Total_Revenue"),
            x="Total_Revenue",
            y="Description",
            orientation="h",
            title="Top Products by Revenue"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        popular = product_sales.nlargest(
            10, "Total_Quantity"
        )

        fig = px.bar(
            popular.sort_values("Total_Quantity"),
            x="Total_Quantity",
            y="Description",
            orientation="h",
            title="Top Products by Quantity"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.subheader("Product Performance")

    st.dataframe(
        product_sales.sort_values(
            "Total_Revenue",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Product Analysis",
        product_sales.to_csv(index=False),
        "product_analysis.csv",
        "text/csv"
    )


# =====================================================
# PAGE 5: FORECAST AND CHURN
# =====================================================

elif page == "Forecast & Churn":

    st.title("🤖 Forecasting & Customer Churn")

    st.subheader("📈 Sales Forecast")

    forecast = load_optional_csv(FORECAST_PATH)

    if not forecast.empty:

        st.dataframe(
            forecast,
            use_container_width=True,
            hide_index=True
        )

        date_col = next(
            (
                c for c in forecast.columns
                if c.lower() in ["month", "date", "ds"]
            ),
            None
        )

        value_col = next(
            (
                c for c in forecast.columns
                if c.lower() in [
                    "forecast",
                    "predicted_sales",
                    "predicted_revenue",
                    "sales_forecast",
                    "prediction"
                ]
            ),
            None
        )

        if date_col and value_col:

            fig = px.line(
                forecast,
                x=date_col,
                y=value_col,
                markers=True,
                title="Predicted Sales"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

    else:

        st.info(
            "Run src/sales_forecasting.py to generate forecasts."
        )

    st.markdown("---")

    st.subheader("⚠️ Customer Churn Analysis")

    churn = load_optional_csv(CHURN_PATH)

    if not churn.empty:

        st.dataframe(
            churn,
            use_container_width=True,
            hide_index=True
        )

        churn_col = next(
            (
                c for c in churn.columns
                if c.lower() in [
                    "churn",
                    "churn_risk",
                    "churn_prediction",
                    "prediction",
                    "risk"
                ]
            ),
            None
        )

        if churn_col:

            counts = (
                churn[churn_col]
                .astype(str)
                .value_counts()
                .reset_index()
            )

            counts.columns = ["Churn Category", "Customers"]

            fig = px.pie(
                counts,
                names="Churn Category",
                values="Customers",
                hole=0.45,
                title="Churn Distribution"
            )

            fig.update_traces(
                textfont_color="#24332F"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        st.download_button(
            "Download Churn Results",
            churn.to_csv(index=False),
            "churn_analysis.csv",
            "text/csv"
        )

    else:

        st.info("Run src/churn_prediction.py to generate churn results.")

    st.caption(
        "Churn is an inactivity-based prediction proxy, "
        "not a confirmed customer cancellation.")


# =====================================================
# PAGE 6: MARKET BASKET ANALYSIS
# =====================================================

elif page == "Market Basket Analysis":

    st.title("🛍️ Market Basket Analysis")

    st.write(
        "Discover products frequently purchased together."
    )

    basket = load_optional_csv(BASKET_PATH)

    if not basket.empty:

        st.subheader("Product Association Rules")

        st.dataframe(
            basket,
            use_container_width=True,
            hide_index=True
        )

        confidence_col = next(
            (
                c for c in basket.columns
                if c.lower() == "confidence"
            ),
            None
        )

        if confidence_col:

            basket[confidence_col] = pd.to_numeric(
                basket[confidence_col],
                errors="coerce"
            )

            top_rules = basket.nlargest(
                10, confidence_col
            )

            fig = px.bar(
                top_rules,
                x=confidence_col,
                y=top_rules.index.astype(str),
                orientation="h",
                title="Top Association Rules by Confidence"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        st.download_button(
            "Download Market Basket Rules",
            basket.to_csv(index=False),
            "market_basket_rules.csv",
            "text/csv"
        )

    else:

        st.info(
            "Run src/market_basket.py to generate association rules."
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    background-color:#E6F0EB;
    border-radius:10px;
">
    <h3 style="color:#123C35;">
        E-Commerce Sales & Customer Intelligence
    </h3>

    <p style="color:#24332F;">
        Built using Python | Pandas | Plotly | Streamlit
    </p>

    <p style="color:#60746B;">
        Data Science & Machine Learning Project
    </p>
</div>
""", unsafe_allow_html=True)
