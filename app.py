"""
================================================================================
LUXURY E-COMMERCE ANALYTICS DASHBOARD
================================================================================
Senior Data Analyst: Premium Retail Analytics Platform
Client: High-End UAE E-Commerce Firm
Tech Stack: Streamlit, Plotly, Pandas
================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ================================================================================
# PAGE CONFIGURATION
# ================================================================================

st.set_page_config(
    page_title="Luxury E-Commerce Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================================
# CUSTOM CSS - LUXURY THEME
# ================================================================================

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%);
        border-right: 1px solid #c9a227;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #f5f5f5;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #c9a227 !important;
        font-family: 'Playfair Display', serif;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #c9a227;
        font-size: 2rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #f5f5f5;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        color: #4ade80;
    }
    
    /* Cards/Containers */
    .luxury-card {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #c9a227;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    .gold-text {
        color: #c9a227;
        font-weight: bold;
    }
    
    .premium-header {
        background: linear-gradient(90deg, #c9a227, #f4d03f, #c9a227);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Divider */
    .gold-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #c9a227, transparent);
        margin: 20px 0;
    }
    
    /* DataFrames */
    .stDataFrame {
        border: 1px solid #c9a227;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(26, 26, 46, 0.5);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #f5f5f5;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #c9a227 !important;
        color: #1a1a2e !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: rgba(26, 26, 46, 0.8);
        border: 1px solid #c9a227;
        color: #f5f5f5;
    }
    
    /* Date input */
    .stDateInput > div > div {
        background-color: rgba(26, 26, 46, 0.8);
        border: 1px solid #c9a227;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background-color: rgba(26, 26, 46, 0.8);
        border: 1px solid #c9a227;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: rgba(201, 162, 39, 0.1);
        border: 1px solid #c9a227;
        color: #f5f5f5;
    }
    
    /* KPI Box */
    .kpi-box {
        background: linear-gradient(135deg, rgba(201, 162, 39, 0.1), rgba(26, 26, 46, 0.9));
        border: 1px solid #c9a227;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .kpi-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(201, 162, 39, 0.2);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #c9a227;
        margin: 10px 0;
    }
    
    .kpi-label {
        color: #f5f5f5;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .kpi-delta-positive {
        color: #4ade80;
        font-size: 0.9rem;
    }
    
    .kpi-delta-negative {
        color: #f87171;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================================
# DATA LOADING AND CLEANING FUNCTIONS
# ================================================================================

@st.cache_data
def load_data():
    """Load and perform initial data cleaning"""
    try:
        # Load CSV files
        customers = pd.read_csv('customers.csv')
        orders = pd.read_csv('orders.csv')
        order_items = pd.read_csv('order_items.csv')
        fulfillment = pd.read_csv('fulfillment.csv')
        returns = pd.read_csv('returns.csv')
        
        # ====== DATA CLEANING ======
        
        # 1. Remove duplicates
        customers = customers.drop_duplicates(subset=['customer_id'], keep='first')
        orders = orders.drop_duplicates(subset=['order_id'], keep='first')
        
        # 2. Standardize city names
        city_mapping = {
            'DUBAI': 'Dubai', 'dubai': 'Dubai', 'Dxb': 'Dubai',
            'ABU DHABI': 'Abu Dhabi', 'abu dhabi': 'Abu Dhabi', 'AD': 'Abu Dhabi',
            'SHARJAH': 'Sharjah', 'sharjah': 'Sharjah', 'SHJ': 'Sharjah',
            'AJMAN': 'Ajman', 'ajman': 'Ajman',
            'RAS AL KHAIMAH': 'Ras Al Khaimah', 'ras al khaimah': 'Ras Al Khaimah', 'RAK': 'Ras Al Khaimah'
        }
        customers['city'] = customers['city'].replace(city_mapping)
        
        # 3. Standardize category names
        category_mapping = {
            'electronics': 'Electronics', 'ELECTRONICS': 'Electronics', 'Elec': 'Electronics',
            'fashion': 'Fashion', 'FASHION': 'Fashion', 'Fash': 'Fashion',
            'home & kitchen': 'Home & Kitchen', 'HOME & KITCHEN': 'Home & Kitchen', 'Home': 'Home & Kitchen',
            'beauty': 'Beauty', 'BEAUTY': 'Beauty',
            'groceries': 'Groceries', 'GROCERIES': 'Groceries', 'Groc': 'Groceries'
        }
        order_items['product_category'] = order_items['product_category'].replace(category_mapping)
        
        # 4. Standardize delivery status
        status_mapping = {
            'OnTime': 'On Time', 'on-time': 'On Time', 'ON TIME': 'On Time',
            'delayed': 'Delayed', 'DELAYED': 'Delayed',
            'failed': 'Failed', 'FAILED': 'Failed',
            'pending': 'Pending', 'PENDING': 'Pending'
        }
        fulfillment['delivery_status'] = fulfillment['delivery_status'].replace(status_mapping)
        
        # 5. Handle missing values
        orders['discount_amount'] = orders['discount_amount'].fillna(0)
        fulfillment['delivery_zone'] = fulfillment['delivery_zone'].fillna('Unknown')
        returns['return_reason'] = returns['return_reason'].fillna('Not Specified')
        
        # 6. Fix negative amounts
        orders['net_amount'] = orders['net_amount'].abs()
        orders['gross_amount'] = orders['gross_amount'].abs()
        orders['discount_amount'] = orders['discount_amount'].abs()
        
        # 7. Convert date columns
        customers['signup_date'] = pd.to_datetime(customers['signup_date'])
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        fulfillment['promised_date'] = pd.to_datetime(fulfillment['promised_date'])
        fulfillment['actual_delivery_date'] = pd.to_datetime(fulfillment['actual_delivery_date'])
        returns['return_date'] = pd.to_datetime(returns['return_date'])
        
        # 8. Fix impossible dates (delivery before order)
        merged_dates = orders[['order_id', 'order_date']].merge(
            fulfillment[['order_id', 'actual_delivery_date']], on='order_id'
        )
        invalid_dates = merged_dates[
            merged_dates['actual_delivery_date'] < merged_dates['order_date']
        ]['order_id'].tolist()
        fulfillment.loc[fulfillment['order_id'].isin(invalid_dates), 'actual_delivery_date'] = pd.NaT
        
        return customers, orders, order_items, fulfillment, returns
        
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.info("Please ensure all CSV files are in the same directory as app.py")
        st.stop()

# Load data
customers_df, orders_df, order_items_df, fulfillment_df, returns_df = load_data()

# ================================================================================
# HELPER FUNCTIONS FOR KPI CALCULATIONS
# ================================================================================

def calculate_kpis(orders, customers, fulfillment, returns, order_items):
    """Calculate all KPIs from the KPI Dictionary"""
    
    kpis = {}
    
    # Filter delivered orders for revenue calculations
    delivered_orders = orders[orders['order_status'] == 'Delivered']
    
    # 1. Total Revenue (AED)
    kpis['total_revenue'] = delivered_orders['net_amount'].sum()
    
    # 2. Average Order Value (AOV)
    kpis['aov'] = delivered_orders['net_amount'].mean() if len(delivered_orders) > 0 else 0
    
    # 3. Discount Rate (%)
    total_gross = orders['gross_amount'].sum()
    total_discount = orders['discount_amount'].sum()
    kpis['discount_rate'] = (total_discount / total_gross * 100) if total_gross > 0 else 0
    
    # 4. Repeat Customer Rate (%)
    customer_order_counts = orders.groupby('customer_id').size()
    repeat_customers = (customer_order_counts >= 2).sum()
    total_active_customers = len(customer_order_counts)
    kpis['repeat_customer_rate'] = (repeat_customers / total_active_customers * 100) if total_active_customers > 0 else 0
    
    # 5. Total Orders
    kpis['total_orders'] = len(orders)
    
    # 6. Total Customers
    kpis['total_customers'] = len(customers)
    
    # 7. Cancellation Rate (%)
    cancelled_orders = len(orders[orders['order_status'] == 'Cancelled'])
    kpis['cancellation_rate'] = (cancelled_orders / len(orders) * 100) if len(orders) > 0 else 0
    
    # 8. Return Rate (%)
    returned_orders = len(returns)
    kpis['return_rate'] = (returned_orders / len(delivered_orders) * 100) if len(delivered_orders) > 0 else 0
    
    # 9. On-Time Delivery Rate (%)
    delivered_fulfillment = fulfillment[fulfillment['actual_delivery_date'].notna()]
    on_time = delivered_fulfillment[
        delivered_fulfillment['actual_delivery_date'] <= delivered_fulfillment['promised_date']
    ]
    kpis['on_time_delivery_rate'] = (len(on_time) / len(delivered_fulfillment) * 100) if len(delivered_fulfillment) > 0 else 0
    
    # 10. SLA Breach Count
    kpis['sla_breach_count'] = len(delivered_fulfillment) - len(on_time)
    
    # 11. Average Delay Days
    delayed = delivered_fulfillment[
        delivered_fulfillment['actual_delivery_date'] > delivered_fulfillment['promised_date']
    ].copy()
    if len(delayed) > 0:
        delayed['delay_days'] = (delayed['actual_delivery_date'] - delayed['promised_date']).dt.days
        kpis['avg_delay_days'] = delayed['delay_days'].mean()
    else:
        kpis['avg_delay_days'] = 0
    
    # 12. Total Refund Amount (AED)
    kpis['total_refunds'] = returns[returns['refund_status'] == 'Processed']['refund_amount'].sum()
    
    # 13. Customer Lifetime Value (CLV) - Premium Focus
    customer_revenue = orders.merge(customers[['customer_id', 'customer_segment']], on='customer_id')
    clv_by_segment = customer_revenue.groupby('customer_segment')['net_amount'].mean()
    kpis['clv_vip'] = clv_by_segment.get('VIP', 0)
    kpis['clv_premium'] = clv_by_segment.get('Premium', 0)
    kpis['clv_regular'] = clv_by_segment.get('Regular', 0)
    
    return kpis

def calculate_segment_metrics(orders, customers):
    """Calculate metrics by customer segment for premium focus"""
    
    merged = orders.merge(customers[['customer_id', 'customer_segment']], on='customer_id')
    
    segment_metrics = merged.groupby('customer_segment').agg({
        'net_amount': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    }).round(2)
    
    segment_metrics.columns = ['Total Revenue', 'AOV', 'Order Count', 'Unique Customers']
    segment_metrics = segment_metrics.reset_index()
    
    return segment_metrics

# ================================================================================
# SIDEBAR FILTERS
# ================================================================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='color: #c9a227; font-size: 1.8rem;'>💎 LUXURY</h1>
    <h3 style='color: #f5f5f5; font-size: 1rem; letter-spacing: 3px;'>E-COMMERCE ANALYTICS</h3>
</div>
<div class='gold-divider'></div>
""", unsafe_allow_html=True)

st.sidebar.header("🎯 Filters")

# Date Range Filter
st.sidebar.subheader("📅 Date Range")
min_date = orders_df['order_date'].min().date()
max_date = orders_df['order_date'].max().date()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)

# Customer Segment Filter
st.sidebar.subheader("👑 Customer Tier")
segments = ['All'] + list(customers_df['customer_segment'].unique())
selected_segment = st.sidebar.selectbox("Select Segment", segments)

# Product Category Filter
st.sidebar.subheader("🛍️ Product Category")
categories = ['All'] + list(order_items_df['product_category'].unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=['All']
)

# City Filter
st.sidebar.subheader("📍 City")
cities = ['All'] + list(customers_df['city'].unique())
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    cities,
    default=['All']
)

# Order Channel Filter
st.sidebar.subheader("📱 Order Channel")
channels = ['All'] + list(orders_df['order_channel'].unique())
selected_channel = st.sidebar.selectbox("Select Channel", channels)

# ================================================================================
# APPLY FILTERS
# ================================================================================

# Filter orders by date
filtered_orders = orders_df[
    (orders_df['order_date'].dt.date >= start_date) &
    (orders_df['order_date'].dt.date <= end_date)
].copy()

# Filter by customer segment
if selected_segment != 'All':
    segment_customers = customers_df[customers_df['customer_segment'] == selected_segment]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(segment_customers)]

# Filter by city
if 'All' not in selected_cities:
    city_customers = customers_df[customers_df['city'].isin(selected_cities)]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(city_customers)]

# Filter by channel
if selected_channel != 'All':
    filtered_orders = filtered_orders[filtered_orders['order_channel'] == selected_channel]

# Filter order items
filtered_order_items = order_items_df[order_items_df['order_id'].isin(filtered_orders['order_id'])]

# Filter by category
if 'All' not in selected_categories:
    filtered_order_items = filtered_order_items[
        filtered_order_items['product_category'].isin(selected_categories)
    ]
    # Update filtered orders based on category filter
    filtered_orders = filtered_orders[
        filtered_orders['order_id'].isin(filtered_order_items['order_id'])
    ]

# Filter fulfillment and returns
filtered_fulfillment = fulfillment_df[fulfillment_df['order_id'].isin(filtered_orders['order_id'])]
filtered_returns = returns_df[returns_df['order_id'].isin(filtered_orders['order_id'])]

# Filtered customers
filtered_customer_ids = filtered_orders['customer_id'].unique()
filtered_customers = customers_df[customers_df['customer_id'].isin(filtered_customer_ids)]

# ================================================================================
# CALCULATE KPIS WITH FILTERED DATA
# ================================================================================

kpis = calculate_kpis(
    filtered_orders, 
    filtered_customers, 
    filtered_fulfillment, 
    filtered_returns,
    filtered_order_items
)

# ================================================================================
# MAIN DASHBOARD HEADER
# ================================================================================

st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 class='premium-header'>💎 LUXURY E-COMMERCE ANALYTICS</h1>
    <p style='color: #f5f5f5; font-size: 1.1rem; letter-spacing: 2px;'>
        EXECUTIVE DASHBOARD | UAE PREMIUM RETAIL
    </p>
</div>
<div class='gold-divider'></div>
""", unsafe_allow_html=True)

# ================================================================================
# TAB NAVIGATION
# ================================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "💰 Revenue Analytics", 
    "👥 Customer Intelligence",
    "🚚 Operations & Fulfillment",
    "↩️ Returns Analysis"
])

# ================================================================================
# TAB 1: EXECUTIVE OVERVIEW
# ================================================================================

with tab1:
    st.markdown("### 🎯 Key Performance Indicators")
    
    # Row 1: Primary KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-value'>AED {kpis['total_revenue']:,.0f}</div>
            <div class='kpi-delta-positive'>▲ Delivered Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Average Order Value</div>
            <div class='kpi-value'>AED {kpis['aov']:,.0f}</div>
            <div class='kpi-delta-positive'>Premium Indicator</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Total Orders</div>
            <div class='kpi-value'>{kpis['total_orders']:,}</div>
            <div class='kpi-delta-positive'>Filtered Period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Active Customers</div>
            <div class='kpi-value'>{len(filtered_customers):,}</div>
            <div class='kpi-delta-positive'>Unique Buyers</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Row 2: Secondary KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        color = 'kpi-delta-positive' if kpis['repeat_customer_rate'] > 30 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Repeat Customer Rate</div>
            <div class='kpi-value'>{kpis['repeat_customer_rate']:.1f}%</div>
            <div class='{color}'>Loyalty Metric</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = 'kpi-delta-positive' if kpis['on_time_delivery_rate'] > 80 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>On-Time Delivery</div>
            <div class='kpi-value'>{kpis['on_time_delivery_rate']:.1f}%</div>
            <div class='{color}'>SLA Performance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = 'kpi-delta-positive' if kpis['cancellation_rate'] < 10 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Cancellation Rate</div>
            <div class='kpi-value'>{kpis['cancellation_rate']:.1f}%</div>
            <div class='{color}'>Order Health</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = 'kpi-delta-positive' if kpis['return_rate'] < 15 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Return Rate</div>
            <div class='kpi-value'>{kpis['return_rate']:.1f}%</div>
            <div class='{color}'>Quality Indicator</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Revenue Trend")
        daily_revenue = filtered_orders[filtered_orders['order_status'] == 'Delivered'].groupby(
            filtered_orders['order_date'].dt.date
        )['net_amount'].sum().reset_index()
        daily_revenue.columns = ['Date', 'Revenue']
        
        fig = px.area(
            daily_revenue,
            x='Date',
            y='Revenue',
            title='',
            color_discrete_sequence=['#c9a227']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Revenue (AED)'),
            hovermode='x unified'
        )
        fig.update_traces(
            fill='tozeroy',
            fillcolor='rgba(201,162,39,0.3)',
            line=dict(color='#c9a227', width=2)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏙️ Revenue by City")
        city_revenue = filtered_orders.merge(
            customers_df[['customer_id', 'city']], on='customer_id'
        ).groupby('city')['net_amount'].sum().reset_index()
        city_revenue.columns = ['City', 'Revenue']
        
        fig = px.pie(
            city_revenue,
            values='Revenue',
            names='City',
            title='',
            color_discrete_sequence=['#c9a227', '#f4d03f', '#8b7355', '#d4af37', '#b8860b'],
            hole=0.4
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            legend=dict(orientation='h', yanchor='bottom', y=-0.2)
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Order Status Distribution
    st.markdown("### 📊 Order Status Distribution")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        status_dist = filtered_orders['order_status'].value_counts().reset_index()
        status_dist.columns = ['Status', 'Count']
        
        fig = px.bar(
            status_dist,
            x='Status',
            y='Count',
            color='Status',
            color_discrete_map={
                'Delivered': '#4ade80',
                'In Transit': '#c9a227',
                'Cancelled': '#f87171',
                'Returned': '#fb923c'
            }
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            showlegend=False,
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Status Summary")
        for _, row in status_dist.iterrows():
            pct = row['Count'] / len(filtered_orders) * 100
            st.markdown(f"""
            <div style='padding: 10px; margin: 5px 0; background: rgba(201,162,39,0.1); border-radius: 5px;'>
                <span style='color: #c9a227; font-weight: bold;'>{row['Status']}</span>
                <span style='color: #f5f5f5; float: right;'>{row['Count']:,} ({pct:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)

# ================================================================================
# TAB 2: REVENUE ANALYTICS
# ================================================================================

with tab2:
    st.markdown("### 💰 Revenue Analytics Dashboard")
    
    # Category Revenue Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛍️ Revenue by Product Category")
        category_revenue = filtered_order_items.groupby('product_category')['item_total'].sum().reset_index()
        category_revenue.columns = ['Category', 'Revenue']
        category_revenue = category_revenue.sort_values('Revenue', ascending=True)
        
        fig = px.bar(
            category_revenue,
            x='Revenue',
            y='Category',
            orientation='h',
            color='Revenue',
            color_continuous_scale=['#8b7355', '#c9a227', '#f4d03f']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Revenue (AED)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📱 Revenue by Channel")
        channel_revenue = filtered_orders[filtered_orders['order_status'] == 'Delivered'].groupby(
            'order_channel'
        )['net_amount'].sum().reset_index()
        channel_revenue.columns = ['Channel', 'Revenue']
        
        fig = px.pie(
            channel_revenue,
            values='Revenue',
            names='Channel',
            color_discrete_sequence=['#c9a227', '#f4d03f', '#8b7355'],
            hole=0.5
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5'
        )
        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Payment Methods Analysis
    st.markdown("#### 💳 Payment Method Analysis")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        payment_analysis = filtered_orders.groupby('payment_method').agg({
            'net_amount': ['sum', 'mean', 'count']
        }).round(2)
        payment_analysis.columns = ['Total Revenue', 'Avg Order Value', 'Transaction Count']
        payment_analysis = payment_analysis.reset_index()
        
        fig = px.bar(
            payment_analysis,
            x='payment_method',
            y=['Total Revenue', 'Avg Order Value'],
            barmode='group',
            color_discrete_sequence=['#c9a227', '#f4d03f']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            xaxis_title='Payment Method',
            yaxis_title='Amount (AED)',
            legend_title='Metric',
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Top Payment Method")
        top_payment = payment_analysis.loc[payment_analysis['Total Revenue'].idxmax()]
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Most Used</div>
            <div class='kpi-value' style='font-size: 1.5rem;'>{top_payment['payment_method']}</div>
            <div style='color: #f5f5f5;'>AED {top_payment['Total Revenue']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("##### Highest AOV")
        highest_aov = payment_analysis.loc[payment_analysis['Avg Order Value'].idxmax()]
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Best AOV</div>
            <div class='kpi-value' style='font-size: 1.5rem;'>{highest_aov['payment_method']}</div>
            <div style='color: #f5f5f5;'>AED {highest_aov['Avg Order Value']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Discount Analysis
    st.markdown("#### 🏷️ Discount Performance")
    col1, col2 = st.columns(2)
    
    with col1:
        # Discount distribution
        filtered_orders_copy = filtered_orders.copy()
        filtered_orders_copy['discount_pct'] = (filtered_orders_copy['discount_amount'] / filtered_orders_copy['gross_amount'] * 100).fillna(0)
        filtered_orders_copy['discount_bucket'] = pd.cut(
            filtered_orders_copy['discount_pct'],
            bins=[-1, 0, 5, 15, 30, 100],
            labels=['No Discount', '0-5%', '5-15%', '15-30%', '30%+']
        )
        discount_dist = filtered_orders_copy['discount_bucket'].value_counts().reset_index()
        discount_dist.columns = ['Discount Range', 'Count']
        
        fig = px.pie(
            discount_dist,
            values='Count',
            names='Discount Range',
            color_discrete_sequence=['#1a1a2e', '#4a4a5e', '#8b7355', '#c9a227', '#f4d03f']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            title='Orders by Discount Range'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Coupon performance
        coupon_orders = filtered_orders[filtered_orders['coupon_code'].notna()]
        if len(coupon_orders) > 0:
            coupon_performance = coupon_orders.groupby('coupon_code').agg({
                'net_amount': 'sum',
                'order_id': 'count',
                'discount_amount': 'sum'
            }).round(2)
            coupon_performance.columns = ['Revenue', 'Usage Count', 'Discount Given']
            coupon_performance = coupon_performance.sort_values('Revenue', ascending=False).head(5).reset_index()
            
            st.markdown("##### Top Coupon Codes Performance")
            display_coupon = coupon_performance.copy()
            display_coupon['Revenue'] = display_coupon['Revenue'].apply(lambda x: f"AED {x:,.0f}")
            display_coupon['Discount Given'] = display_coupon['Discount Given'].apply(lambda x: f"AED {x:,.0f}")
            st.dataframe(display_coupon, use_container_width=True)
        else:
            st.info("No coupon data available for the selected period.")

# ================================================================================
# TAB 3: CUSTOMER INTELLIGENCE
# ================================================================================

with tab3:
    st.markdown("### 👥 Customer Intelligence & Segmentation")
    
    # Premium Segment Focus
    st.markdown("#### 👑 Customer Lifetime Value by Segment")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-box' style='border-color: #ffd700;'>
            <div class='kpi-label'>👑 VIP CLV</div>
            <div class='kpi-value'>AED {kpis['clv_vip']:,.0f}</div>
            <div style='color: #ffd700;'>Top Tier Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-box' style='border-color: #c0c0c0;'>
            <div class='kpi-label'>⭐ Premium CLV</div>
            <div class='kpi-value'>AED {kpis['clv_premium']:,.0f}</div>
            <div style='color: #c0c0c0;'>High Value Segment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-box' style='border-color: #cd7f32;'>
            <div class='kpi-label'>🔹 Regular CLV</div>
            <div class='kpi-value'>AED {kpis['clv_regular']:,.0f}</div>
            <div style='color: #cd7f32;'>Growth Opportunity</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Segment Deep Dive
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Segment Performance Matrix")
        segment_metrics = calculate_segment_metrics(filtered_orders, customers_df)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Total Revenue',
            x=segment_metrics['customer_segment'],
            y=segment_metrics['Total Revenue'],
            marker_color='#c9a227'
        ))
        fig.add_trace(go.Scatter(
            name='AOV',
            x=segment_metrics['customer_segment'],
            y=segment_metrics['AOV'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#f4d03f', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            yaxis=dict(title='Revenue (AED)', gridcolor='rgba(201,162,39,0.1)'),
            yaxis2=dict(title='AOV (AED)', overlaying='y', side='right', gridcolor='rgba(201,162,39,0.1)'),
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Customer Distribution by City")
        city_customers = filtered_customers['city'].value_counts().reset_index()
        city_customers.columns = ['City', 'Customers']
        
        fig = px.bar(
            city_customers,
            x='City',
            y='Customers',
            color='Customers',
            color_continuous_scale=['#8b7355', '#c9a227', '#f4d03f']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Customer Acquisition Analysis
    st.markdown("#### 📈 Customer Acquisition Trend")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        monthly_signups = filtered_customers.groupby(
            filtered_customers['signup_date'].dt.to_period('M')
        ).size().reset_index()
        monthly_signups.columns = ['Month', 'New Customers']
        monthly_signups['Month'] = monthly_signups['Month'].astype(str)
        
        fig = px.line(
            monthly_signups,
            x='Month',
            y='New Customers',
            markers=True,
            color_discrete_sequence=['#c9a227']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Signup Channels")
        channel_signups = filtered_customers['signup_channel'].value_counts().reset_index()
        channel_signups.columns = ['Channel', 'Count']
        
        for _, row in channel_signups.iterrows():
            pct = row['Count'] / len(filtered_customers) * 100
            st.markdown(f"""
            <div style='padding: 12px; margin: 8px 0; background: rgba(201,162,39,0.1); 
                        border-left: 3px solid #c9a227; border-radius: 0 5px 5px 0;'>
                <span style='color: #c9a227; font-weight: bold;'>{row['Channel']}</span><br>
                <span style='color: #f5f5f5; font-size: 1.2rem;'>{row['Count']:,}</span>
                <span style='color: #888; font-size: 0.9rem;'> ({pct:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Top Customers Table
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### 🏆 Top 10 Customers by Revenue")
    
    top_customers = filtered_orders.groupby('customer_id').agg({
        'net_amount': 'sum',
        'order_id': 'count'
    }).reset_index()
    top_customers.columns = ['Customer ID', 'Total Spent', 'Order Count']
    top_customers = top_customers.merge(
        customers_df[['customer_id', 'customer_name', 'customer_segment', 'city']],
        left_on='Customer ID',
        right_on='customer_id'
    ).drop('customer_id', axis=1)
    top_customers = top_customers.sort_values('Total Spent', ascending=False).head(10)
    top_customers = top_customers[['Customer ID', 'customer_name', 'customer_segment', 'city', 'Total Spent', 'Order Count']]
    top_customers.columns = ['ID', 'Name', 'Segment', 'City', 'Total Spent (AED)', 'Orders']
    
    # Format the display dataframe
    display_df = top_customers.copy()
    display_df['Total Spent (AED)'] = display_df['Total Spent (AED)'].apply(lambda x: f"AED {x:,.2f}")
    
    st.dataframe(display_df, use_container_width=True)

# ================================================================================
# TAB 4: OPERATIONS & FULFILLMENT
# ================================================================================

with tab4:
    st.markdown("### 🚚 Operations & Fulfillment Performance")
    
    # Delivery KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>On-Time Delivery</div>
            <div class='kpi-value'>{kpis['on_time_delivery_rate']:.1f}%</div>
            <div class='kpi-delta-positive'>Target: 85%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>SLA Breaches</div>
            <div class='kpi-value'>{kpis['sla_breach_count']:,}</div>
            <div class='kpi-delta-negative'>Needs Attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Avg Delay Days</div>
            <div class='kpi-value'>{kpis['avg_delay_days']:.1f}</div>
            <div class='kpi-delta-negative'>For Late Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pending_count = len(filtered_fulfillment[filtered_fulfillment['delivery_status'] == 'Pending'])
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Pending Deliveries</div>
            <div class='kpi-value'>{pending_count:,}</div>
            <div style='color: #c9a227;'>In Pipeline</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Delivery Status and Partner Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Delivery Status Distribution")
        status_dist = filtered_fulfillment['delivery_status'].value_counts().reset_index()
        status_dist.columns = ['Status', 'Count']
        
        colors = {
            'On Time': '#4ade80',
            'Delayed': '#fb923c',
            'Failed': '#f87171',
            'Pending': '#c9a227'
        }
        
        fig = px.pie(
            status_dist,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map=colors,
            hole=0.4
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏢 Warehouse Hub Performance")
        hub_performance = filtered_fulfillment.groupby('warehouse_hub').agg({
            'order_id': 'count',
            'delivery_status': lambda x: (x == 'On Time').sum() / len(x) * 100 if len(x) > 0 else 0
        }).reset_index()
        hub_performance.columns = ['Warehouse', 'Total Orders', 'On-Time %']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Total Orders',
            x=hub_performance['Warehouse'],
            y=hub_performance['Total Orders'],
            marker_color='#c9a227'
        ))
        fig.add_trace(go.Scatter(
            name='On-Time %',
            x=hub_performance['Warehouse'],
            y=hub_performance['On-Time %'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#4ade80', width=3),
            marker=dict(size=12)
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            yaxis=dict(title='Orders', gridcolor='rgba(201,162,39,0.1)'),
            yaxis2=dict(title='On-Time %', overlaying='y', side='right', range=[0, 100]),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Delay Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚠️ Delay Reasons Breakdown")
        delay_data = filtered_fulfillment[
            filtered_fulfillment['delay_reason'].notna() & 
            (filtered_fulfillment['delay_reason'] != 'Order Cancelled')
        ]
        if len(delay_data) > 0:
            delay_reasons = delay_data['delay_reason'].value_counts().reset_index()
            delay_reasons.columns = ['Reason', 'Count']
            
            fig = px.bar(
                delay_reasons,
                x='Count',
                y='Reason',
                orientation='h',
                color='Count',
                color_continuous_scale=['#8b7355', '#c9a227', '#f4d03f']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
                yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No delay data available for the selected period.")
    
    with col2:
        st.markdown("#### 🚛 Delivery Partner Performance")
        partner_perf = filtered_fulfillment.groupby('delivery_partner').agg({
            'order_id': 'count',
            'delivery_status': lambda x: (x == 'On Time').sum() / len(x) * 100 if len(x) > 0 else 0
        }).reset_index()
        partner_perf.columns = ['Partner', 'Deliveries', 'On-Time %']
        partner_perf = partner_perf.sort_values('On-Time %', ascending=False)
        
        fig = px.bar(
            partner_perf,
            x='Partner',
            y='On-Time %',
            color='On-Time %',
            color_continuous_scale=['#f87171', '#fb923c', '#4ade80'],
            text='On-Time %'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)', range=[0, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Delivery Zone Analysis
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### 📍 Delivery Zone Performance")
    
    zone_data = filtered_fulfillment[filtered_fulfillment['delivery_zone'] != 'Unknown']
    if len(zone_data) > 0:
        zone_perf = zone_data.groupby('delivery_zone').agg({
            'order_id': 'count',
            'delivery_status': lambda x: (x == 'On Time').sum() / len(x) * 100 if len(x) > 0 else 0
        }).reset_index()
        zone_perf.columns = ['Zone', 'Total Deliveries', 'On-Time Rate']
        zone_perf = zone_perf.sort_values('Zone')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=zone_perf['Zone'],
            y=zone_perf['Total Deliveries'],
            name='Deliveries',
            marker_color='#c9a227'
        ))
        fig.add_trace(go.Scatter(
            x=zone_perf['Zone'],
            y=zone_perf['On-Time Rate'],
            name='On-Time %',
            yaxis='y2',
            mode='lines+markers+text',
            text=[f'{v:.0f}%' for v in zone_perf['On-Time Rate']],
            textposition='top center',
            line=dict(color='#4ade80', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            yaxis=dict(title='Total Deliveries', gridcolor='rgba(201,162,39,0.1)'),
            yaxis2=dict(title='On-Time %', overlaying='y', side='right', range=[0, 100]),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No delivery zone data available for the selected period.")

# ================================================================================
# TAB 5: RETURNS ANALYSIS
# ================================================================================

with tab5:
    st.markdown("### ↩️ Returns & Refunds Analysis")
    
    # Returns KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Return Rate</div>
            <div class='kpi-value'>{kpis['return_rate']:.1f}%</div>
            <div class='kpi-delta-negative'>Of Delivered Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Total Returns</div>
            <div class='kpi-value'>{len(filtered_returns):,}</div>
            <div style='color: #fb923c;'>Items Returned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Refunds Processed</div>
            <div class='kpi-value'>AED {kpis['total_refunds']:,.0f}</div>
            <div class='kpi-delta-negative'>Total Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_refund = filtered_returns['refund_amount'].mean() if len(filtered_returns) > 0 else 0
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Avg Refund Value</div>
            <div class='kpi-value'>AED {avg_refund:,.0f}</div>
            <div style='color: #c9a227;'>Per Return</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Return Reasons and Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Return Reasons")
        if len(filtered_returns) > 0:
            reason_dist = filtered_returns['return_reason'].value_counts().reset_index()
            reason_dist.columns = ['Reason', 'Count']
            
            fig = px.pie(
                reason_dist,
                values='Count',
                names='Reason',
                color_discrete_sequence=['#c9a227', '#f4d03f', '#8b7355', '#d4af37', '#b8860b'],
                hole=0.4
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No return data available for the selected filters.")
    
    with col2:
        st.markdown("#### 💰 Refund Status")
        if len(filtered_returns) > 0:
            refund_status = filtered_returns.groupby('refund_status').agg({
                'return_id': 'count',
                'refund_amount': 'sum'
            }).reset_index()
            refund_status.columns = ['Status', 'Count', 'Total Amount']
            
            colors = {'Processed': '#4ade80', 'Pending': '#c9a227', 'Rejected': '#f87171'}
            
            fig = px.bar(
                refund_status,
                x='Status',
                y='Total Amount',
                color='Status',
                color_discrete_map=colors,
                text='Count'
            )
            fig.update_traces(texttemplate='%{text} returns', textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                showlegend=False,
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
                yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Refund Amount (AED)')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No return data available for the selected filters.")
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # Returns by Category
    st.markdown("#### 🛍️ Returns by Product Category")
    
    if len(filtered_returns) > 0:
        returns_with_items = filtered_returns.merge(
            filtered_order_items[['order_id', 'product_category', 'item_total']].drop_duplicates('order_id'),
            on='order_id',
            how='left'
        )
        
        category_returns = returns_with_items.groupby('product_category').agg({
            'return_id': 'count',
            'refund_amount': 'sum'
        }).reset_index()
        category_returns.columns = ['Category', 'Return Count', 'Refund Amount']
        category_returns = category_returns.sort_values('Return Count', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                category_returns,
                x='Category',
                y='Return Count',
                color='Return Count',
                color_continuous_scale=['#8b7355', '#c9a227', '#f4d03f']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)'),
                yaxis=dict(gridcolor='rgba(201,162,39,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Return rate by category
            category_orders = filtered_order_items.groupby('product_category')['order_id'].nunique().reset_index()
            category_orders.columns = ['Category', 'Total Orders']
            
            return_rate_by_cat = category_returns.merge(category_orders, on='Category')
            return_rate_by_cat['Return Rate'] = (
                return_rate_by_cat['Return Count'] / return_rate_by_cat['Total Orders'] * 100
            ).round(2)
            
            st.markdown("##### Return Rate by Category")
            for _, row in return_rate_by_cat.iterrows():
                color = '#4ade80' if row['Return Rate'] < 10 else '#fb923c' if row['Return Rate'] < 20 else '#f87171'
                st.markdown(f"""
                <div style='padding: 12px; margin: 8px 0; background: rgba(201,162,39,0.1); 
                            border-left: 3px solid {color}; border-radius: 0 5px 5px 0;'>
                    <span style='color: #c9a227; font-weight: bold;'>{row['Category']}</span><br>
                    <span style='color: {color}; font-size: 1.3rem; font-weight: bold;'>{row['Return Rate']:.1f}%</span>
                    <span style='color: #888;'> ({row['Return Count']} of {row['Total Orders']} orders)</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No return data available for the selected filters.")
    
    # Returns Trend
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### 📈 Returns Trend Over Time")
    
    if len(filtered_returns) > 0:
        daily_returns = filtered_returns.groupby(
            filtered_returns['return_date'].dt.date
        ).agg({
            'return_id': 'count',
            'refund_amount': 'sum'
        }).reset_index()
        daily_returns.columns = ['Date', 'Returns', 'Refund Amount']
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(name='Returns', x=daily_returns['Date'], y=daily_returns['Returns'],
                   marker_color='#c9a227'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(name='Refund Amount', x=daily_returns['Date'], y=daily_returns['Refund Amount'],
                       mode='lines', line=dict(color='#f87171', width=2)),
            secondary_y=True
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            hovermode='x unified'
        )
        fig.update_xaxes(gridcolor='rgba(201,162,39,0.1)')
        fig.update_yaxes(title_text='Return Count', secondary_y=False, gridcolor='rgba(201,162,39,0.1)')
        fig.update_yaxes(title_text='Refund Amount (AED)', secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No return data available for the selected filters.")

# ================================================================================
# FOOTER
# ================================================================================

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 30px 0; color: #888;'>
    <p style='letter-spacing: 3px; font-size: 0.8rem;'>
        💎 LUXURY E-COMMERCE ANALYTICS PLATFORM 💎
    </p>
    <p style='font-size: 0.7rem;'>
        Built with Streamlit | Data refreshed in real-time | © 2024 Premium Retail Analytics
    </p>
</div>
""", unsafe_allow_html=True)
