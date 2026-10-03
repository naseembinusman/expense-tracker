
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💸",
    layout="wide"
)

# 2. Initialize Session State for Data Storage
if "expenses" not in st.session_state:
    # Starting with initial logged expenses
    st.session_state.expenses = pd.DataFrame([
        {"Date": "2026-10-01", "Item": "Breakfast", "Category": "Dining & Cafes", "Payment": "Tabby Card", "Amount": 9.00},
        {"Date": "2026-10-01", "Item": "Snack", "Category": "Dining & Cafes", "Payment": "Tabby Card", "Amount": 2.25}
    ])

st.title("💸 Expense Tracker & Budget Log")

# 3. Sidebar Configuration
st.sidebar.header("⚙️ Settings")
currency = st.sidebar.selectbox("Select Currency", ["AED", "USD", "EUR", "GBP", "INR"])
budget_target = st.sidebar.number_input("Monthly Target Budget", value=3000, step=100)

# 4. Main Navigation Tabs
tab_log, tab_dash = st.tabs(["📝 Log Expense", "📊 Dashboard & Analytics"])

# TAB 1: LOG EXPENSE FORM
with tab_log:
    st.subheader("Add a New Transaction")
    
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount ({})".format(currency), min_value=0.01, step=1.0, format="%.2f")
            item = st.text_input("Description / Item", placeholder="e.g. Coffee, Groceries")
            exp_date = st.date_input("Date", datetime.now())
            
        with col2:
            category = st.selectbox(
                "Category", 
                ["Dining & Cafes", "Groceries", "Transport & Fuel", "Bills & Utilities", "Shopping & Lifestyle", "Entertainment", "Other"]
            )
            payment = st.selectbox(
                "Payment Method", 
                ["Tabby Card", "Credit Card", "Debit Card", "Cash", "Apple Pay / Wallet"]
            )
            
        submitted = st.form_submit_button("➕ Log Expense", use_container_width=True)
        
        if submitted:
            new_data = pd.DataFrame([{
                "Date": str(exp_date),
                "Item": item,
                "Category": category,
                "Payment": payment,
                "Amount": float(amount)
            }])
            # Append new entry to session state dataframe
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
            st.success(f"Logged {amount} {currency} for '{item}' successfully!")

# TAB 2: DASHBOARD & REPORTING
with tab_dash:
    df = st.session_state.expenses
    
    if df.empty:
        st.info("No expenses logged yet.")
    else:
        # Calculate Key Metrics
        total_spent = df["Amount"].sum()
        total_count = len(df)
        tabby_total = df[df["Payment"] == "Tabby Card"]["Amount"].sum()
        
        # Display Summary Cards (st.metric)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Spent", f"{total_spent:.2f} {currency}", f"{(total_spent/budget_target)*100:.1f}% of Budget")
        m2.metric("Total Transactions", total_count)
        m3.metric("Tabby Card Spend", f"{tabby_total:.2f} {currency}")
        
        top_cat = df.groupby("Category")["Amount"].sum().idxmax() if not df.empty else "N/A"
        m4.metric("Top Spending Category", top_cat)
        
        st.divider()
        
        # Interactive Visual Charts (Plotly)
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Category Breakdown")
            cat_df = df.groupby("Category")["Amount"].sum().reset_index()
            fig_pie = px.pie(cat_df, values="Amount", names="Category", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.subheader("Payment Method Totals")
            pay_df = df.groupby("Payment")["Amount"].sum().reset_index()
            fig_bar = px.bar(pay_df, x="Payment", y="Amount", color="Payment", text_auto=".2f")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.divider()
        
        # Interactive Data Table
        st.subheader("Transaction Log")
        st.dataframe(df, use_container_width=True)
        
        # CSV Download Option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="expense_report.csv",
            mime="text/csv"
        )
          