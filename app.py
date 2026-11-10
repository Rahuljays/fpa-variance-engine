import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ==========================================
# PAGE CONFIGURATION & DESIGN SYSTEM
# ==========================================
st.set_page_config(
    page_title="Enterprise FP&A Variance Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Minimalist Executive CSS Injection
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #fafbfc;
            color: #111827;
        }

        .main {
            background-color: #fafbfc;
            padding: 2rem 3rem;
        }

        /* Executive Header Banner */
        .executive-header {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            padding: 2.5rem 3rem;
            border-radius: 16px;
            margin-bottom: 2.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }
        .executive-header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            color: #111827;
            margin: 0;
            letter-spacing: -0.02em;
        }
        .executive-header p {
            font-size: 1rem;
            color: #4b5563;
            margin-top: 0.5rem;
            font-weight: 400;
        }

        /* Metric Cards */
        div.stMetric {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 20px 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease;
        }
        div.stMetric:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-color: #d1d5db;
        }

        [data-testid="stMetricLabel"] {
            font-weight: 500;
            font-size: 0.8rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        [data-testid="stMetricValue"] {
            font-weight: 700;
            font-size: 1.85rem;
            color: #111827;
            letter-spacing: -0.02em;
        }

        /* Navigation Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f3f4f6;
            padding: 6px;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid #e5e7eb;
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.875rem;
            color: #4b5563;
            background-color: transparent;
            border: none;
            padding: 0 20px;
            transition: all 0.2s ease;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #111827 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        /* Chart & Table Containers */
        div[data-testid="stVerticalBlock"] > div > div.stDataFrame, 
        div[data-testid="stVerticalBlock"] > div > div.stPlotlyChart {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            border: 1px solid #e5e7eb;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #f3f4f6;
            border-right: 1px solid #e5e7eb;
            padding-top: 2rem;
        }

        /* Footer */
        .executive-footer {
            text-align: center;
            padding: 3rem 0;
            color: #6b7280;
            font-size: 0.85rem;
            border-top: 1px solid #e5e7eb;
            margin-top: 4rem;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# AUTO-GENERATE ROBUST MOCK DATA (WITH MONTH)
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

bva_path = os.path.join(data_dir, 'bva_data.csv')
pvm_path = os.path.join(data_dir, 'pvm_data.csv')
cost_path = os.path.join(data_dir, 'cost_data.csv')

np.random.seed(42)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# 1. BvA Data
departments = ['Sales', 'Engineering', 'Operations', 'Finance', 'Marketing']
line_items = [
    ('Salaries & Wages', '6000', 50000),
    ('Cloud Hosting / AWS', '6100', 12000),
    ('Software Subscriptions', '6200', 5000),
    ('Marketing Campaigns', '6300', 20000),
    ('Office & Admin', '6400', 4000)
]
bva_rows = []
for dept in departments:
    for item, code, base_budget in line_items:
        for m in months:
            budget = base_budget * np.random.uniform(0.95, 1.05)
            actual = budget * np.random.uniform(0.90, 1.15)
            bva_rows.append({
                'Department': dept, 'Account_Code': code, 'Line_Item': item,
                'Month': m, 'Budget_Amount': round(budget, 2), 'Actual_Amount': round(actual, 2)
            })
pd.DataFrame(bva_rows).to_csv(bva_path, index=False)

# 2. PVM Data
product_lines = ['Enterprise Suite', 'Pro Tier', 'API Connector', 'Starter Pack']
pvm_rows = []
for prod in product_lines:
    base_units = np.random.randint(500, 2000)
    base_price = np.random.randint(50, 500)
    for m in months:
        b_units = base_units * np.random.uniform(0.95, 1.05)
        a_units = b_units * np.random.uniform(0.85, 1.20)
        b_price = base_price
        a_price = b_price * np.random.uniform(0.95, 1.08)
        pvm_rows.append({
            'Product_Line': prod, 'Month': m,
            'Budget_Units': int(b_units), 'Actual_Units': int(a_units),
            'Budget_Price': round(b_price, 2), 'Actual_Price': round(a_price, 2)
        })
pd.DataFrame(pvm_rows).to_csv(pvm_path, index=False)

# 3. Cost Data
cost_centers = ['Assembly Line A', 'Machining', 'Packaging & Shipping']
cost_items = [
    ('Direct Labor', 25.0, 1000),
    ('Raw Materials (Steel/Alloy)', 150.0, 300),
    ('Machine Maintenance', 75.0, 150)
]
cost_rows = []
for cc in cost_centers:
    for item, std_rate, std_qty in cost_items:
        for m in months:
            s_rate = std_rate
            a_rate = s_rate * np.random.uniform(0.95, 1.12)
            s_qty = std_qty * np.random.uniform(0.95, 1.05)
            a_qty = s_qty * np.random.uniform(0.90, 1.15)
            cost_rows.append({
                'Cost_Center': cc, 'Item': item, 'Month': m,
                'Standard_Rate': round(s_rate, 2), 'Actual_Rate': round(a_rate, 2),
                'Standard_Hours_Units': round(s_qty, 2), 'Actual_Hours_Units': round(a_qty, 2)
            })
pd.DataFrame(cost_rows).to_csv(cost_path, index=False)

# Import custom variance modules
from modules.bva import calculate_bva_variance
from modules.pvm import calculate_pvm_variance
from modules.costs import calculate_cost_variances


# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_all_data():
    bva_df = calculate_bva_variance(pd.read_csv(bva_path))
    pvm_df = calculate_pvm_variance(pd.read_csv(pvm_path))
    cost_df = calculate_cost_variances(pd.read_csv(cost_path))
    return bva_df, pvm_df, cost_df


bva_df, pvm_df, cost_df = load_all_data()

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### 🎛️ **Control Panel**")
selected_month = st.sidebar.selectbox(
    "Reporting Period",
    options=['All Months'] + list(bva_df['Month'].unique())
)

if selected_month == 'All Months':
    f_bva, f_pvm, f_cost = bva_df, pvm_df, cost_df
else:
    f_bva = bva_df[bva_df['Month'] == selected_month]
    f_pvm = pvm_df[pvm_df['Month'] == selected_month]
    f_cost = cost_df[cost_df['Month'] == selected_month]

# ==========================================
# HEADER BANNER
# ==========================================
st.markdown("""
    <div class="executive-header">
        <h1>Enterprise FP&A Variance Engine</h1>
        <p>Automated Financial Ledger Variance Analysis, Revenue PVM Deconstruction, and Cost Control</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# NAVIGATION TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Budget vs. Actual",
    "📈 Revenue PVM",
    "⚙️ Cost Variances",
    "🔮 Scenario Simulator"
])

# ==========================================
# TAB 1: BUDGET VS. ACTUAL (BvA)
# ==========================================
with tab1:
    st.subheader("Departmental Budget Performance")
    total_budget = f_bva['Budget_Amount'].sum()
    total_actual = f_bva['Actual_Amount'].sum()
    total_var = f_bva['Absolute_Variance'].sum()
    pct_var = (total_var / total_budget) * 100 if total_budget != 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Budget", f"${total_budget:,.2f}")
    col2.metric("Actual Spend", f"${total_actual:,.2f}")
    col3.metric("Net Variance", f"${total_var:,.2f}", delta=f"{pct_var:.2f}%", delta_color="inverse")
    col4.metric("Period", selected_month)

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("### Variance by Department")
        dept_summary = f_bva.groupby('Department')[['Budget_Amount', 'Actual_Amount']].sum().reset_index()
        fig_dept = px.bar(dept_summary, x='Department', y=['Budget_Amount', 'Actual_Amount'], barmode='group',
                          color_discrete_sequence=['#2563eb', '#f59e0b'])
        fig_dept.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family='Inter')
        st.plotly_chart(fig_dept, width='stretch')

    with col_chart2:
        st.markdown("### Status Breakdown")
        status_counts = f_bva['Variance_Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_status = px.pie(status_counts, names='Status', values='Count', hole=0.5,
                            color_discrete_map={'Unfavorable (U)': '#dc2626', 'Favorable (F)': '#16a34a'})
        fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family='Inter')
        st.plotly_chart(fig_status, width='stretch')

    st.markdown("### Detailed BvA Ledger Table")
    st.dataframe(f_bva, width='stretch')

# ==========================================
# TAB 2: PVM ANALYSIS
# ==========================================
with tab2:
    st.subheader("Top-Line Revenue PVM Deconstruction")
    rev_budget = f_pvm['Budget_Revenue'].sum()
    rev_actual = f_pvm['Actual_Revenue'].sum()
    vol_impact = f_pvm['Volume_Variance'].sum()
    price_impact = f_pvm['Price_Variance'].sum()
    mix_impact = f_pvm['Mix_Variance'].sum()

    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
    pcol1.metric("Baseline Revenue", f"${rev_budget:,.2f}")
    pcol2.metric("Actual Revenue", f"${rev_actual:,.2f}", delta=f"${rev_actual - rev_budget:,.2f}")
    pcol3.metric("Volume Impact", f"${vol_impact:,.2f}")
    pcol4.metric("Price Realization", f"${price_impact:,.2f}")

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    pvm_totals = pd.DataFrame({
        'Driver': ['Volume Variance', 'Price Variance', 'Mix/Interaction', 'Net Variance'],
        'Impact': [vol_impact, price_impact, mix_impact, (rev_actual - rev_budget)]
    })
    fig_pvm = px.bar(pvm_totals, x='Driver', y='Impact', color='Driver',
                     color_discrete_sequence=['#2563eb', '#16a34a', '#f59e0b', '#dc2626'])
    fig_pvm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family='Inter',
                          showlegend=False)
    st.plotly_chart(fig_pvm, width='stretch')
    st.dataframe(f_pvm, width='stretch')

# ==========================================
# TAB 3: OPERATIONAL COST VARIANCES
# ==========================================
with tab3:
    st.subheader("Standard Costing: Rate vs. Efficiency")
    std_c = f_cost['Standard_Cost'].sum()
    act_c = f_cost['Actual_Cost'].sum()
    rate_var = f_cost['Rate_Price_Variance'].sum()
    eff_var = f_cost['Efficiency_Usage_Variance'].sum()

    ccol1, ccol2, ccol3, ccol4 = st.columns(4)
    ccol1.metric("Standard Cost", f"${std_c:,.2f}")
    ccol2.metric("Actual Cost", f"${act_c:,.2f}")
    ccol3.metric("Rate Variance", f"${rate_var:,.2f}")
    ccol4.metric("Efficiency Variance", f"${eff_var:,.2f}")

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    fig_cost = px.bar(f_cost, x='Cost_Center', y=['Rate_Price_Variance', 'Efficiency_Usage_Variance'], barmode='group',
                      color_discrete_sequence=['#f59e0b', '#2563eb'])
    fig_cost.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family='Inter')
    st.plotly_chart(fig_cost, width='stretch')
    st.dataframe(f_cost, width='stretch')

# ==========================================
# TAB 4: SCENARIO STRESS-TESTING
# ==========================================
with tab4:
    st.subheader("Executive Scenario & Sensitivity Simulator")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        cogs_inflation = st.slider("COGS / Cost Inflation Shock (%)", -10.0, 25.0, 5.0, 0.5)
    with s_col2:
        demand_shift = st.slider("Sales Volume Demand Shock (%)", -20.0, 20.0, 0.0, 1.0)

    simulated_actual_spend = total_actual * (1 + (cogs_inflation / 100))
    simulated_revenue = rev_actual * (1 + (demand_shift / 100))
    simulated_ebitda = simulated_revenue - simulated_actual_spend

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Simulated Revenue", f"${simulated_revenue:,.2f}", delta=f"{demand_shift}%")
    sc2.metric("Simulated Expense", f"${simulated_actual_spend:,.2f}", delta=f"{cogs_inflation}%",
               delta_color="inverse")
    sc3.metric("Gross Margin / EBITDA", f"${simulated_ebitda:,.2f}")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
    <div class="executive-footer">
        <p>Enterprise FP&A Variance Engine • Institutional Financial Modeling Portfolio Project</p>
    </div>
""", unsafe_allow_html=True)
