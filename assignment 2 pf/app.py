import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 🎯 Title of the App
st.title("Loan Calculator 💳")

# 🔢 User Inputs
loan_amount = st.number_input("Loan Amount ($)", min_value=1000, step=500, value=10000)
interest_rate = st.slider("Annual Interest Rate (%)", 1.0, 20.0, 5.0, step=0.1)
loan_term = st.slider("Loan Term (Years)", 1, 30, 10)

# 🏦 EMI Calculation
monthly_rate = (interest_rate / 100) / 12
num_payments = loan_term * 12

# Avoid division by zero error
if monthly_rate > 0:
    emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
else:
    emi = loan_amount / num_payments  # If interest rate is zero

st.subheader(f"📌 Monthly EMI: **${emi:.2f}**")

# 📊 Loan Balance Over Time
months = np.arange(1, num_payments + 1)
balance = loan_amount * ((1 + monthly_rate) ** months - 1) / ((1 + monthly_rate) ** num_payments - 1)

fig, ax = plt.subplots()
ax.plot(months, balance, label="Remaining Loan Balance", color='blue')
ax.set_xlabel("Months")
ax.set_ylabel("Remaining Balance ($)")
ax.legend()
ax.grid()
st.pyplot(fig)

