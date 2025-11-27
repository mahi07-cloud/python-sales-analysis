import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sales Intelligence Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (Sci-Fi / Cyberpunk Theme) ---
st.markdown("""
<style>
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #050505 100%);
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #0a0a0f;
        border-right: 1px solid rgba(0, 229, 255, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* KPI Cards (Glassmorphism) */
    div.metric-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.05);
        text-align: center;
        transition: transform 0.3s ease;
    }
    div.metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.2);
        border: 1px solid rgba(0, 229, 255, 0.5);
    }
    
    /* Custom Metric Text */
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        background: -webkit-linear-gradient(#00E5FF, #2979FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Remove top bar */
    header[data-testid="stHeader"] {
        background: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def get_data():
    df = pd.read_csv('sales_data.csv')
    
    # Cleaning
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
    df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
    df.dropna(subset=['Quantity Ordered', 'Price Each'], inplace=True)
    
    # Logic
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    # City Logic
    def get_city(address):
        return address.split(',')[0].strip('"')
    df['City'] = df['Purchase Address'].apply(lambda x: get_city(x))
    
    return df

df = get_data()

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.title("⚡ Control Panel")
st.sidebar.markdown("---")

city = st.sidebar.multiselect(
    "📍 Filter by City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

product_type = st.sidebar.multiselect(
    "📦 Filter by Product:",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Filter Data
df_selection = df.query("City == @city & Product == @product_type")

if df_selection.empty:
    st.error("⚠️ No data available! Please adjust your filters.")
    st.stop()

# --- 5. MAIN INTERFACE ---

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>📊 E-Commerce <span style='color:#00E5FF'>Live Intelligence</span></h1>", unsafe_allow_html=True)

# Calculations
total_sales = int(df_selection["Sales"].sum())
avg_sale = round(df_selection["Sales"].mean(), 2)
total_qty = int(df_selection["Quantity Ordered"].sum())

# KPI ROW
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">$ {total_sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Avg Transaction</div>
        <div class="metric-value">$ {avg_sale}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Units Sold</div>
        <div class="metric-value">{total_qty:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 6. ADVANCED CHARTS ---

col1, col2 = st.columns([2, 1])

# Chart 1: Neon Bar Chart
with col1:
    st.subheader("📈 Revenue by Product")
    
    sales_by_product = df_selection.groupby("Product").sum(numeric_only=True)[["Sales"]].sort_values("Sales")
    
    fig_bar = go.Figure(go.Bar(
        x=sales_by_product["Sales"],
        y=sales_by_product.index,
        orientation='h',
        marker=dict(
            color=sales_by_product["Sales"],
            colorscale='Viridis', # Changed to Viridis (Blue/Green/Purple) which is 100% safe
            line=dict(color='rgba(0, 229, 255, 0.5)', width=1)
        )
    ))
    
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title="Revenue ($)", tickfont=dict(color='#94a3b8')),
        yaxis=dict(tickfont=dict(color='#e0e0e0')),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Chart 2: 3D Donut Chart
with col2:
    st.subheader("🌍 Regional Split")
    
    sales_by_city = df_selection.groupby("City").sum(numeric_only=True)[["Sales"]].reset_index()
    
    fig_pie = px.pie(
        sales_by_city,
        values='Sales',
        names='City',
        hole=0.6,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0'),
        annotations=[dict(text='Sales', x=0.5, y=0.5, font_size=20, showarrow=False, font_color='white')],
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 7. DATA TABLE EXPANDER ---
st.markdown("### 📋 Detailed Records")
with st.expander("Click to view raw data"):
    # FIX: Changed cmap="mako" to "PuBu" (Purple-Blue) which is standard in Matplotlib
    st.dataframe(
        df_selection.style.background_gradient(cmap="PuBu"),
        use_container_width=True
    )
    
    # CSV Download Button
    csv = df_selection.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name='sales_data_export.csv',
        mime='text/csv',
    )