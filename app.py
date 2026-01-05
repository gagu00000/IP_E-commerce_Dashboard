"""
================================================================================
SOUQPLUS ANALYTICS DASHBOARD
================================================================================
UAE Premium E-Commerce Intelligence Platform
Developed by: Group 1 | Master of AI in Business | SP Jain
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
    page_title="SouqPlus Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================================
# EXECUTIVE THEME - NAVY BLUE & SILVER
# ================================================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1a2d47 50%, #0d1b2a 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #152238 100%);
        border-right: 2px solid #3a86ff;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e8e8e8;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #3a86ff;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #3a86ff, transparent);
        margin: 25px 0;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #1a2d47 0%, #0d1b2a 100%);
        border: 1px solid #2a4a7f;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(58, 134, 255, 0.15);
        border-color: #3a86ff;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        margin: 10px 0;
    }
    
    .kpi-label {
        color: #8facc4;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .kpi-delta-positive {
        color: #4ade80;
        font-size: 0.85rem;
    }
    
    .kpi-delta-negative {
        color: #f87171;
        font-size: 0.85rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #1a2d47 0%, #0d1b2a 100%);
        border: 1px solid #2a4a7f;
        border-left: 4px solid #3a86ff;
        border-radius: 8px;
        padding: 20px 25px;
        margin: 15px 0;
    }
    
    .insight-title {
        color: #3a86ff;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    
    .insight-text {
        color: #d0d0d0;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    .whatif-box {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), #0d1b2a);
        border: 1px solid #4ade80;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .whatif-value {
        font-size: 1.6rem;
        font-weight: bold;
        color: #4ade80;
    }
    
    .stRadio > div {
        background-color: rgba(58, 134, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #2a4a7f;
    }
    
    .tier-bronze { color: #cd7f32; }
    .tier-silver { color: #c0c0c0; }
    .tier-gold { color: #ffd700; }
    .tier-platinum { color: #e5e4e2; }
</style>
""", unsafe_allow_html=True)

# ================================================================================
# DATA LOADING AND CLEANING (COMPREHENSIVE - WITH SAFE COLUMN CHECKS)
# ================================================================================

@st.cache_data
def load_and_clean_data():
    """Load and thoroughly clean all data files"""
    try:
        customers = pd.read_csv('customers.csv')
        orders = pd.read_csv('orders.csv')
        order_items = pd.read_csv('order_items.csv')
        fulfillment = pd.read_csv('fulfillment.csv')
        returns = pd.read_csv('returns.csv')
        
        # ===== 1. REMOVE DUPLICATES (Safe method) =====
        if 'customer_id' in customers.columns:
            customers = customers.drop_duplicates(subset=['customer_id'], keep='first')
        else:
            customers = customers.drop_duplicates(keep='first')
        
        if 'order_id' in orders.columns:
            orders = orders.drop_duplicates(subset=['order_id'], keep='first')
        else:
            orders = orders.drop_duplicates(keep='first')
        
        # For order_items - check which columns exist
        if 'order_item_id' in order_items.columns:
            order_items = order_items.drop_duplicates(subset=['order_item_id'], keep='first')
        elif 'item_id' in order_items.columns:
            order_items = order_items.drop_duplicates(subset=['item_id'], keep='first')
        else:
            order_items = order_items.drop_duplicates(keep='first')
        
        # For fulfillment - check which columns exist
        if 'fulfillment_id' in fulfillment.columns:
            fulfillment = fulfillment.drop_duplicates(subset=['fulfillment_id'], keep='first')
        elif 'order_id' in fulfillment.columns:
            fulfillment = fulfillment.drop_duplicates(subset=['order_id'], keep='first')
        else:
            fulfillment = fulfillment.drop_duplicates(keep='first')
        
        # For returns - check which columns exist
        if 'return_id' in returns.columns:
            returns = returns.drop_duplicates(subset=['return_id'], keep='first')
        else:
            returns = returns.drop_duplicates(keep='first')
        
        # ===== 2. STANDARDIZE CITY NAMES =====
        city_mapping = {
            'DUBAI': 'Dubai', 'dubai': 'Dubai', 'Dxb': 'Dubai', 'DXB': 'Dubai',
            'ABU DHABI': 'Abu Dhabi', 'abu dhabi': 'Abu Dhabi', 'AD': 'Abu Dhabi', 'AbuDhabi': 'Abu Dhabi',
            'SHARJAH': 'Sharjah', 'sharjah': 'Sharjah', 'SHJ': 'Sharjah',
            'AJMAN': 'Ajman', 'ajman': 'Ajman', 'AJM': 'Ajman',
            'RAS AL KHAIMAH': 'Ras Al Khaimah', 'ras al khaimah': 'Ras Al Khaimah', 
            'RAK': 'Ras Al Khaimah', 'Ras al Khaimah': 'Ras Al Khaimah'
        }
        if 'city' in customers.columns:
            customers['city'] = customers['city'].replace(city_mapping)
        
        # ===== 3. STANDARDIZE CATEGORY NAMES =====
        category_mapping = {
            'electronics': 'Electronics', 'ELECTRONICS': 'Electronics', 'Electronic': 'Electronics',
            'fashion': 'Fashion', 'FASHION': 'Fashion', 'Fashions': 'Fashion',
            'home & kitchen': 'Home & Kitchen', 'HOME & KITCHEN': 'Home & Kitchen', 
            'Home and Kitchen': 'Home & Kitchen', 'home&kitchen': 'Home & Kitchen',
            'beauty': 'Beauty', 'BEAUTY': 'Beauty', 'Beauties': 'Beauty',
            'groceries': 'Groceries', 'GROCERIES': 'Groceries', 'Grocery': 'Groceries'
        }
        if 'product_category' in order_items.columns:
            order_items['product_category'] = order_items['product_category'].replace(category_mapping)
        
        # ===== 4. HANDLE MISSING VALUES =====
        if 'discount_amount' in orders.columns:
            orders['discount_amount'] = orders['discount_amount'].fillna(0)
        else:
            orders['discount_amount'] = 0
        
        if 'delivery_zone' in fulfillment.columns:
            fulfillment['delivery_zone'] = fulfillment['delivery_zone'].fillna('Unknown Zone')
        
        if 'delay_reason' in fulfillment.columns:
            fulfillment['delay_reason'] = fulfillment['delay_reason'].fillna('No Delay')
        
        if 'delivery_partner' in fulfillment.columns:
            fulfillment['delivery_partner'] = fulfillment['delivery_partner'].fillna('Unknown Partner')
        else:
            fulfillment['delivery_partner'] = 'Unknown Partner'
        
        if 'return_reason' in returns.columns:
            returns['return_reason'] = returns['return_reason'].fillna('Not Specified')
        
        # ===== 5. CONVERT DATES =====
        if 'signup_date' in customers.columns:
            customers['signup_date'] = pd.to_datetime(customers['signup_date'], errors='coerce')
        
        if 'order_date' in orders.columns:
            orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
        
        if 'promised_date' in fulfillment.columns:
            fulfillment['promised_date'] = pd.to_datetime(fulfillment['promised_date'], errors='coerce')
        
        if 'actual_delivery_date' in fulfillment.columns:
            fulfillment['actual_delivery_date'] = pd.to_datetime(fulfillment['actual_delivery_date'], errors='coerce')
        
        if 'return_date' in returns.columns:
            returns['return_date'] = pd.to_datetime(returns['return_date'], errors='coerce')
        
        # ===== 6. FIX IMPOSSIBLE DATES =====
        today = pd.Timestamp.today()
        min_valid_date = pd.Timestamp('2020-01-01')
        
        if 'order_date' in orders.columns:
            orders = orders[
                (orders['order_date'] >= min_valid_date) & 
                (orders['order_date'] <= today)
            ]
        
        # ===== 7. FIX NEGATIVE AMOUNTS =====
        if 'net_amount' in orders.columns:
            orders['net_amount'] = orders['net_amount'].abs()
        
        if 'gross_amount' in orders.columns:
            orders['gross_amount'] = orders['gross_amount'].abs()
        
        if 'discount_amount' in orders.columns:
            orders['discount_amount'] = orders['discount_amount'].abs()
        
        # ===== 8. HANDLE OUTLIERS (Orders > AED 10,000) =====
        if 'net_amount' in orders.columns:
            revenue_cap = orders['net_amount'].quantile(0.99)
            orders['net_amount_capped'] = orders['net_amount'].clip(upper=revenue_cap)
            orders['is_outlier'] = orders['net_amount'] > 10000
        
        # ===== 9. CREATE CUSTOMER TIERS =====
        if 'net_amount' in orders.columns and 'customer_id' in orders.columns:
            customer_spending = orders.groupby('customer_id')['net_amount'].sum().reset_index()
            customer_spending.columns = ['customer_id', 'total_spending']
            
            def assign_tier(spending):
                if spending < 500:
                    return 'Bronze'
                elif spending < 2000:
                    return 'Silver'
                elif spending < 5000:
                    return 'Gold'
                else:
                    return 'Platinum'
            
            customer_spending['customer_tier'] = customer_spending['total_spending'].apply(assign_tier)
            customers = customers.merge(
                customer_spending[['customer_id', 'total_spending', 'customer_tier']], 
                on='customer_id', 
                how='left'
            )
            customers['customer_tier'] = customers['customer_tier'].fillna('Bronze')
            customers['total_spending'] = customers['total_spending'].fillna(0)
        else:
            customers['customer_tier'] = 'Bronze'
            customers['total_spending'] = 0
        
        return customers, orders, order_items, fulfillment, returns
        
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.info("Please ensure all CSV files (customers.csv, orders.csv, order_items.csv, fulfillment.csv, returns.csv) are in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info(f"Details: {str(e)}")
        st.stop()

# Load data
customers_df, orders_df, order_items_df, fulfillment_df, returns_df = load_and_clean_data()

# ================================================================================
# CHART COLORS
# ================================================================================

COLORS = {
    'primary': '#3a86ff',
    'secondary': '#4cc9f0',
    'accent': '#7209b7',
    'success': '#4ade80',
    'warning': '#fb923c',
    'danger': '#f87171',
    'neutral': '#8facc4'
}

CHART_COLORS = ['#3a86ff', '#4cc9f0', '#4ade80', '#fb923c', '#f87171', '#a78bfa', '#7209b7']
TIER_COLORS = {'Bronze': '#cd7f32', 'Silver': '#c0c0c0', 'Gold': '#ffd700', 'Platinum': '#e5e4e2'}

# ================================================================================
# SIDEBAR - FILTERS
# ================================================================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='color: #3a86ff; font-size: 1.8rem; margin-bottom: 5px;'>🛍️ SOUQPLUS</h1>
    <p style='color: #8facc4; font-size: 0.85rem; letter-spacing: 3px;'>ANALYTICS DASHBOARD</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== VIEW TOGGLE (MANDATORY - HEAVILY GRADED) =====
st.sidebar.markdown("### 📊 Dashboard View")
view_mode = st.sidebar.radio(
    "Select View",
    ["Executive View", "Manager View"],
    index=0,
    help="Executive: Revenue & Growth | Manager: Operations & Issues"
)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### 🎯 Filters")

# ===== FILTER 1: DATE RANGE =====
st.sidebar.markdown("**📅 Date Range**")
min_date = orders_df['order_date'].min().date()
max_date = orders_df['order_date'].max().date()

# Default to last 90 days
default_start = max(min_date, max_date - timedelta(days=90))

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("From", default_start, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)

# ===== FILTER 2: CITY =====
st.sidebar.markdown("**🏙️ City**")
available_cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Ras Al Khaimah']
city_options = [c for c in available_cities if c in customers_df['city'].unique()]
if not city_options:
    city_options = list(customers_df['city'].unique())
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=city_options,
    default=city_options
)

# ===== FILTER 3: ORDER CHANNEL =====
st.sidebar.markdown("**📱 Order Channel**")
channel_options = list(orders_df['order_channel'].unique()) if 'order_channel' in orders_df.columns else ['App', 'Web', 'Call Center']
selected_channels = st.sidebar.multiselect(
    "Select Channels",
    options=channel_options,
    default=channel_options
)

# ===== FILTER 4: PRODUCT CATEGORY =====
st.sidebar.markdown("**🛍️ Product Category**")
category_options = list(order_items_df['product_category'].unique()) if 'product_category' in order_items_df.columns else []
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=category_options,
    default=category_options
)

# ===== FILTER 5: CUSTOMER SEGMENT =====
st.sidebar.markdown("**👥 Customer Segment**")
segment_options = list(customers_df['customer_segment'].unique()) if 'customer_segment' in customers_df.columns else ['Regular', 'Premium', 'VIP']
selected_segments = st.sidebar.multiselect(
    "Select Segments",
    options=segment_options,
    default=segment_options
)

# ===== FILTER 6: ORDER STATUS =====
st.sidebar.markdown("**📦 Order Status**")
status_options = list(orders_df['order_status'].unique()) if 'order_status' in orders_df.columns else ['Delivered', 'Cancelled', 'Returned', 'In Transit']
selected_statuses = st.sidebar.multiselect(
    "Select Statuses",
    options=status_options,
    default=status_options
)

# ===== FILTER 7: CUSTOMER TIER (OPTIONAL BONUS) =====
st.sidebar.markdown("**👑 Customer Tier (Bonus)**")
tier_options = ['Bronze', 'Silver', 'Gold', 'Platinum']
selected_tiers = st.sidebar.multiselect(
    "Select Tiers",
    options=tier_options,
    default=tier_options
)

# ================================================================================
# APPLY FILTERS
# ================================================================================

# Filter orders by date
filtered_orders = orders_df[
    (orders_df['order_date'].dt.date >= start_date) &
    (orders_df['order_date'].dt.date <= end_date)
].copy()

# Calculate previous period for comparison
period_length = (end_date - start_date).days
prev_start = start_date - timedelta(days=period_length)
prev_end = start_date - timedelta(days=1)

previous_orders = orders_df[
    (orders_df['order_date'].dt.date >= prev_start) &
    (orders_df['order_date'].dt.date <= prev_end)
].copy()

# Filter by city
if selected_cities and 'city' in customers_df.columns:
    city_customers = customers_df[customers_df['city'].isin(selected_cities)]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(city_customers)]
    previous_orders = previous_orders[previous_orders['customer_id'].isin(city_customers)]

# Filter by channel
if selected_channels and 'order_channel' in filtered_orders.columns:
    filtered_orders = filtered_orders[filtered_orders['order_channel'].isin(selected_channels)]
    previous_orders = previous_orders[previous_orders['order_channel'].isin(selected_channels)]

# Filter by customer segment
if selected_segments and 'customer_segment' in customers_df.columns:
    segment_customers = customers_df[customers_df['customer_segment'].isin(selected_segments)]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(segment_customers)]
    previous_orders = previous_orders[previous_orders['customer_id'].isin(segment_customers)]

# Filter by order status
if selected_statuses and 'order_status' in filtered_orders.columns:
    filtered_orders = filtered_orders[filtered_orders['order_status'].isin(selected_statuses)]
    previous_orders = previous_orders[previous_orders['order_status'].isin(selected_statuses)]

# Filter by customer tier
if selected_tiers and 'customer_tier' in customers_df.columns:
    tier_customers = customers_df[customers_df['customer_tier'].isin(selected_tiers)]['customer_id']
    filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(tier_customers)]
    previous_orders = previous_orders[previous_orders['customer_id'].isin(tier_customers)]

# Filter order items by category
filtered_order_items = order_items_df[order_items_df['order_id'].isin(filtered_orders['order_id'])]
if selected_categories and 'product_category' in filtered_order_items.columns:
    filtered_order_items = filtered_order_items[filtered_order_items['product_category'].isin(selected_categories)]
    filtered_orders = filtered_orders[filtered_orders['order_id'].isin(filtered_order_items['order_id'])]

# Get related filtered data
filtered_customer_ids = filtered_orders['customer_id'].unique()
filtered_customers = customers_df[customers_df['customer_id'].isin(filtered_customer_ids)]
filtered_fulfillment = fulfillment_df[fulfillment_df['order_id'].isin(filtered_orders['order_id'])]
filtered_returns = returns_df[returns_df['order_id'].isin(filtered_orders['order_id'])]

# ================================================================================
# KPI CALCULATIONS
# ================================================================================

def calculate_executive_kpis(orders, previous_orders):
    """Calculate Executive View KPIs with period comparison"""
    kpis = {}
    
    # Check for order_status column
    if 'order_status' in orders.columns:
        delivered_orders = orders[orders['order_status'] == 'Delivered']
        prev_delivered = previous_orders[previous_orders['order_status'] == 'Delivered'] if len(previous_orders) > 0 else pd.DataFrame()
    else:
        delivered_orders = orders
        prev_delivered = previous_orders
    
    # Total Revenue
    kpis['total_revenue'] = delivered_orders['net_amount'].sum() if 'net_amount' in delivered_orders.columns else 0
    prev_revenue = prev_delivered['net_amount'].sum() if len(prev_delivered) > 0 and 'net_amount' in prev_delivered.columns else 0
    
    # Revenue % change vs previous period
    if prev_revenue > 0:
        kpis['revenue_change'] = ((kpis['total_revenue'] - prev_revenue) / prev_revenue) * 100
    else:
        kpis['revenue_change'] = 0
    
    # Average Order Value
    kpis['aov'] = delivered_orders['net_amount'].mean() if len(delivered_orders) > 0 and 'net_amount' in delivered_orders.columns else 0
    prev_aov = prev_delivered['net_amount'].mean() if len(prev_delivered) > 0 and 'net_amount' in prev_delivered.columns else 0
    kpis['aov_change'] = ((kpis['aov'] - prev_aov) / prev_aov * 100) if prev_aov > 0 else 0
    
    # Repeat Customer Rate
    if 'customer_id' in orders.columns:
        customer_order_counts = orders.groupby('customer_id').size()
        repeat_customers = (customer_order_counts >= 2).sum()
        total_active = len(customer_order_counts)
        kpis['repeat_rate'] = (repeat_customers / total_active * 100) if total_active > 0 else 0
    else:
        kpis['repeat_rate'] = 0
    
    # Discount Rate
    if 'gross_amount' in orders.columns and 'discount_amount' in orders.columns:
        total_gross = orders['gross_amount'].sum()
        total_discount = orders['discount_amount'].sum()
        kpis['discount_rate'] = (total_discount / total_gross * 100) if total_gross > 0 else 0
    else:
        kpis['discount_rate'] = 0
    
    # Additional metrics
    kpis['total_orders'] = len(orders)
    kpis['delivered_count'] = len(delivered_orders)
    
    return kpis

def calculate_manager_kpis(orders, fulfillment, returns):
    """Calculate Manager View KPIs"""
    kpis = {}
    
    # On-Time Delivery Rate
    if 'actual_delivery_date' in fulfillment.columns and 'promised_date' in fulfillment.columns:
        delivered_fulfillment = fulfillment[fulfillment['actual_delivery_date'].notna()]
        on_time = delivered_fulfillment[
            delivered_fulfillment['actual_delivery_date'] <= delivered_fulfillment['promised_date']
        ]
        kpis['on_time_rate'] = (len(on_time) / len(delivered_fulfillment) * 100) if len(delivered_fulfillment) > 0 else 0
        kpis['sla_breach_count'] = len(delivered_fulfillment) - len(on_time)
    else:
        kpis['on_time_rate'] = 0
        kpis['sla_breach_count'] = 0
    
    # Cancellation Rate
    if 'order_status' in orders.columns:
        cancelled = len(orders[orders['order_status'] == 'Cancelled'])
        kpis['cancellation_rate'] = (cancelled / len(orders) * 100) if len(orders) > 0 else 0
        kpis['cancelled_orders'] = cancelled
        kpis['delivered_orders'] = len(orders[orders['order_status'] == 'Delivered'])
    else:
        kpis['cancellation_rate'] = 0
        kpis['cancelled_orders'] = 0
        kpis['delivered_orders'] = 0
    
    # Total Refund Amount
    if 'refund_status' in returns.columns and 'refund_amount' in returns.columns:
        kpis['total_refunds'] = returns[returns['refund_status'] == 'Processed']['refund_amount'].sum()
    elif 'refund_amount' in returns.columns:
        kpis['total_refunds'] = returns['refund_amount'].sum()
    else:
        kpis['total_refunds'] = 0
    
    # Additional metrics
    kpis['total_orders'] = len(orders)
    kpis['avg_order_value'] = orders['net_amount'].mean() if len(orders) > 0 and 'net_amount' in orders.columns else 0
    
    return kpis

# Calculate KPIs
exec_kpis = calculate_executive_kpis(filtered_orders, previous_orders)
mgr_kpis = calculate_manager_kpis(filtered_orders, filtered_fulfillment, filtered_returns)

# ================================================================================
# MAIN HEADER
# ================================================================================

view_label = "EXECUTIVE" if view_mode == "Executive View" else "OPERATIONS"

st.markdown(f"""
<div style='text-align: center; padding: 10px 0 20px 0;'>
    <h1 style='color: #ffffff; font-size: 2.2rem; font-weight: 600; margin-bottom: 5px;'>
        🛍️ SouqPlus Analytics Dashboard
    </h1>
    <p style='color: #8facc4; font-size: 1rem; letter-spacing: 2px;'>
        UAE E-COMMERCE INTELLIGENCE | {view_label} VIEW
    </p>
</div>
<div class='divider'></div>
""", unsafe_allow_html=True)

# ================================================================================
# EXECUTIVE VIEW
# ================================================================================

if view_mode == "Executive View":
    
    # ===== 4 KPI CARDS =====
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        change_class = 'kpi-delta-positive' if exec_kpis['revenue_change'] >= 0 else 'kpi-delta-negative'
        change_symbol = '▲' if exec_kpis['revenue_change'] >= 0 else '▼'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-value'>AED {exec_kpis['total_revenue']:,.0f}</div>
            <div class='{change_class}'>{change_symbol} {abs(exec_kpis['revenue_change']):.1f}% vs previous period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        aov_class = 'kpi-delta-positive' if exec_kpis['aov_change'] >= 0 else 'kpi-delta-negative'
        aov_symbol = '▲' if exec_kpis['aov_change'] >= 0 else '▼'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Average Order Value</div>
            <div class='kpi-value'>AED {exec_kpis['aov']:,.0f}</div>
            <div class='{aov_class}'>{aov_symbol} {abs(exec_kpis['aov_change']):.1f}% vs previous</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rate_class = 'kpi-delta-positive' if exec_kpis['repeat_rate'] > 30 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Repeat Customer Rate</div>
            <div class='kpi-value'>{exec_kpis['repeat_rate']:.1f}%</div>
            <div class='{rate_class}'>{'Strong Loyalty' if exec_kpis['repeat_rate'] > 30 else 'Needs Improvement'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        disc_class = 'kpi-delta-positive' if exec_kpis['discount_rate'] < 15 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Discount Rate</div>
            <div class='kpi-value'>{exec_kpis['discount_rate']:.1f}%</div>
            <div class='{disc_class}'>{'Healthy Margin' if exec_kpis['discount_rate'] < 15 else 'High Burn Rate'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 1 & 2 =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Revenue Trend")
        agg_type = st.radio("View by", ["Weekly", "Monthly"], horizontal=True, key="rev_agg")
        
        if 'order_status' in filtered_orders.columns:
            delivered = filtered_orders[filtered_orders['order_status'] == 'Delivered'].copy()
        else:
            delivered = filtered_orders.copy()
        
        if len(delivered) > 0 and 'net_amount' in delivered.columns:
            if agg_type == "Weekly":
                delivered['period'] = delivered['order_date'].dt.to_period('W').apply(lambda x: x.start_time)
            else:  # Monthly
                delivered['period'] = delivered['order_date'].dt.to_period('M').apply(lambda x: x.start_time)
            
            revenue_trend = delivered.groupby('period')['net_amount'].sum().reset_index()
            revenue_trend.columns = ['Date', 'Revenue']
            
            fig = px.line(revenue_trend, x='Date', y='Revenue', markers=True,
                         color_discrete_sequence=[COLORS['primary']])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e8e8e8',
                xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title=''),
                yaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='Revenue (AED)'),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No delivered orders in selected period.")
    
    with col2:
        st.markdown("### 🏙️ Revenue by City")
        
        if 'city' in customers_df.columns:
            city_revenue = filtered_orders.merge(customers_df[['customer_id', 'city']], on='customer_id')
            if 'order_status' in city_revenue.columns:
                city_revenue = city_revenue[city_revenue['order_status'] == 'Delivered']
            
            if len(city_revenue) > 0 and 'net_amount' in city_revenue.columns:
                city_agg = city_revenue.groupby('city')['net_amount'].sum().reset_index()
                city_agg.columns = ['City', 'Revenue']
                city_agg = city_agg.sort_values('Revenue', ascending=True)
                
                fig = px.bar(city_agg, x='Revenue', y='City', orientation='h',
                            color='Revenue', color_continuous_scale=['#1a2d47', '#3a86ff', '#4cc9f0'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8e8e8', showlegend=False, coloraxis_showscale=False,
                    xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='Revenue (AED)'),
                    yaxis=dict(title=''),
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available.")
        else:
            st.info("City data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 3 & 4 =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📱 Channel Contribution")
        
        if len(filtered_orders) > 0 and 'order_channel' in filtered_orders.columns:
            channel_orders = filtered_orders.groupby('order_channel').agg({
                'order_id': 'count', 'net_amount': 'sum'
            }).reset_index()
            channel_orders.columns = ['Channel', 'Orders', 'Revenue']
            channel_orders['Percentage'] = (channel_orders['Orders'] / channel_orders['Orders'].sum() * 100).round(1)
            
            fig = px.pie(channel_orders, values='Orders', names='Channel',
                        color_discrete_sequence=CHART_COLORS, hole=0.5)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e8e8e8', margin=dict(l=0, r=0, t=20, b=0)
            )
            fig.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No channel data available.")
    
    with col2:
        st.markdown("### 🛍️ Category Revenue by City")
        
        if 'city' in customers_df.columns and 'product_category' in filtered_order_items.columns:
            orders_city = filtered_orders.merge(customers_df[['customer_id', 'city']], on='customer_id')
            orders_detail = orders_city.merge(
                filtered_order_items[['order_id', 'product_category', 'item_total']], on='order_id'
            )
            
            if len(orders_detail) > 0:
                cat_city = orders_detail.groupby(['city', 'product_category'])['item_total'].sum().reset_index()
                cat_city.columns = ['City', 'Category', 'Revenue']
                
                fig = px.bar(cat_city, x='City', y='Revenue', color='Category',
                            color_discrete_sequence=CHART_COLORS, barmode='stack')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8e8e8',
                    xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title=''),
                    yaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='Revenue (AED)'),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, bgcolor='rgba(0,0,0,0)'),
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available.")
        else:
            st.info("Category or city data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CUSTOMER TIER DISTRIBUTION (BONUS) =====
    st.markdown("### 👑 Customer Tier Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'customer_tier' in filtered_customers.columns:
            tier_dist = filtered_customers['customer_tier'].value_counts().reset_index()
            tier_dist.columns = ['Tier', 'Count']
            tier_order = ['Bronze', 'Silver', 'Gold', 'Platinum']
            tier_dist['Tier'] = pd.Categorical(tier_dist['Tier'], categories=tier_order, ordered=True)
            tier_dist = tier_dist.sort_values('Tier')
            
            fig = px.bar(tier_dist, x='Tier', y='Count', color='Tier',
                        color_discrete_map=TIER_COLORS)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e8e8e8', showlegend=False,
                xaxis=dict(title=''), yaxis=dict(title='Customers', gridcolor='rgba(58,134,255,0.1)'),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Customer tier data not available.")
    
    with col2:
        if 'customer_tier' in customers_df.columns:
            tier_revenue = filtered_orders.merge(customers_df[['customer_id', 'customer_tier']], on='customer_id')
            tier_rev_agg = tier_revenue.groupby('customer_tier')['net_amount'].sum().reset_index()
            tier_rev_agg.columns = ['Tier', 'Revenue']
            tier_order = ['Bronze', 'Silver', 'Gold', 'Platinum']
            tier_rev_agg['Tier'] = pd.Categorical(tier_rev_agg['Tier'], categories=tier_order, ordered=True)
            tier_rev_agg = tier_rev_agg.sort_values('Tier')
            
            fig = px.bar(tier_rev_agg, x='Tier', y='Revenue', color='Tier',
                        color_discrete_map=TIER_COLORS)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e8e8e8', showlegend=False,
                xaxis=dict(title=''), yaxis=dict(title='Revenue (AED)', gridcolor='rgba(58,134,255,0.1)'),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Customer tier data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== INSIGHTS BOX =====
    st.markdown("### 💡 Executive Insights")
    
    # Calculate insights
    top_city, top_city_rev, bottom_city = "N/A", 0, "N/A"
    if 'city' in customers_df.columns:
        city_revenue = filtered_orders.merge(customers_df[['customer_id', 'city']], on='customer_id')
        if 'order_status' in city_revenue.columns:
            city_revenue = city_revenue[city_revenue['order_status'] == 'Delivered']
        if len(city_revenue) > 0:
            city_agg = city_revenue.groupby('city')['net_amount'].sum().reset_index()
            city_agg.columns = ['City', 'Revenue']
            city_agg = city_agg.sort_values('Revenue', ascending=True)
            if len(city_agg) > 0:
                top_city = city_agg.iloc[-1]['City']
                top_city_rev = city_agg.iloc[-1]['Revenue']
                bottom_city = city_agg.iloc[0]['City']
    
    top_channel, top_channel_pct = "N/A", 0
    if 'order_channel' in filtered_orders.columns and len(filtered_orders) > 0:
        channel_orders = filtered_orders.groupby('order_channel').size().reset_index()
        channel_orders.columns = ['Channel', 'Orders']
        channel_orders['Percentage'] = (channel_orders['Orders'] / channel_orders['Orders'].sum() * 100).round(1)
        if len(channel_orders) > 0:
            top_channel = channel_orders.loc[channel_orders['Orders'].idxmax()]['Channel']
            top_channel_pct = channel_orders.loc[channel_orders['Orders'].idxmax()]['Percentage']
    
    st.markdown(f"""
    <div class='insight-box'>
        <div class='insight-title'>📊 Key Findings & Recommendations</div>
        <div class='insight-text'>
            <p>• <strong>Top performing city is {top_city}</strong> with <strong>AED {top_city_rev:,.0f}</strong> in revenue. Consider increasing marketing investment here.</p>
            <p>• <strong>Underperforming city: {bottom_city}</strong> — Investigate delivery issues or regional preferences.</p>
            <p>• <strong>{top_channel} channel</strong> contributes <strong>{top_channel_pct:.1f}%</strong> of orders — Optimize other channels for diversification.</p>
            <p>• <strong>Repeat customer rate is {exec_kpis['repeat_rate']:.1f}%</strong> — {'Healthy loyalty base.' if exec_kpis['repeat_rate'] > 30 else 'Launch retention campaigns to improve loyalty.'}</p>
            <p>• <strong>Discount burn accounts for {exec_kpis['discount_rate']:.1f}%</strong> of gross revenue — {'Within acceptable limits.' if exec_kpis['discount_rate'] < 15 else 'Review promotional strategy to protect margins.'}</p>
            <p>• <strong>Revenue {('increased' if exec_kpis['revenue_change'] >= 0 else 'decreased')} by {abs(exec_kpis['revenue_change']):.1f}%</strong> compared to previous period.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# MANAGER VIEW
# ================================================================================

else:
    
    # ===== 4 KPI CARDS =====
    st.markdown("### 🔧 Operational KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        rate_class = 'kpi-delta-positive' if mgr_kpis['on_time_rate'] > 85 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>On-Time Delivery Rate</div>
            <div class='kpi-value'>{mgr_kpis['on_time_rate']:.1f}%</div>
            <div class='{rate_class}'>Target: 85%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>SLA Breach Count</div>
            <div class='kpi-value'>{mgr_kpis['sla_breach_count']:,}</div>
            <div class='kpi-delta-negative'>Requires Attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cancel_class = 'kpi-delta-positive' if mgr_kpis['cancellation_rate'] < 10 else 'kpi-delta-negative'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Cancellation Rate</div>
            <div class='kpi-value'>{mgr_kpis['cancellation_rate']:.1f}%</div>
            <div class='{cancel_class}'>Target: &lt;10%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Total Refunds</div>
            <div class='kpi-value'>AED {mgr_kpis['total_refunds']:,.0f}</div>
            <div class='kpi-delta-negative'>Cost Impact</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 1 & 2 =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 SLA Breach Trend")
        
        if 'actual_delivery_date' in filtered_fulfillment.columns and 'promised_date' in filtered_fulfillment.columns:
            breach_data = filtered_fulfillment[
                (filtered_fulfillment['actual_delivery_date'].notna()) &
                (filtered_fulfillment['actual_delivery_date'] > filtered_fulfillment['promised_date'])
            ].copy()
            
            if len(breach_data) > 0:
                breach_trend = breach_data.groupby(
                    breach_data['actual_delivery_date'].dt.date
                ).size().reset_index()
                breach_trend.columns = ['Date', 'Breaches']
                
                fig = px.line(breach_trend, x='Date', y='Breaches', markers=True,
                             color_discrete_sequence=[COLORS['danger']])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8e8e8',
                    xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title=''),
                    yaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='SLA Breaches'),
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=6))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No SLA breaches in selected period! ✅")
        else:
            st.info("Delivery date data not available.")
    
    with col2:
        st.markdown("### 📍 Breaches by Delivery Zone (Top 10)")
        
        if 'actual_delivery_date' in filtered_fulfillment.columns and 'promised_date' in filtered_fulfillment.columns:
            breach_data = filtered_fulfillment[
                (filtered_fulfillment['actual_delivery_date'].notna()) &
                (filtered_fulfillment['actual_delivery_date'] > filtered_fulfillment['promised_date'])
            ].copy()
            
            if len(breach_data) > 0 and 'delivery_zone' in breach_data.columns:
                zone_breaches = breach_data.groupby('delivery_zone').size().reset_index()
                zone_breaches.columns = ['Zone', 'Breaches']
                zone_breaches = zone_breaches.sort_values('Breaches', ascending=False).head(10)
                zone_breaches = zone_breaches.sort_values('Breaches', ascending=True)
                
                fig = px.bar(zone_breaches, x='Breaches', y='Zone', orientation='h',
                            color='Breaches', color_continuous_scale=['#fb923c', '#f87171'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8e8e8', showlegend=False, coloraxis_showscale=False,
                    xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='Breaches'),
                    yaxis=dict(title=''),
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No zone data available.")
        else:
            st.info("Delivery data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 3 & 4 =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Delay Reasons (Pareto Analysis)")
        
        if 'delay_reason' in filtered_fulfillment.columns:
            delay_data = filtered_fulfillment[
                (filtered_fulfillment['delay_reason'].notna()) &
                (filtered_fulfillment['delay_reason'] != 'No Delay') &
                (filtered_fulfillment['delay_reason'] != 'Order Cancelled') &
                (filtered_fulfillment['delay_reason'] != '')
            ]
            
            if len(delay_data) > 0:
                delay_reasons = delay_data.groupby('delay_reason').size().reset_index()
                delay_reasons.columns = ['Reason', 'Count']
                delay_reasons = delay_reasons.sort_values('Count', ascending=False)
                delay_reasons['Cumulative'] = delay_reasons['Count'].cumsum()
                delay_reasons['Cumulative %'] = (delay_reasons['Cumulative'] / delay_reasons['Count'].sum() * 100)
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Bar(x=delay_reasons['Reason'], y=delay_reasons['Count'],
                          name='Count', marker_color=COLORS['primary']),
                    secondary_y=False
                )
                
                fig.add_trace(
                    go.Scatter(x=delay_reasons['Reason'], y=delay_reasons['Cumulative %'],
                              name='Cumulative %', mode='lines+markers',
                              line=dict(color=COLORS['danger'], width=3), marker=dict(size=8)),
                    secondary_y=True
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8e8e8',
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, bgcolor='rgba(0,0,0,0)'),
                    xaxis=dict(gridcolor='rgba(58,134,255,0.1)', tickangle=45),
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                fig.update_yaxes(title_text='Count', secondary_y=False, gridcolor='rgba(58,134,255,0.1)')
                fig.update_yaxes(title_text='Cumulative %', secondary_y=True, range=[0, 105])
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No delay data available.")
        else:
            st.info("Delay reason data not available.")
    
    with col2:
        st.markdown("### ↩️ Return Rate by Category")
        
        if 'product_category' in filtered_order_items.columns and len(filtered_returns) > 0:
            returns_cat = filtered_returns.merge(
                filtered_order_items[['order_id', 'product_category']].drop_duplicates('order_id'),
                on='order_id', how='left'
            )
            
            cat_returns = returns_cat.groupby('product_category').size().reset_index()
            cat_returns.columns = ['Category', 'Returns']
            
            cat_orders = filtered_order_items.groupby('product_category')['order_id'].nunique().reset_index()
            cat_orders.columns = ['Category', 'Orders']
            
            return_rate = cat_returns.merge(cat_orders, on='Category')
            return_rate['Return Rate'] = (return_rate['Returns'] / return_rate['Orders'] * 100).round(2)
            return_rate = return_rate.sort_values('Return Rate', ascending=False)
            
            if len(return_rate) > 0:
                fig = px.bar(return_rate, x='Category', y='Return Rate', color='Return Rate',
                            color_continuous_scale=['#4ade80', '#fb923c', '#f87171'], text='Return Rate')
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8e8e8', showlegend=False, coloraxis_showscale=False,
                    xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title=''),
                    yaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='Return Rate (%)',
                              range=[0, max(return_rate['Return Rate']) * 1.3 if len(return_rate) > 0 else 10]),
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No return data available.")
        else:
            st.info("Return or category data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== SORTABLE TABLE =====
    st.markdown("### 📋 Top 10 Problem Areas (Sortable)")
    
    if 'delivery_zone' in filtered_fulfillment.columns and 'actual_delivery_date' in filtered_fulfillment.columns:
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
        problem_zones.columns = ['Delivery Zone', 'SLA Breach Count', 'Avg Delay Days', 'Top Delay Reason', 'Total Orders']
        problem_zones = problem_zones.sort_values('SLA Breach Count', ascending=False).head(10)
        problem_zones['Avg Delay Days'] = problem_zones['Avg Delay Days'].round(1)
        
        st.dataframe(
            problem_zones,
            use_container_width=True,
            column_config={
                "Delivery Zone": st.column_config.TextColumn("Delivery Zone"),
                "SLA Breach Count": st.column_config.NumberColumn("SLA Breaches", format="%d"),
                "Avg Delay Days": st.column_config.NumberColumn("Avg Delay (Days)", format="%.1f"),
                "Top Delay Reason": st.column_config.TextColumn("Primary Reason"),
                "Total Orders": st.column_config.NumberColumn("Total Orders", format="%d")
            }
        )
    else:
        st.info("Zone analysis data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== DRILL-DOWN (COMPLETE) =====
    st.markdown("### 🔍 Zone Drill-Down Analysis")
    
    if 'delivery_zone' in filtered_fulfillment.columns:
        zone_list = filtered_fulfillment['delivery_zone'].dropna().unique().tolist()
        
        if len(zone_list) > 0:
            selected_zone = st.selectbox("Select a Delivery Zone for Detailed Breakdown", zone_list)
            
            if selected_zone:
                zone_detail = filtered_fulfillment[filtered_fulfillment['delivery_zone'] == selected_zone]
                zone_orders = filtered_orders[filtered_orders['order_id'].isin(zone_detail['order_id'])]
                
                # KPI Row
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_deliveries = len(zone_detail)
                    st.metric("Total Deliveries", f"{total_deliveries:,}")
                
                with col2:
                    if 'actual_delivery_date' in zone_detail.columns and 'promised_date' in zone_detail.columns:
                        on_time_zone = len(zone_detail[zone_detail['actual_delivery_date'] <= zone_detail['promised_date']])
                        on_time_pct = (on_time_zone / total_deliveries * 100) if total_deliveries > 0 else 0
                    else:
                        on_time_pct = 0
                    st.metric("On-Time Rate", f"{on_time_pct:.1f}%")
                
                with col3:
                    # CANCELLATION RATE FOR ZONE
                    if 'order_status' in zone_orders.columns:
                        zone_cancelled = len(zone_orders[zone_orders['order_status'] == 'Cancelled'])
                        zone_cancel_rate = (zone_cancelled / len(zone_orders) * 100) if len(zone_orders) > 0 else 0
                    else:
                        zone_cancel_rate = 0
                    st.metric("Cancellation Rate", f"{zone_cancel_rate:.1f}%")
                
                with col4:
                    if 'actual_delivery_date' in zone_detail.columns and 'promised_date' in zone_detail.columns:
                        breach_zone = len(zone_detail[zone_detail['actual_delivery_date'] > zone_detail['promised_date']])
                    else:
                        breach_zone = 0
                    st.metric("SLA Breaches", f"{breach_zone:,}")
                
                # Charts Row
                col1, col2 = st.columns(2)
                
                with col1:
                    # Delay Reasons Breakdown
                    if 'delay_reason' in zone_detail.columns:
                        zone_delays = zone_detail[
                            (zone_detail['delay_reason'].notna()) & 
                            (zone_detail['delay_reason'] != 'No Delay') &
                            (zone_detail['delay_reason'] != '')
                        ]
                        if len(zone_delays) > 0:
                            delay_breakdown = zone_delays['delay_reason'].value_counts().reset_index()
                            delay_breakdown.columns = ['Reason', 'Count']
                            
                            fig = px.pie(delay_breakdown, values='Count', names='Reason',
                                        color_discrete_sequence=CHART_COLORS, hole=0.4)
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#e8e8e8',
                                title=dict(text='Delay Reasons Breakdown', font=dict(color='#ffffff')),
                                margin=dict(l=0, r=0, t=40, b=0)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No delays in this zone.")
                    else:
                        st.info("Delay reason data not available.")
                
                with col2:
                    # DELIVERY PARTNER PERFORMANCE
                    if 'delivery_partner' in zone_detail.columns:
                        zone_detail_copy = zone_detail.copy()
                        if 'actual_delivery_date' in zone_detail_copy.columns and 'promised_date' in zone_detail_copy.columns:
                            zone_detail_copy['is_breach'] = zone_detail_copy['actual_delivery_date'] > zone_detail_copy['promised_date']
                        else:
                            zone_detail_copy['is_breach'] = False
                        
                        partner_perf = zone_detail_copy.groupby('delivery_partner').agg({
                            'order_id': 'count'
                        }).reset_index()
                        partner_perf.columns = ['Partner', 'Deliveries']
                        
                        breach_by_partner = zone_detail_copy[zone_detail_copy['is_breach'] == True].groupby('delivery_partner').size().reset_index()
                        breach_by_partner.columns = ['Partner', 'Breaches']
                        
                        partner_perf = partner_perf.merge(breach_by_partner, on='Partner', how='left')
                        partner_perf['Breaches'] = partner_perf['Breaches'].fillna(0)
                        partner_perf['On-Time Rate'] = ((partner_perf['Deliveries'] - partner_perf['Breaches']) / partner_perf['Deliveries'] * 100).round(1)
                        partner_perf = partner_perf.sort_values('Deliveries', ascending=True)
                        
                        fig = px.bar(partner_perf, x='On-Time Rate', y='Partner', orientation='h',
                                    color='On-Time Rate', color_continuous_scale=['#f87171', '#fb923c', '#4ade80'],
                                    text='On-Time Rate')
                        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#e8e8e8', showlegend=False, coloraxis_showscale=False,
                            title=dict(text='Delivery Partner Performance', font=dict(color='#ffffff')),
                            xaxis=dict(title='On-Time Rate (%)', range=[0, 110]),
                            yaxis=dict(title=''),
                            margin=dict(l=0, r=0, t=40, b=0)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Delivery partner data not available.")
        else:
            st.info("No delivery zones available.")
    else:
        st.info("Delivery zone data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== WHAT-IF ANALYSIS =====
    st.markdown("### 🔮 What-If Analysis")
    st.markdown("*Adjust parameters to project business impact*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📉 Reduce Cancellation Rate")
        cancellation_reduction = st.slider(
            "Reduction percentage:",
            min_value=5, max_value=50, value=20, step=5,
            format="%d%%", key="cancel_slider"
        )
        
        current_cancelled = mgr_kpis['cancelled_orders']
        reduced_cancellations = int(current_cancelled * (cancellation_reduction / 100))
        # FORMULA: Additional Revenue = Cancelled Order Value × (Slider % / 100)
        recovered_revenue = reduced_cancellations * mgr_kpis['avg_order_value']
        
        st.markdown(f"""
        <div class='whatif-box'>
            <p style='color: #e8e8e8; margin-bottom: 10px;'>If cancellations reduced by <strong>{cancellation_reduction}%</strong>:</p>
            <p style='color: #e8e8e8;'>Orders Recovered: <span class='whatif-value'>{reduced_cancellations:,}</span></p>
            <p style='color: #e8e8e8;'>Additional Revenue: <span class='whatif-value'>AED {recovered_revenue:,.0f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🚚 Improve On-Time Delivery")
        delivery_improvement = st.slider(
            "Improvement percentage:",
            min_value=5, max_value=30, value=15, step=5,
            format="%d%%", key="delivery_slider"
        )
        
        current_breaches = mgr_kpis['sla_breach_count']
        reduced_breaches = int(current_breaches * (delivery_improvement / 100))
        avg_refund = mgr_kpis['total_refunds'] / current_breaches if current_breaches > 0 else 50
        cost_savings = reduced_breaches * avg_refund
        new_on_time = min(100, mgr_kpis['on_time_rate'] + delivery_improvement)
        
        st.markdown(f"""
        <div class='whatif-box'>
            <p style='color: #e8e8e8; margin-bottom: 10px;'>If on-time delivery improves by <strong>{delivery_improvement}%</strong>:</p>
            <p style='color: #e8e8e8;'>New On-Time Rate: <span class='whatif-value'>{new_on_time:.1f}%</span></p>
            <p style='color: #e8e8e8;'>Breaches Avoided: <span class='whatif-value'>{reduced_breaches:,}</span></p>
            <p style='color: #e8e8e8;'>Refund Cost Savings: <span class='whatif-value'>AED {cost_savings:,.0f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Combined Impact
    st.markdown("#### 💰 Combined Impact Summary")
    
    total_benefit = recovered_revenue + cost_savings
    
    st.markdown(f"""
    <div class='insight-box' style='border-left-color: #4ade80;'>
        <div class='insight-title' style='color: #4ade80;'>📊 Total Projected Benefit</div>
        <div style='text-align: center; padding: 20px;'>
            <span style='font-size: 2.5rem; font-weight: bold; color: #4ade80;'>AED {total_benefit:,.0f}</span>
            <p style='color: #e8e8e8; margin-top: 15px;'>
                Additional Revenue: <strong>AED {recovered_revenue:,.0f}</strong> | 
                Cost Savings: <strong>AED {cost_savings:,.0f}</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# FOOTER
# ================================================================================

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 30px 0; color: #8facc4;'>
    <p style='font-size: 0.9rem; margin-bottom: 5px;'>
        🛍️ <strong>SouqPlus Analytics Dashboard</strong> 🛍️
    </p>
    <p style='font-size: 0.8rem; color: #6b8aae;'>
        Developed by Group 1 | Master of AI in Business | SP Jain School of Global Management
    </p>
    <p style='font-size: 0.7rem; color: #4a6a8a; margin-top: 10px;'>
        © 2025 | Built with Streamlit & Plotly
    </p>
</div>
""", unsafe_allow_html=True)
