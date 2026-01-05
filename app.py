"""
================================================================================
LUXURY E-COMMERCE ANALYTICS DASHBOARD
================================================================================
Complete Version with Executive & Manager Views + What-If Analysis
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
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%);
        border-right: 1px solid #c9a227;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #f5f5f5;
    }
    
    h1, h2, h3 {
        color: #c9a227 !important;
    }
    
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
    
    .gold-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #c9a227, transparent);
        margin: 20px 0;
    }
    
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
        font-size: 2.2rem;
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
    
    .insight-box {
        background: rgba(201, 162, 39, 0.1);
        border: 1px solid #c9a227;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .insight-title {
        color: #c9a227;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    
    .insight-text {
        color: #f5f5f5;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .whatif-box {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), rgba(26, 26, 46, 0.9));
        border: 1px solid #4ade80;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .whatif-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #4ade80;
    }
    
    .stRadio > div {
        background-color: rgba(201, 162, 39, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================================
# DATA LOADING AND CLEANING
# ================================================================================

@st.cache_data
def load_data():
    """Load and clean all data files"""
    try:
        customers = pd.read_csv('customers.csv')
        orders = pd.read_csv('orders.csv')
        order_items = pd.read_csv('order_items.csv')
        fulfillment = pd.read_csv('fulfillment.csv')
        returns = pd.read_csv('returns.csv')
        
        # Remove duplicates
        customers = customers.drop_duplicates(subset=['customer_id'], keep='first')
        orders = orders.drop_duplicates(subset=['order_id'], keep='first')
        
        # Standardize city names
        city_mapping = {
            'DUBAI': 'Dubai', 'dubai': 'Dubai', 'Dxb': 'Dubai',
            'ABU DHABI': 'Abu Dhabi', 'abu dhabi': 'Abu Dhabi', 'AD': 'Abu Dhabi',
            'SHARJAH': 'Sharjah', 'sharjah': 'Sharjah', 'SHJ': 'Sharjah',
            'AJMAN': 'Ajman', 'ajman': 'Ajman',
            'RAS AL KHAIMAH': 'Ras Al Khaimah', 'ras al khaimah': 'Ras Al Khaimah', 'RAK': 'Ras Al Khaimah'
        }
        customers['city'] = customers['city'].replace(city_mapping)
        
        # Standardize category names
        category_mapping = {
            'electronics': 'Electronics', 'ELECTRONICS': 'Electronics',
            'fashion': 'Fashion', 'FASHION': 'Fashion',
            'home & kitchen': 'Home & Kitchen', 'HOME & KITCHEN': 'Home & Kitchen',
            'beauty': 'Beauty', 'BEAUTY': 'Beauty',
            'groceries': 'Groceries', 'GROCERIES': 'Groceries'
        }
        order_items['product_category'] = order_items['product_category'].replace(category_mapping)
        
        # Handle missing values
        orders['discount_amount'] = orders['discount_amount'].fillna(0)
        fulfillment['delivery_zone'] = fulfillment['delivery_zone'].fillna('Unknown')
        returns['return_reason'] = returns['return_reason'].fillna('Not Specified')
        
        # Fix amounts
        orders['net_amount'] = orders['net_amount'].abs()
        orders['gross_amount'] = orders['gross_amount'].abs()
        orders['discount_amount'] = orders['discount_amount'].abs()
        
        # Convert dates
        customers['signup_date'] = pd.to_datetime(customers['signup_date'])
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        fulfillment['promised_date'] = pd.to_datetime(fulfillment['promised_date'])
        fulfillment['actual_delivery_date'] = pd.to_datetime(fulfillment['actual_delivery_date'])
        returns['return_date'] = pd.to_datetime(returns['return_date'])
        
        return customers, orders, order_items, fulfillment, returns
        
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.info("Please ensure all CSV files (customers.csv, orders.csv, order_items.csv, fulfillment.csv, returns.csv) are in the same directory.")
        st.stop()

# Load data
customers_df, orders_df, order_items_df, fulfillment_df, returns_df = load_data()

# ================================================================================
# SIDEBAR - FILTERS
# ================================================================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='color: #c9a227; font-size: 1.8rem;'>💎 LUXURY</h1>
    <h3 style='color: #f5f5f5; font-size: 1rem; letter-spacing: 3px;'>E-COMMERCE ANALYTICS</h3>
</div>
<div class='gold-divider'></div>
""", unsafe_allow_html=True)

# View Toggle
st.sidebar.markdown("### 🔄 Dashboard View")
view_mode = st.sidebar.radio(
    "Select View",
    ["Executive View", "Manager View"],
    index=0,
    help="Toggle between Executive and Manager dashboards"
)

st.sidebar.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
st.sidebar.header("🎯 Filters")

# Filter 1: Date Range
st.sidebar.subheader("📅 Date Range")
min_date = orders_df['order_date'].min().date()
max_date = orders_df['order_date'].max().date()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)

# Filter 2: City Multi-select
st.sidebar.subheader("🏙️ City")
available_cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Ras Al Khaimah']
city_options = [c for c in available_cities if c in customers_df['city'].unique()]
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=city_options,
    default=city_options,
    help="Filter by customer city"
)

# Filter 3: Order Channel
st.sidebar.subheader("📱 Order Channel")
channel_options = list(orders_df['order_channel'].unique())
selected_channels = st.sidebar.multiselect(
    "Select Channels",
    options=channel_options,
    default=channel_options,
    help="App, Web, Call Center"
)

# Filter 4: Product Category
st.sidebar.subheader("🛍️ Product Category")
category_options = list(order_items_df['product_category'].unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=category_options,
    default=category_options,
    help="Electronics, Fashion, Home & Kitchen, Beauty, Groceries"
)

# Filter 5: Customer Segment
st.sidebar.subheader("👑 Customer Segment")
segment_options = list(customers_df['customer_segment'].unique())
selected_segments = st.sidebar.multiselect(
    "Select Segments",
    options=segment_options,
    default=segment_options,
    help="Regular, Premium, VIP"
)

# Filter 6: Order Status
st.sidebar.subheader("📦 Order Status")
status_options = list(orders_df['order_status'].unique())
selected_statuses = st.sidebar.multiselect(
    "Select Statuses",
    options=status_options,
    default=status_options,
    help="Delivered, Cancelled, Returned, In Transit"
)

# ================================================================================
# APPLY FILTERS
# ================================================================================

# Filter orders by date
filtered_orders = orders_df[
    (orders_df['order_date'].dt.date >= start_date) &
    (orders_df['order_date'].dt.date <= end_date)
].copy()

# Filter by city
if selected_cities:
    city_customers = customers_df[customers_df['city'].isin(selected_cities)]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(city_customers)]

# Filter by channel
if selected_channels:
    filtered_orders = filtered_orders[filtered_orders['order_channel'].isin(selected_channels)]

# Filter by customer segment
if selected_segments:
    segment_customers = customers_df[customers_df['customer_segment'].isin(selected_segments)]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(segment_customers)]

# Filter by order status
if selected_statuses:
    filtered_orders = filtered_orders[filtered_orders['order_status'].isin(selected_statuses)]

# Filter order items by category
filtered_order_items = order_items_df[order_items_df['order_id'].isin(filtered_orders['order_id'])]
if selected_categories:
    filtered_order_items = filtered_order_items[filtered_order_items['product_category'].isin(selected_categories)]
    filtered_orders = filtered_orders[filtered_orders['order_id'].isin(filtered_order_items['order_id'])]

# Get filtered related data
filtered_customer_ids = filtered_orders['customer_id'].unique()
filtered_customers = customers_df[customers_df['customer_id'].isin(filtered_customer_ids)]
filtered_fulfillment = fulfillment_df[fulfillment_df['order_id'].isin(filtered_orders['order_id'])]
filtered_returns = returns_df[returns_df['order_id'].isin(filtered_orders['order_id'])]

# ================================================================================
# KPI CALCULATIONS
# ================================================================================

def calculate_executive_kpis(orders, customers, order_items, previous_orders=None):
    """Calculate Executive View KPIs"""
    kpis = {}
    
    delivered_orders = orders[orders['order_status'] == 'Delivered']
    
    # Total Revenue
    kpis['total_revenue'] = delivered_orders['net_amount'].sum()
    
    # Revenue change (compare to previous period if available)
    if previous_orders is not None and len(previous_orders) > 0:
        prev_delivered = previous_orders[previous_orders['order_status'] == 'Delivered']
        prev_revenue = prev_delivered['net_amount'].sum()
        if prev_revenue > 0:
            kpis['revenue_change'] = ((kpis['total_revenue'] - prev_revenue) / prev_revenue) * 100
        else:
            kpis['revenue_change'] = 0
    else:
        kpis['revenue_change'] = 0
    
    # Average Order Value
    kpis['aov'] = delivered_orders['net_amount'].mean() if len(delivered_orders) > 0 else 0
    
    # Repeat Customer Rate
    customer_order_counts = orders.groupby('customer_id').size()
    repeat_customers = (customer_order_counts >= 2).sum()
    total_active = len(customer_order_counts)
    kpis['repeat_rate'] = (repeat_customers / total_active * 100) if total_active > 0 else 0
    
    # Discount Rate
    total_gross = orders['gross_amount'].sum()
    total_discount = orders['discount_amount'].sum()
    kpis['discount_rate'] = (total_discount / total_gross * 100) if total_gross > 0 else 0
    
    return kpis

def calculate_manager_kpis(orders, fulfillment, returns):
    """Calculate Manager View KPIs"""
    kpis = {}
    
    # On-Time Delivery Rate
    delivered_fulfillment = fulfillment[fulfillment['actual_delivery_date'].notna()]
    on_time = delivered_fulfillment[
        delivered_fulfillment['actual_delivery_date'] <= delivered_fulfillment['promised_date']
    ]
    kpis['on_time_rate'] = (len(on_time) / len(delivered_fulfillment) * 100) if len(delivered_fulfillment) > 0 else 0
    
    # SLA Breach Count
    kpis['sla_breach_count'] = len(delivered_fulfillment) - len(on_time)
    
    # Cancellation Rate
    cancelled = len(orders[orders['order_status'] == 'Cancelled'])
    kpis['cancellation_rate'] = (cancelled / len(orders) * 100) if len(orders) > 0 else 0
    
    # Total Refund Amount
    kpis['total_refunds'] = returns[returns['refund_status'] == 'Processed']['refund_amount'].sum()
    
    # Additional metrics for What-If
    kpis['total_orders'] = len(orders)
    kpis['cancelled_orders'] = cancelled
    kpis['delivered_orders'] = len(orders[orders['order_status'] == 'Delivered'])
    kpis['avg_order_value'] = orders['net_amount'].mean() if len(orders) > 0 else 0
    
    return kpis

# Calculate KPIs
exec_kpis = calculate_executive_kpis(filtered_orders, filtered_customers, filtered_order_items)
mgr_kpis = calculate_manager_kpis(filtered_orders, filtered_fulfillment, filtered_returns)

# ================================================================================
# MAIN HEADER
# ================================================================================

st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='background: linear-gradient(90deg, #c9a227, #f4d03f, #c9a227); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               font-size: 2.5rem; font-weight: bold;'>
        💎 LUXURY E-COMMERCE ANALYTICS
    </h1>
    <p style='color: #f5f5f5; font-size: 1.1rem; letter-spacing: 2px;'>
        UAE PREMIUM RETAIL | {} MODE
    </p>
</div>
<div class='gold-divider'></div>
""".format(view_mode.upper().replace(" VIEW", "")), unsafe_allow_html=True)

# ================================================================================
# EXECUTIVE VIEW
# ================================================================================

if view_mode == "Executive View":
    
    # ===== 4 KPI CARDS =====
    st.markdown("### 🎯 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        change_color = 'kpi-delta-positive' if exec_kpis['revenue_change'] >= 0 else 'kpi-delta-negative'
        change_symbol = '▲' if exec_kpis['revenue_change'] >= 0 else '▼'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-value'>AED {exec_kpis['total_revenue']:,.0f}</div>
            <div class='{change_color}'>{change_symbol} {abs(exec_kpis['revenue_change']):.1f}% vs prev period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Average Order Value</div>
            <div class='kpi-value'>AED {exec_kpis['aov']:,.0f}</div>
            <div class='kpi-delta-positive'>Premium Indicator</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = 'kpi-delta-positive' if exec_kpis['repeat_rate'] > 30 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Repeat Customer Rate</div>
            <div class='kpi-value'>{exec_kpis['repeat_rate']:.1f}%</div>
            <div class='{color}'>Loyalty Metric</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = 'kpi-delta-positive' if exec_kpis['discount_rate'] < 15 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Discount Rate</div>
            <div class='kpi-value'>{exec_kpis['discount_rate']:.1f}%</div>
            <div class='{color}'>Margin Impact</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 1: Daily/Weekly Revenue Trend (Line Chart) =====
    # ===== CHART 2: Revenue by City (Bar Chart) =====
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Revenue Trend")
        
        # Aggregation toggle
        agg_type = st.radio("Aggregation", ["Daily", "Weekly"], horizontal=True, key="rev_agg")
        
        delivered = filtered_orders[filtered_orders['order_status'] == 'Delivered'].copy()
        
        if agg_type == "Daily":
            revenue_trend = delivered.groupby(delivered['order_date'].dt.date)['net_amount'].sum().reset_index()
            revenue_trend.columns = ['Date', 'Revenue']
        else:
            delivered['week'] = delivered['order_date'].dt.to_period('W').apply(lambda x: x.start_time)
            revenue_trend = delivered.groupby('week')['net_amount'].sum().reset_index()
            revenue_trend.columns = ['Date', 'Revenue']
        
        fig = px.line(
            revenue_trend,
            x='Date',
            y='Revenue',
            markers=True,
            color_discrete_sequence=['#c9a227']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)', title=''),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Revenue (AED)'),
            hovermode='x unified'
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏙️ Revenue by City")
        
        city_revenue = filtered_orders.merge(
            customers_df[['customer_id', 'city']], on='customer_id'
        )
        city_revenue = city_revenue[city_revenue['order_status'] == 'Delivered']
        city_revenue = city_revenue.groupby('city')['net_amount'].sum().reset_index()
        city_revenue.columns = ['City', 'Revenue']
        city_revenue = city_revenue.sort_values('Revenue', ascending=True)
        
        fig = px.bar(
            city_revenue,
            x='Revenue',
            y='City',
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
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 3: Channel Contribution (Pie/Donut) =====
    # ===== CHART 4: Category Revenue Mix by City (Stacked Bar) =====
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📱 Channel Contribution")
        
        channel_orders = filtered_orders.groupby('order_channel').agg({
            'order_id': 'count',
            'net_amount': 'sum'
        }).reset_index()
        channel_orders.columns = ['Channel', 'Orders', 'Revenue']
        channel_orders['Percentage'] = (channel_orders['Orders'] / channel_orders['Orders'].sum() * 100).round(1)
        
        fig = px.pie(
            channel_orders,
            values='Orders',
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
    
    with col2:
        st.markdown("### 🛍️ Category Revenue by City")
        
        # Merge orders with customers for city
        orders_with_city = filtered_orders.merge(
            customers_df[['customer_id', 'city']], on='customer_id'
        )
        # Merge with order items for category
        orders_with_details = orders_with_city.merge(
            filtered_order_items[['order_id', 'product_category', 'item_total']],
            on='order_id'
        )
        
        category_city = orders_with_details.groupby(['city', 'product_category'])['item_total'].sum().reset_index()
        category_city.columns = ['City', 'Category', 'Revenue']
        
        fig = px.bar(
            category_city,
            x='City',
            y='Revenue',
            color='Category',
            color_discrete_sequence=['#c9a227', '#f4d03f', '#8b7355', '#d4af37', '#b8860b'],
            barmode='stack'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f5f5',
            xaxis=dict(gridcolor='rgba(201,162,39,0.1)', title=''),
            yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Revenue (AED)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== INSIGHTS BOX =====
    st.markdown("### 💡 Auto-Generated Insights")
    
    # Generate insights
    top_city = city_revenue.iloc[-1]['City'] if len(city_revenue) > 0 else "N/A"
    top_city_rev = city_revenue.iloc[-1]['Revenue'] if len(city_revenue) > 0 else 0
    
    top_channel = channel_orders.loc[channel_orders['Orders'].idxmax()]['Channel'] if len(channel_orders) > 0 else "N/A"
    top_channel_pct = channel_orders.loc[channel_orders['Orders'].idxmax()]['Percentage'] if len(channel_orders) > 0 else 0
    
    avg_discount = exec_kpis['discount_rate']
    
    insights_html = f"""
    <div class='insight-box'>
        <div class='insight-title'>📊 Executive Summary</div>
        <div class='insight-text'>
            <p>• <strong>{top_city}</strong> leads revenue generation with <strong>AED {top_city_rev:,.0f}</strong>, representing the highest performing market.</p>
            <p>• <strong>{top_channel}</strong> channel dominates with <strong>{top_channel_pct:.1f}%</strong> of total orders - consider optimizing other channels.</p>
            <p>• Current discount rate is <strong>{avg_discount:.1f}%</strong> {'- within healthy margins.' if avg_discount < 15 else '- consider reviewing promotional strategy.'}</p>
            <p>• Repeat customer rate of <strong>{exec_kpis['repeat_rate']:.1f}%</strong> {'indicates strong loyalty.' if exec_kpis['repeat_rate'] > 30 else 'suggests opportunity for retention programs.'}</p>
            <p>• Average order value of <strong>AED {exec_kpis['aov']:,.0f}</strong> {'aligns with premium positioning.' if exec_kpis['aov'] > 400 else 'has room for upselling opportunities.'}</p>
        </div>
    </div>
    """
    st.markdown(insights_html, unsafe_allow_html=True)

# ================================================================================
# MANAGER VIEW
# ================================================================================

else:  # Manager View
    
    # ===== 4 KPI CARDS =====
    st.markdown("### 🎯 Operational KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        color = 'kpi-delta-positive' if mgr_kpis['on_time_rate'] > 85 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>On-Time Delivery Rate</div>
            <div class='kpi-value'>{mgr_kpis['on_time_rate']:.1f}%</div>
            <div class='{color}'>Target: 85%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>SLA Breach Count</div>
            <div class='kpi-value'>{mgr_kpis['sla_breach_count']:,}</div>
            <div class='kpi-delta-negative'>Requires Action</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = 'kpi-delta-positive' if mgr_kpis['cancellation_rate'] < 10 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Cancellation Rate</div>
            <div class='kpi-value'>{mgr_kpis['cancellation_rate']:.1f}%</div>
            <div class='{color}'>Target: &lt;10%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Total Refund Amount</div>
            <div class='kpi-value'>AED {mgr_kpis['total_refunds']:,.0f}</div>
            <div class='kpi-delta-negative'>Cost Impact</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 1: SLA Breach Trend (Line Chart) =====
    # ===== CHART 2: SLA Breaches by Zone (Bar Chart - Top 10) =====
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 SLA Breach Trend Over Time")
        
        breach_data = filtered_fulfillment[
            (filtered_fulfillment['actual_delivery_date'].notna()) &
            (filtered_fulfillment['actual_delivery_date'] > filtered_fulfillment['promised_date'])
        ].copy()
        
        if len(breach_data) > 0:
            breach_trend = breach_data.groupby(
                breach_data['actual_delivery_date'].dt.date
            ).size().reset_index()
            breach_trend.columns = ['Date', 'Breaches']
            
            fig = px.line(
                breach_trend,
                x='Date',
                y='Breaches',
                markers=True,
                color_discrete_sequence=['#f87171']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)', title=''),
                yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='SLA Breaches')
            )
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No SLA breaches in selected period.")
    
    with col2:
        st.markdown("### 📍 SLA Breaches by Delivery Zone (Top 10)")
        
        if len(breach_data) > 0:
            zone_breaches = breach_data.groupby('delivery_zone').size().reset_index()
            zone_breaches.columns = ['Zone', 'Breaches']
            zone_breaches = zone_breaches.sort_values('Breaches', ascending=False).head(10)
            zone_breaches = zone_breaches.sort_values('Breaches', ascending=True)
            
            fig = px.bar(
                zone_breaches,
                x='Breaches',
                y='Zone',
                orientation='h',
                color='Breaches',
                color_continuous_scale=['#fb923c', '#f87171']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Number of Breaches'),
                yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No zone data available.")
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 3: Pareto Chart - Delay Reasons =====
    # ===== CHART 4: Return Rate by Category =====
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Delay Reasons (Pareto Analysis)")
        
        delay_data = filtered_fulfillment[
            (filtered_fulfillment['delay_reason'].notna()) &
            (filtered_fulfillment['delay_reason'] != '') &
            (filtered_fulfillment['delay_reason'] != 'Order Cancelled')
        ]
        
        if len(delay_data) > 0:
            delay_reasons = delay_data.groupby('delay_reason').size().reset_index()
            delay_reasons.columns = ['Reason', 'Count']
            delay_reasons = delay_reasons.sort_values('Count', ascending=False)
            delay_reasons['Cumulative'] = delay_reasons['Count'].cumsum()
            delay_reasons['Cumulative %'] = (delay_reasons['Cumulative'] / delay_reasons['Count'].sum() * 100)
            
            # Create Pareto chart
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(
                    x=delay_reasons['Reason'],
                    y=delay_reasons['Count'],
                    name='Count',
                    marker_color='#c9a227'
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=delay_reasons['Reason'],
                    y=delay_reasons['Cumulative %'],
                    name='Cumulative %',
                    mode='lines+markers',
                    line=dict(color='#f87171', width=3),
                    marker=dict(size=8)
                ),
                secondary_y=True
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)', tickangle=45)
            )
            fig.update_yaxes(title_text='Count', secondary_y=False, gridcolor='rgba(201,162,39,0.1)')
            fig.update_yaxes(title_text='Cumulative %', secondary_y=True, range=[0, 100])
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No delay data available.")
    
    with col2:
        st.markdown("### ↩️ Return Rate by Category")
        
        # Get returns by category
        returns_with_cat = filtered_returns.merge(
            filtered_order_items[['order_id', 'product_category']].drop_duplicates('order_id'),
            on='order_id',
            how='left'
        )
        
        category_returns = returns_with_cat.groupby('product_category').size().reset_index()
        category_returns.columns = ['Category', 'Returns']
        
        # Get total orders by category
        category_orders = filtered_order_items.groupby('product_category')['order_id'].nunique().reset_index()
        category_orders.columns = ['Category', 'Orders']
        
        # Calculate return rate
        return_rate = category_returns.merge(category_orders, on='Category')
        return_rate['Return Rate'] = (return_rate['Returns'] / return_rate['Orders'] * 100).round(2)
        return_rate = return_rate.sort_values('Return Rate', ascending=False)
        
        if len(return_rate) > 0:
            fig = px.bar(
                return_rate,
                x='Category',
                y='Return Rate',
                color='Return Rate',
                color_continuous_scale=['#4ade80', '#fb923c', '#f87171'],
                text='Return Rate'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='rgba(201,162,39,0.1)', title=''),
                yaxis=dict(gridcolor='rgba(201,162,39,0.1)', title='Return Rate (%)', range=[0, max(return_rate['Return Rate']) * 1.3])
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No return data available.")
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== SORTABLE TABLE: Top 10 Problem Areas =====
    st.markdown("### 📋 Top 10 Problem Areas")
    
    # Calculate problem areas by zone
    zone_analysis = filtered_fulfillment.copy()
    zone_analysis['is_breach'] = zone_analysis['actual_delivery_date'] > zone_analysis['promised_date']
    zone_analysis['delay_days'] = (zone_analysis['actual_delivery_date'] - zone_analysis['promised_date']).dt.days
    zone_analysis.loc[zone_analysis['delay_days'] < 0, 'delay_days'] = 0
    
    problem_zones = zone_analysis.groupby('delivery_zone').agg({
        'is_breach': 'sum',
        'delay_days': 'mean',
        'delay_reason': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A',
        'order_id': 'count'
    }).reset_index()
    problem_zones.columns = ['Zone', 'Breach Count', 'Avg Delay Days', 'Top Delay Reason', 'Total Orders']
    problem_zones = problem_zones.sort_values('Breach Count', ascending=False).head(10)
    problem_zones['Avg Delay Days'] = problem_zones['Avg Delay Days'].round(1)
    
    st.dataframe(
        problem_zones,
        use_container_width=True,
        column_config={
            "Zone": st.column_config.TextColumn("Delivery Zone"),
            "Breach Count": st.column_config.NumberColumn("SLA Breaches", format="%d"),
            "Avg Delay Days": st.column_config.NumberColumn("Avg Delay (Days)", format="%.1f"),
            "Top Delay Reason": st.column_config.TextColumn("Primary Reason"),
            "Total Orders": st.column_config.NumberColumn("Total Orders", format="%d")
        }
    )
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== DRILL-DOWN: Zone Detail =====
    st.markdown("### 🔍 Zone Drill-Down Analysis")
    
    zone_list = filtered_fulfillment['delivery_zone'].unique().tolist()
    selected_zone = st.selectbox("Select a Zone for Detailed Breakdown", zone_list)
    
    if selected_zone:
        zone_detail = filtered_fulfillment[filtered_fulfillment['delivery_zone'] == selected_zone]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_deliveries = len(zone_detail)
            st.metric("Total Deliveries", f"{total_deliveries:,}")
        
        with col2:
            on_time_zone = len(zone_detail[zone_detail['actual_delivery_date'] <= zone_detail['promised_date']])
            on_time_pct = (on_time_zone / total_deliveries * 100) if total_deliveries > 0 else 0
            st.metric("On-Time Rate", f"{on_time_pct:.1f}%")
        
        with col3:
            breach_zone = total_deliveries - on_time_zone
            st.metric("SLA Breaches", f"{breach_zone:,}")
        
        # Delay reason breakdown for zone
        zone_delays = zone_detail[zone_detail['delay_reason'].notna()]
        if len(zone_delays) > 0:
            delay_breakdown = zone_delays['delay_reason'].value_counts().reset_index()
            delay_breakdown.columns = ['Reason', 'Count']
            
            fig = px.pie(
                delay_breakdown,
                values='Count',
                names='Reason',
                color_discrete_sequence=['#c9a227', '#f4d03f', '#8b7355', '#d4af37'],
                hole=0.4
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f5f5',
                title=f'Delay Reasons in {selected_zone}'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    
    # ===== WHAT-IF ANALYSIS =====
    st.markdown("### 🔮 What-If Analysis")
    st.markdown("*Adjust the sliders to see projected impact on business metrics*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📉 Reduce Cancellation Rate")
        cancellation_reduction = st.slider(
            "Reduce cancellation rate by:",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            format="%d%%",
            key="cancel_slider"
        )
        
        # Calculate impact
        current_cancelled = mgr_kpis['cancelled_orders']
        reduced_cancellations = int(current_cancelled * (cancellation_reduction / 100))
        recovered_revenue = reduced_cancellations * mgr_kpis['avg_order_value']
        
        st.markdown(f"""
        <div class='whatif-box'>
            <p style='color: #f5f5f5; margin-bottom: 10px;'>If cancellations reduced by <strong>{cancellation_reduction}%</strong>:</p>
            <p style='color: #f5f5f5;'>Orders Recovered: <span class='whatif-value'>{reduced_cancellations:,}</span></p>
            <p style='color: #f5f5f5;'>Projected Revenue Gain: <span class='whatif-value'>AED {recovered_revenue:,.0f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🚚 Improve On-Time Delivery")
        delivery_improvement = st.slider(
            "Improve on-time delivery by:",
            min_value=5,
            max_value=30,
            value=15,
            step=5,
            format="%d%%",
            key="delivery_slider"
        )
        
        # Calculate impact
        current_breaches = mgr_kpis['sla_breach_count']
        reduced_breaches = int(current_breaches * (delivery_improvement / 100))
        # Assume each breach has a cost (refund/compensation)
        avg_refund_per_breach = mgr_kpis['total_refunds'] / current_breaches if current_breaches > 0 else 50
        cost_savings = reduced_breaches * avg_refund_per_breach
        
        new_on_time_rate = min(100, mgr_kpis['on_time_rate'] + delivery_improvement)
        
        st.markdown(f"""
        <div class='whatif-box'>
            <p style='color: #f5f5f5; margin-bottom: 10px;'>If on-time delivery improves by <strong>{delivery_improvement}%</strong>:</p>
            <p style='color: #f5f5f5;'>New On-Time Rate: <span class='whatif-value'>{new_on_time_rate:.1f}%</span></p>
            <p style='color: #f5f5f5;'>Breaches Avoided: <span class='whatif-value'>{reduced_breaches:,}</span></p>
            <p style='color: #f5f5f5;'>Refund Cost Reduction: <span class='whatif-value'>AED {cost_savings:,.0f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Combined Impact Summary
    st.markdown("#### 💰 Combined Impact Summary")
    
    total_benefit = recovered_revenue + cost_savings
    
    st.markdown(f"""
    <div class='insight-box' style='border-color: #4ade80;'>
        <div class='insight-title' style='color: #4ade80;'>📊 Total Projected Benefit</div>
        <div style='text-align: center; padding: 20px;'>
            <span style='font-size: 3rem; font-weight: bold; color: #4ade80;'>AED {total_benefit:,.0f}</span>
            <p style='color: #f5f5f5; margin-top: 10px;'>
                Revenue Recovery: AED {recovered_revenue:,.0f} | Cost Savings: AED {cost_savings:,.0f}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
