import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Set Page Configuration
st.set_page_config(page_title="💳 Advanced Loan EMI Calculator", page_icon="💰", layout="wide")

# 🎨 Custom CSS for Styling
st.markdown("""
    <style>
        body { background-color: #f5f7fa; }
        h1 { color: #FF5733; text-align: center; }
        h2 { color: #4CAF50; }
        h3 { color: #FFC300; }
        .stButton>button { background-color: #FF5733; color: white; border-radius: 10px; }
        .stDataFrame { background-color: #1E1E1E !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 🎯 Function to calculate EMI
def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    tenure_months = tenure * 12
    if monthly_rate > 0:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    else:
        emi = principal / tenure_months
    return emi

# 🎯 Function to generate amortization schedule
def generate_amortization_schedule(principal, rate, tenure, emi, extra_payment):
    months, interest_paid, principal_paid = [], [], []
    remaining_balance, total_interest, month_count = principal, 0, 1

    while remaining_balance > 0:
        interest = (remaining_balance * (rate / (12 * 100)))
        principal_payment = min(emi - interest + extra_payment, remaining_balance)
        remaining_balance -= principal_payment
        total_interest += interest

        months.append(month_count)
        interest_paid.append(interest)
        principal_paid.append(principal_payment)
        month_count += 1

    schedule_df = pd.DataFrame({
        "Month": months,
        "EMI ($)": [emi + extra_payment] * len(months),
        "Principal Paid ($)": principal_paid,
        "Interest Paid ($)": interest_paid,
        "Remaining Balance ($)": np.maximum(remaining_balance, 0)
    })

    return schedule_df, total_interest, len(months)

# 🏦 **Main App Layout**
st.title("💳 Advanced Loan EMI Calculator")
st.write("### 📌 Calculate your EMI, compare loans, and plan better!")

# 🎯 Sidebar: Loan Details
st.sidebar.header("📌 Loan Details")
loan_amount = st.sidebar.slider("Loan Amount ($)", 1000, 100000, 50000, 500)
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", 0.1, 20.0, 5.0, 0.1)
loan_tenure = st.sidebar.slider("Loan Tenure (Years)", 1, 30, 10, 1)
extra_payment = st.sidebar.number_input("Extra Monthly Payment ($)", 0, 1000, 0, 50)

# 💡 **EMI Calculation**
emi = calculate_emi(loan_amount, interest_rate, loan_tenure)

# Generate Amortization Schedule
schedule_df, total_interest, actual_tenure = generate_amortization_schedule(
    loan_amount, interest_rate, loan_tenure, emi, extra_payment
)

# 🔢 **Total Cost Breakdown**
total_payment = total_interest + loan_amount

# 📌 **Display EMI and Loan Summary**
st.metric("📌 Monthly EMI", f"${emi:.2f}")
st.metric("💰 Total Interest", f"${total_interest:.2f}")
st.metric("🔄 Total Payment", f"${total_payment:.2f}")
st.metric("⏳ Loan Paid Off in", f"{actual_tenure} Months")

# 📊 **Interactive Loan Breakdown Chart**
st.write("### 📊 Loan Payment Breakdown")
fig = px.area(schedule_df, x="Month", y=["Principal Paid ($)", "Interest Paid ($)"], 
              labels={"value": "Amount ($)", "variable": "Payment Type"}, 
              title="Principal vs Interest Over Time", color_discrete_map={"Principal Paid ($)": "#2ECC71", "Interest Paid ($)": "#E74C3C"})
st.plotly_chart(fig, use_container_width=True)

# 📊 **Pie Chart: Principal vs Interest**
fig_pie = go.Figure(data=[go.Pie(labels=["Principal", "Interest"], values=[loan_amount, total_interest], hole=0.3)])
fig_pie.update_layout(title_text="Total Payment Breakdown")
st.plotly_chart(fig_pie)

# 📊 **Loan Comparison Feature**
st.write("### 📊 Compare Loan Scenarios")
loan_amount_2 = st.number_input("Enter Another Loan Amount ($)", min_value=1000, max_value=100000, value=50000, step=500)
interest_rate_2 = st.slider("Select Another Interest Rate (%)", 0.1, 20.0, 5.0, 0.1)
loan_tenure_2 = st.slider("Select Another Tenure (Years)", 1, 30, 10, 1)
emi_2 = calculate_emi(loan_amount_2, interest_rate_2, loan_tenure_2)

# 🔥 **Comparison Bar Chart**
fig_bar = px.bar(x=["First Loan", "Second Loan"], y=[emi, emi_2], text_auto=True, 
                 labels={"x": "Loan Scenarios", "y": "Monthly EMI ($)"}, title="Comparison of EMI for Different Loan Plans",
                 color=["#3498DB", "#E74C3C"], color_discrete_sequence=["#3498DB", "#E74C3C"])
st.plotly_chart(fig_bar)

# ✨ **Footer**
st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | Advanced Finance Automation | Instructor: Dr. Usama Arshad")
