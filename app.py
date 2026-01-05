"""
================================================================================
SOUQPLUS ANALYTICS DASHBOARD - UPDATED WITH PROFESSOR FEEDBACK
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
        cursor: help;
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
    
    .kpi-subtitle {
        color: #6b8aae;
        font-size: 0.75rem;
        margin-top: 5px;
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
    
    .filter-container {
        background: rgba(58, 134, 255, 0.05);
        border: 1px solid #2a4a7f;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 15px;
    }
    
    .filter-label {
        color: #8facc4;
        font-size: 0.8rem;
        margin-bottom: 5px;
    }
    
    .breach-breakdown {
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid #f87171;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
    }
    
    .breach-item {
        color: #e8e8e8;
        font-size: 0.8rem;
        padding: 3px 0;
    }
    
    .tier-bronze { color: #cd7f32; }
    .tier-silver { color: #c0c0c0; }
    .tier-gold { color: #ffd700; }
    .tier-platinum { color: #e5e4e2; }
</style>
""", unsafe_allow_html=True)

# ================================================================================
# HELPER FUNCTIONS
# ================================================================================

def format_number_short(num):
    """Format number in shortened format (e.g., 2.2M, 150K)"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

def format_currency_short(num):
    """Format currency in shortened format with AED"""
    if num >= 1_000_000:
        return f"AED {num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"AED {num/1_000:.1f}K"
    else:
        return f"AED {num:.0f}"

def format_currency_full(num):
    """Format currency with full number"""
    return f"AED {num:,.2f}"

# ================================================================================
# DATA LOADING AND CLEANING
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
        
        # ===== 1. REMOVE DUPLICATES =====
        if 'customer_id' in customers.columns:
            customers = customers.drop_duplicates(subset=['customer_id'], keep='first')
        else:
            customers = customers.drop_duplicates(keep='first')
        
        if 'order_id' in orders.columns:
            orders = orders.drop_duplicates(subset=['order_id'], keep='first')
        else:
            orders = orders.drop_duplicates(keep='first')
        
        if 'order_item_id' in order_items.columns:
            order_items = order_items.drop_duplicates(subset=['order_item_id'], keep='first')
        elif 'item_id' in order_items.columns:
            order_items = order_items.drop_duplicates(subset=['item_id'], keep='first')
        else:
            order_items = order_items.drop_duplicates(keep='first')
        
        if 'fulfillment_id' in fulfillment.columns:
            fulfillment = fulfillment.drop_duplicates(subset=['fulfillment_id'], keep='first')
        elif 'order_id' in fulfillment.columns:
            fulfillment = fulfillment.drop_duplicates(subset=['order_id'], keep='first')
        else:
            fulfillment = fulfillment.drop_duplicates(keep='first')
        
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
        
        # ===== 8. HANDLE OUTLIERS =====
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
        st.info("Please ensure all CSV files are in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
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
# SIDEBAR - GLOBAL FILTERS (Date Range & View Toggle Only)
# ================================================================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='color: #3a86ff; font-size: 1.8rem; margin-bottom: 5px;'>🛍️ SOUQPLUS</h1>
    <p style='color: #8facc4; font-size: 0.85rem; letter-spacing: 3px;'>ANALYTICS DASHBOARD</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== VIEW TOGGLE =====
st.sidebar.markdown("### 📊 Dashboard View")
view_mode = st.sidebar.radio(
    "Select View",
    ["Executive View", "Manager View"],
    index=0,
    help="Executive: Revenue & Growth | Manager: Operations & Issues"
)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== GLOBAL DATE FILTER ONLY =====
st.sidebar.markdown("### 📅 Date Range")
st.sidebar.caption("Global filter applied to all charts")

min_date = orders_df['order_date'].min().date()
max_date = orders_df['order_date'].max().date()
default_start = max(min_date, max_date - timedelta(days=90))

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("From", default_start, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### ℹ️ About Local Filters")
st.sidebar.info("Each chart has its own filter controls for granular analysis. Look for filter dropdowns above each visualization.")

# ================================================================================
# BASE FILTERED DATA (Date Only)
# ================================================================================

base_filtered_orders = orders_df[
    (orders_df['order_date'].dt.date >= start_date) &
    (orders_df['order_date'].dt.date <= end_date)
].copy()

base_filtered_customer_ids = base_filtered_orders['customer_id'].unique()
base_filtered_customers = customers_df[customers_df['customer_id'].isin(base_filtered_customer_ids)]
base_filtered_order_items = order_items_df[order_items_df['order_id'].isin(base_filtered_orders['order_id'])]
base_filtered_fulfillment = fulfillment_df[fulfillment_df['order_id'].isin(base_filtered_orders['order_id'])]
base_filtered_returns = returns_df[returns_df['order_id'].isin(base_filtered_orders['order_id'])]

# ================================================================================
# KPI CALCULATIONS
# ================================================================================

def calculate_executive_kpis(orders):
    """Calculate Executive View KPIs"""
    kpis = {}
    
    if 'order_status' in orders.columns:
        delivered_orders = orders[orders['order_status'] == 'Delivered']
    else:
        delivered_orders = orders
    
    # Total Revenue (full value stored for hover)
    kpis['total_revenue'] = delivered_orders['net_amount'].sum() if 'net_amount' in delivered_orders.columns else 0
    
    # Average Order Value
    kpis['aov'] = delivered_orders['net_amount'].mean() if len(delivered_orders) > 0 and 'net_amount' in delivered_orders.columns else 0
    
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
    
    kpis['total_orders'] = len(orders)
    kpis['delivered_count'] = len(delivered_orders)
    
    return kpis

def calculate_manager_kpis(orders, fulfillment, returns):
    """Calculate Manager View KPIs with SLA Breach Breakdown"""
    kpis = {}
    
    # On-Time Delivery Rate & SLA Breach Details
    if 'actual_delivery_date' in fulfillment.columns and 'promised_date' in fulfillment.columns:
        delivered_fulfillment = fulfillment[fulfillment['actual_delivery_date'].notna()]
        on_time = delivered_fulfillment[
            delivered_fulfillment['actual_delivery_date'] <= delivered_fulfillment['promised_date']
        ]
        late = delivered_fulfillment[
            delivered_fulfillment['actual_delivery_date'] > delivered_fulfillment['promised_date']
        ]
        
        kpis['on_time_rate'] = (len(on_time) / len(delivered_fulfillment) * 100) if len(delivered_fulfillment) > 0 else 0
        kpis['sla_breach_count'] = len(late)
        
        # SLA BREACH BREAKDOWN by Zone, Partner, Reason
        kpis['breach_by_zone'] = {}
        kpis['breach_by_partner'] = {}
        kpis['breach_by_reason'] = {}
        
        if len(late) > 0:
            if 'delivery_zone' in late.columns:
                zone_breaches = late['delivery_zone'].value_counts().head(3).to_dict()
                kpis['breach_by_zone'] = zone_breaches
            
            if 'delivery_partner' in late.columns:
                partner_breaches = late['delivery_partner'].value_counts().head(3).to_dict()
                kpis['breach_by_partner'] = partner_breaches
            
            if 'delay_reason' in late.columns:
                reason_breaches = late[late['delay_reason'] != 'No Delay']['delay_reason'].value_counts().head(3).to_dict()
                kpis['breach_by_reason'] = reason_breaches
    else:
        kpis['on_time_rate'] = 0
        kpis['sla_breach_count'] = 0
        kpis['breach_by_zone'] = {}
        kpis['breach_by_partner'] = {}
        kpis['breach_by_reason'] = {}
    
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
    
    # Total Refunds
    if 'refund_status' in returns.columns and 'refund_amount' in returns.columns:
        kpis['total_refunds'] = returns[returns['refund_status'] == 'Processed']['refund_amount'].sum()
    elif 'refund_amount' in returns.columns:
        kpis['total_refunds'] = returns['refund_amount'].sum()
    else:
        kpis['total_refunds'] = 0
    
    kpis['total_orders'] = len(orders)
    kpis['avg_order_value'] = orders['net_amount'].mean() if len(orders) > 0 and 'net_amount' in orders.columns else 0
    
    return kpis

# Calculate KPIs
exec_kpis = calculate_executive_kpis(base_filtered_orders)
mgr_kpis = calculate_manager_kpis(base_filtered_orders, base_filtered_fulfillment, base_filtered_returns)

# Calculate Refund as % of Revenue
total_revenue_for_refund = exec_kpis['total_revenue']
refund_percentage = (mgr_kpis['total_refunds'] / total_revenue_for_refund * 100) if total_revenue_for_refund > 0 else 0

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
    <p style='color: #6b8aae; font-size: 0.85rem;'>
        📅 {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}
    </p>
</div>
<div class='divider'></div>
""", unsafe_allow_html=True)

# ================================================================================
# EXECUTIVE VIEW
# ================================================================================

if view_mode == "Executive View":
    
    # ===== 4 KPI CARDS (Clean - No Deltas) =====
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total Revenue - Shortened format with hover showing full amount
        revenue_short = format_currency_short(exec_kpis['total_revenue'])
        revenue_full = format_currency_full(exec_kpis['total_revenue'])
        st.markdown(f"""
        <div class='kpi-card' title='Full Amount: {revenue_full}'>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-value'>{revenue_short}</div>
            <div class='kpi-subtitle'>Hover for full amount</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-card' title='Average Order Value: {format_currency_full(exec_kpis["aov"])}'>
            <div class='kpi-label'>Average Order Value</div>
            <div class='kpi-value'>AED {exec_kpis['aov']:,.0f}</div>
            <div class='kpi-subtitle'>{exec_kpis['delivered_count']:,} delivered orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Repeat Customer Rate</div>
            <div class='kpi-value'>{exec_kpis['repeat_rate']:.1f}%</div>
            <div class='kpi-subtitle'>Customers with 2+ orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Discount Rate</div>
            <div class='kpi-value'>{exec_kpis['discount_rate']:.1f}%</div>
            <div class='kpi-subtitle'>Of gross revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 1: REVENUE TREND (with local filter) =====
    st.markdown("### 📊 Revenue Trend")
    
    # LOCAL FILTER for Revenue Trend
    rev_col1, rev_col2, rev_col3 = st.columns([1, 1, 2])
    
    with rev_col1:
        rev_agg_type = st.selectbox("Aggregation", ["Weekly", "Monthly"], key="rev_trend_agg")
    
    with rev_col2:
        rev_channel_options = ['All Channels'] + list(base_filtered_orders['order_channel'].unique()) if 'order_channel' in base_filtered_orders.columns else ['All Channels']
        rev_channel_filter = st.selectbox("Channel", rev_channel_options, key="rev_trend_channel")
    
    # Apply local filter
    rev_trend_data = base_filtered_orders.copy()
    if rev_channel_filter != 'All Channels' and 'order_channel' in rev_trend_data.columns:
        rev_trend_data = rev_trend_data[rev_trend_data['order_channel'] == rev_channel_filter]
    
    if 'order_status' in rev_trend_data.columns:
        delivered = rev_trend_data[rev_trend_data['order_status'] == 'Delivered'].copy()
    else:
        delivered = rev_trend_data.copy()
    
    if len(delivered) > 0 and 'net_amount' in delivered.columns:
        if rev_agg_type == "Weekly":
            delivered['period'] = delivered['order_date'].dt.to_period('W').apply(lambda x: x.start_time)
        else:
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
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 2 & 3: Revenue by City & Channel Contribution =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏙️ Revenue by City")
        
        # LOCAL FILTER for City Chart
        city_segment_options = ['All Segments'] + list(customers_df['customer_segment'].unique()) if 'customer_segment' in customers_df.columns else ['All Segments']
        city_segment_filter = st.selectbox("Customer Segment", city_segment_options, key="city_segment_filter")
        
        # Apply local filter
        city_filtered_customers = base_filtered_customers.copy()
        if city_segment_filter != 'All Segments' and 'customer_segment' in city_filtered_customers.columns:
            city_filtered_customers = city_filtered_customers[city_filtered_customers['customer_segment'] == city_segment_filter]
        
        city_filtered_orders = base_filtered_orders[base_filtered_orders['customer_id'].isin(city_filtered_customers['customer_id'])]
        
        if 'city' in customers_df.columns:
            city_revenue = city_filtered_orders.merge(customers_df[['customer_id', 'city']], on='customer_id')
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
    
    with col2:
        st.markdown("### 📱 Channel Contribution")
        
        # LOCAL FILTER for Channel Chart
        channel_city_options = ['All Cities'] + list(customers_df['city'].unique()) if 'city' in customers_df.columns else ['All Cities']
        channel_city_filter = st.selectbox("City", channel_city_options, key="channel_city_filter")
        
        # Apply local filter
        channel_filtered_orders = base_filtered_orders.copy()
        if channel_city_filter != 'All Cities' and 'city' in customers_df.columns:
            city_customer_ids = customers_df[customers_df['city'] == channel_city_filter]['customer_id']
            channel_filtered_orders = channel_filtered_orders[channel_filtered_orders['customer_id'].isin(city_customer_ids)]
        
        if len(channel_filtered_orders) > 0 and 'order_channel' in channel_filtered_orders.columns:
            channel_orders = channel_filtered_orders.groupby('order_channel').agg({
                'order_id': 'count', 'net_amount': 'sum'
            }).reset_index()
            channel_orders.columns = ['Channel', 'Orders', 'Revenue']
            
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
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 4: Category Revenue by City =====
    st.markdown("### 🛍️ Category Revenue Analysis")
    
    # LOCAL FILTERS for Category Chart
    cat_col1, cat_col2, cat_col3 = st.columns([1, 1, 2])
    
    with cat_col1:
        cat_city_options = ['All Cities'] + list(customers_df['city'].unique()) if 'city' in customers_df.columns else ['All Cities']
        cat_city_filter = st.selectbox("Filter by City", cat_city_options, key="cat_city_filter")
    
    with cat_col2:
        cat_channel_options = ['All Channels'] + list(base_filtered_orders['order_channel'].unique()) if 'order_channel' in base_filtered_orders.columns else ['All Channels']
        cat_channel_filter = st.selectbox("Filter by Channel", cat_channel_options, key="cat_channel_filter")
    
    # Apply local filters
    cat_filtered_orders = base_filtered_orders.copy()
    if cat_city_filter != 'All Cities' and 'city' in customers_df.columns:
        city_customers = customers_df[customers_df['city'] == cat_city_filter]['customer_id']
        cat_filtered_orders = cat_filtered_orders[cat_filtered_orders['customer_id'].isin(city_customers)]
    
    if cat_channel_filter != 'All Channels' and 'order_channel' in cat_filtered_orders.columns:
        cat_filtered_orders = cat_filtered_orders[cat_filtered_orders['order_channel'] == cat_channel_filter]
    
    cat_filtered_items = base_filtered_order_items[base_filtered_order_items['order_id'].isin(cat_filtered_orders['order_id'])]
    
    if 'product_category' in cat_filtered_items.columns and len(cat_filtered_items) > 0:
        cat_revenue = cat_filtered_items.groupby('product_category')['item_total'].sum().reset_index()
        cat_revenue.columns = ['Category', 'Revenue']
        cat_revenue = cat_revenue.sort_values('Revenue', ascending=False)
        
        fig = px.bar(cat_revenue, x='Category', y='Revenue', color='Category',
                    color_discrete_sequence=CHART_COLORS)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8e8e8', showlegend=False,
            xaxis=dict(gridcolor='rgba(58,134,255,0.1)', title=''),
            yaxis=dict(gridcolor='rgba(58,134,255,0.1)', title='Revenue (AED)'),
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No category data available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CUSTOMER TIER DISTRIBUTION =====
    st.markdown("### 👑 Customer Tier Distribution")
    
    # LOCAL FILTER for Tier Chart
    tier_col1, tier_col2, _ = st.columns([1, 1, 2])
    
    with tier_col1:
        tier_city_options = ['All Cities'] + list(customers_df['city'].unique()) if 'city' in customers_df.columns else ['All Cities']
        tier_city_filter = st.selectbox("Filter by City", tier_city_options, key="tier_city_filter")
    
    # Apply local filter
    tier_filtered_customers = base_filtered_customers.copy()
    if tier_city_filter != 'All Cities' and 'city' in tier_filtered_customers.columns:
        tier_filtered_customers = tier_filtered_customers[tier_filtered_customers['city'] == tier_city_filter]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'customer_tier' in tier_filtered_customers.columns:
            tier_dist = tier_filtered_customers['customer_tier'].value_counts().reset_index()
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
            tier_customer_ids = tier_filtered_customers['customer_id']
            tier_orders = base_filtered_orders[base_filtered_orders['customer_id'].isin(tier_customer_ids)]
            tier_revenue = tier_orders.merge(customers_df[['customer_id', 'customer_tier']], on='customer_id')
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
    top_city, top_city_rev = "N/A", 0
    if 'city' in customers_df.columns:
        city_revenue = base_filtered_orders.merge(customers_df[['customer_id', 'city']], on='customer_id')
        if 'order_status' in city_revenue.columns:
            city_revenue = city_revenue[city_revenue['order_status'] == 'Delivered']
        if len(city_revenue) > 0:
            city_agg = city_revenue.groupby('city')['net_amount'].sum()
            if len(city_agg) > 0:
                top_city = city_agg.idxmax()
                top_city_rev = city_agg.max()
    
    top_channel = "N/A"
    if 'order_channel' in base_filtered_orders.columns:
        top_channel = base_filtered_orders['order_channel'].value_counts().idxmax()
    
    st.markdown(f"""
    <div class='insight-box'>
        <div class='insight-title'>📊 Key Findings</div>
        <div class='insight-text'>
            <p>• <strong>Total Revenue: {format_currency_full(exec_kpis['total_revenue'])}</strong> from {exec_kpis['delivered_count']:,} delivered orders.</p>
            <p>• <strong>Top City: {top_city}</strong> with {format_currency_short(top_city_rev)} in revenue.</p>
            <p>• <strong>Leading Channel: {top_channel}</strong> — consider optimizing other channels for growth.</p>
            <p>• <strong>Repeat Rate: {exec_kpis['repeat_rate']:.1f}%</strong> — {'Strong customer loyalty!' if exec_kpis['repeat_rate'] > 30 else 'Consider retention campaigns.'}</p>
            <p>• <strong>Discount Burn: {exec_kpis['discount_rate']:.1f}%</strong> of gross revenue.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# MANAGER VIEW
# ================================================================================

else:
    
    # ===== 4 KPI CARDS (Clean - No Deltas) WITH BREACH BREAKDOWN =====
    st.markdown("### 🔧 Operational KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>On-Time Delivery Rate</div>
            <div class='kpi-value'>{mgr_kpis['on_time_rate']:.1f}%</div>
            <div class='kpi-subtitle'>Target: 85%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # SLA BREACH WITH BREAKDOWN
        breach_breakdown_html = ""
        if mgr_kpis['breach_by_zone']:
            breach_breakdown_html += "<div class='breach-breakdown'><strong style='color:#f87171;'>Top Breach Zones:</strong>"
            for zone, count in list(mgr_kpis['breach_by_zone'].items())[:3]:
                breach_breakdown_html += f"<div class='breach-item'>• {zone}: {count}</div>"
            breach_breakdown_html += "</div>"
        
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>SLA Breach Count</div>
            <div class='kpi-value' style='color: #f87171;'>{mgr_kpis['sla_breach_count']:,}</div>
            {breach_breakdown_html}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Cancellation Rate</div>
            <div class='kpi-value'>{mgr_kpis['cancellation_rate']:.1f}%</div>
            <div class='kpi-subtitle'>{mgr_kpis['cancelled_orders']:,} cancelled orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # TOTAL REFUNDS AS % OF REVENUE
        refund_short = format_currency_short(mgr_kpis['total_refunds'])
        st.markdown(f"""
        <div class='kpi-card' title='Full Amount: {format_currency_full(mgr_kpis["total_refunds"])}'>
            <div class='kpi-label'>Total Refunds</div>
            <div class='kpi-value' style='color: #fb923c;'>{refund_short}</div>
            <div class='kpi-subtitle' style='color: #f87171;'>{refund_percentage:.1f}% of Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== ADDITIONAL BREACH BREAKDOWN DETAILS =====
    if mgr_kpis['breach_by_partner'] or mgr_kpis['breach_by_reason']:
        st.markdown("#### 📍 SLA Breach Breakdown Details")
        
        breach_col1, breach_col2, breach_col3 = st.columns(3)
        
        with breach_col1:
            st.markdown("**By Delivery Zone:**")
            if mgr_kpis['breach_by_zone']:
                for zone, count in mgr_kpis['breach_by_zone'].items():
                    st.markdown(f"• {zone}: **{count}**")
            else:
                st.markdown("*No zone data*")
        
        with breach_col2:
            st.markdown("**By Delivery Partner:**")
            if mgr_kpis['breach_by_partner']:
                for partner, count in mgr_kpis['breach_by_partner'].items():
                    st.markdown(f"• {partner}: **{count}**")
            else:
                st.markdown("*No partner data*")
        
        with breach_col3:
            st.markdown("**By Delay Reason:**")
            if mgr_kpis['breach_by_reason']:
                for reason, count in mgr_kpis['breach_by_reason'].items():
                    st.markdown(f"• {reason}: **{count}**")
            else:
                st.markdown("*No reason data*")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 1 & 2: SLA Breach Trend & Breaches by Zone =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 SLA Breach Trend")
        
        # LOCAL FILTER
        breach_partner_options = ['All Partners'] + list(base_filtered_fulfillment['delivery_partner'].unique()) if 'delivery_partner' in base_filtered_fulfillment.columns else ['All Partners']
        breach_partner_filter = st.selectbox("Filter by Partner", breach_partner_options, key="breach_partner_filter")
        
        breach_data = base_filtered_fulfillment.copy()
        if breach_partner_filter != 'All Partners' and 'delivery_partner' in breach_data.columns:
            breach_data = breach_data[breach_data['delivery_partner'] == breach_partner_filter]
        
        if 'actual_delivery_date' in breach_data.columns and 'promised_date' in breach_data.columns:
            breach_data = breach_data[
                (breach_data['actual_delivery_date'].notna()) &
                (breach_data['actual_delivery_date'] > breach_data['promised_date'])
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
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No SLA breaches found! ✅")
        else:
            st.info("Delivery date data not available.")
    
    with col2:
        st.markdown("### 📍 Breaches by Zone (Top 10)")
        
        # LOCAL FILTER
        zone_partner_options = ['All Partners'] + list(base_filtered_fulfillment['delivery_partner'].unique()) if 'delivery_partner' in base_filtered_fulfillment.columns else ['All Partners']
        zone_partner_filter = st.selectbox("Filter by Partner", zone_partner_options, key="zone_partner_filter")
        
        zone_breach_data = base_filtered_fulfillment.copy()
        if zone_partner_filter != 'All Partners' and 'delivery_partner' in zone_breach_data.columns:
            zone_breach_data = zone_breach_data[zone_breach_data['delivery_partner'] == zone_partner_filter]
        
        if 'actual_delivery_date' in zone_breach_data.columns and 'promised_date' in zone_breach_data.columns:
            zone_breach_data = zone_breach_data[
                (zone_breach_data['actual_delivery_date'].notna()) &
                (zone_breach_data['actual_delivery_date'] > zone_breach_data['promised_date'])
            ]
            
            if len(zone_breach_data) > 0 and 'delivery_zone' in zone_breach_data.columns:
                zone_breaches = zone_breach_data.groupby('delivery_zone').size().reset_index()
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
                st.info("No zone breach data available.")
        else:
            st.info("Delivery data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== CHART 3 & 4: Pareto & Return Rate =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Delay Reasons (Pareto)")
        
        # LOCAL FILTER
        delay_zone_options = ['All Zones'] + list(base_filtered_fulfillment['delivery_zone'].dropna().unique()) if 'delivery_zone' in base_filtered_fulfillment.columns else ['All Zones']
        delay_zone_filter = st.selectbox("Filter by Zone", delay_zone_options, key="delay_zone_filter")
        
        delay_data = base_filtered_fulfillment.copy()
        if delay_zone_filter != 'All Zones' and 'delivery_zone' in delay_data.columns:
            delay_data = delay_data[delay_data['delivery_zone'] == delay_zone_filter]
        
        if 'delay_reason' in delay_data.columns:
            delay_data = delay_data[
                (delay_data['delay_reason'].notna()) &
                (delay_data['delay_reason'] != 'No Delay') &
                (delay_data['delay_reason'] != 'Order Cancelled') &
                (delay_data['delay_reason'] != '')
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
        
        # LOCAL FILTER
        return_city_options = ['All Cities'] + list(customers_df['city'].unique()) if 'city' in customers_df.columns else ['All Cities']
        return_city_filter = st.selectbox("Filter by City", return_city_options, key="return_city_filter")
        
        # Apply local filter
        return_filtered_orders = base_filtered_orders.copy()
        if return_city_filter != 'All Cities' and 'city' in customers_df.columns:
            city_customers = customers_df[customers_df['city'] == return_city_filter]['customer_id']
            return_filtered_orders = return_filtered_orders[return_filtered_orders['customer_id'].isin(city_customers)]
        
        return_filtered_items = base_filtered_order_items[base_filtered_order_items['order_id'].isin(return_filtered_orders['order_id'])]
        return_filtered_returns = base_filtered_returns[base_filtered_returns['order_id'].isin(return_filtered_orders['order_id'])]
        
        if 'product_category' in return_filtered_items.columns and len(return_filtered_returns) > 0:
            returns_cat = return_filtered_returns.merge(
                return_filtered_items[['order_id', 'product_category']].drop_duplicates('order_id'),
                on='order_id', how='left'
            )
            
            cat_returns = returns_cat.groupby('product_category').size().reset_index()
            cat_returns.columns = ['Category', 'Returns']
            
            cat_orders = return_filtered_items.groupby('product_category')['order_id'].nunique().reset_index()
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
                              range=[0, max(return_rate['Return Rate']) * 1.3]),
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
    
    # LOCAL FILTER
    table_col1, table_col2, _ = st.columns([1, 1, 2])
    
    with table_col1:
        table_partner_options = ['All Partners'] + list(base_filtered_fulfillment['delivery_partner'].unique()) if 'delivery_partner' in base_filtered_fulfillment.columns else ['All Partners']
        table_partner_filter = st.selectbox("Filter by Partner", table_partner_options, key="table_partner_filter")
    
    # Apply local filter
    table_data = base_filtered_fulfillment.copy()
    if table_partner_filter != 'All Partners' and 'delivery_partner' in table_data.columns:
        table_data = table_data[table_data['delivery_partner'] == table_partner_filter]
    
    if 'delivery_zone' in table_data.columns and 'actual_delivery_date' in table_data.columns:
        zone_analysis = table_data.copy()
        zone_analysis['is_breach'] = zone_analysis['actual_delivery_date'] > zone_analysis['promised_date']
        zone_analysis['delay_days'] = (zone_analysis['actual_delivery_date'] - zone_analysis['promised_date']).dt.days
        zone_analysis.loc[zone_analysis['delay_days'] < 0, 'delay_days'] = 0
        
        problem_zones = zone_analysis.groupby('delivery_zone').agg({
            'is_breach': 'sum',
            'delay_days': 'mean',
            'delay_reason': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A',
            'order_id': 'count'
        }).reset_index()
        problem_zones.columns = ['Delivery Zone', 'SLA Breaches', 'Avg Delay Days', 'Top Delay Reason', 'Total Orders']
        problem_zones = problem_zones.sort_values('SLA Breaches', ascending=False).head(10)
        problem_zones['Avg Delay Days'] = problem_zones['Avg Delay Days'].round(1)
        
        st.dataframe(
            problem_zones,
            use_container_width=True,
            column_config={
                "Delivery Zone": st.column_config.TextColumn("Delivery Zone"),
                "SLA Breaches": st.column_config.NumberColumn("SLA Breaches", format="%d"),
                "Avg Delay Days": st.column_config.NumberColumn("Avg Delay (Days)", format="%.1f"),
                "Top Delay Reason": st.column_config.TextColumn("Primary Reason"),
                "Total Orders": st.column_config.NumberColumn("Total Orders", format="%d")
            }
        )
    else:
        st.info("Zone analysis data not available.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== DRILL-DOWN =====
    st.markdown("### 🔍 Zone Drill-Down Analysis")
    
    # LOCAL FILTER
    if 'delivery_zone' in base_filtered_fulfillment.columns:
        zone_list = base_filtered_fulfillment['delivery_zone'].dropna().unique().tolist()
        
        if len(zone_list) > 0:
            selected_zone = st.selectbox("Select a Delivery Zone", zone_list, key="drill_zone")
            
            if selected_zone:
                zone_detail = base_filtered_fulfillment[base_filtered_fulfillment['delivery_zone'] == selected_zone]
                zone_orders = base_filtered_orders[base_filtered_orders['order_id'].isin(zone_detail['order_id'])]
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Deliveries", f"{len(zone_detail):,}")
                
                with col2:
                    if 'actual_delivery_date' in zone_detail.columns and 'promised_date' in zone_detail.columns:
                        on_time_zone = len(zone_detail[zone_detail['actual_delivery_date'] <= zone_detail['promised_date']])
                        on_time_pct = (on_time_zone / len(zone_detail) * 100) if len(zone_detail) > 0 else 0
                    else:
                        on_time_pct = 0
                    st.metric("On-Time Rate", f"{on_time_pct:.1f}%")
                
                with col3:
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
                
                # Partner Performance Chart
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'delay_reason' in zone_detail.columns:
                        zone_delays = zone_detail[
                            (zone_detail['delay_reason'].notna()) & 
                            (zone_detail['delay_reason'] != 'No Delay')
                        ]
                        if len(zone_delays) > 0:
                            delay_breakdown = zone_delays['delay_reason'].value_counts().reset_index()
                            delay_breakdown.columns = ['Reason', 'Count']
                            
                            fig = px.pie(delay_breakdown, values='Count', names='Reason',
                                        color_discrete_sequence=CHART_COLORS, hole=0.4)
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#e8e8e8',
                                title=dict(text='Delay Reasons', font=dict(color='#ffffff')),
                                margin=dict(l=0, r=0, t=40, b=0)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No delays in this zone.")
                
                with col2:
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
                            title=dict(text='Partner Performance', font=dict(color='#ffffff')),
                            xaxis=dict(title='On-Time Rate (%)', range=[0, 110]),
                            yaxis=dict(title=''),
                            margin=dict(l=0, r=0, t=40, b=0)
                        )
                        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # ===== WHAT-IF ANALYSIS =====
    st.markdown("### 🔮 What-If Analysis")
    
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
        recovered_revenue = reduced_cancellations * mgr_kpis['avg_order_value']
        
        st.markdown(f"""
        <div class='whatif-box'>
            <p style='color: #e8e8e8;'>If cancellations reduced by <strong>{cancellation_reduction}%</strong>:</p>
            <p style='color: #e8e8e8;'>Orders Recovered: <span class='whatif-value'>{reduced_cancellations:,}</span></p>
            <p style='color: #e8e8e8;'>Additional Revenue: <span class='whatif-value'>{format_currency_short(recovered_revenue)}</span></p>
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
            <p style='color: #e8e8e8;'>If on-time delivery improves by <strong>{delivery_improvement}%</strong>:</p>
            <p style='color: #e8e8e8;'>New On-Time Rate: <span class='whatif-value'>{new_on_time:.1f}%</span></p>
            <p style='color: #e8e8e8;'>Breaches Avoided: <span class='whatif-value'>{reduced_breaches:,}</span></p>
            <p style='color: #e8e8e8;'>Refund Savings: <span class='whatif-value'>{format_currency_short(cost_savings)}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Combined Impact
    total_benefit = recovered_revenue + cost_savings
    
    st.markdown(f"""
    <div class='insight-box' style='border-left-color: #4ade80;'>
        <div class='insight-title' style='color: #4ade80;'>💰 Total Projected Benefit</div>
        <div style='text-align: center; padding: 20px;'>
            <span style='font-size: 2.5rem; font-weight: bold; color: #4ade80;'>{format_currency_short(total_benefit)}</span>
            <p style='color: #e8e8e8; margin-top: 15px;'>
                Revenue Recovery: <strong>{format_currency_short(recovered_revenue)}</strong> | 
                Cost Savings: <strong>{format_currency_short(cost_savings)}</strong>
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
