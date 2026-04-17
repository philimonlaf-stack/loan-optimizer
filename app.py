import streamlit as st
import matplotlib.pyplot as plt

from engine import simulate
from optimizer import optimize

st.set_page_config(page_title="Loan AI Optimizer", layout="wide")

st.title("🏦 Loan AI Optimization Platform")

# Inputs
col1, col2, col3 = st.columns(3)

balance = col1.number_input("Loan Balance (€)", value=94000)
rate = col2.number_input("Interest Rate (%)", value=4.42) / 100
months = col3.number_input("Remaining Months", value=242)

target = st.number_input("🎯 Target Interest (€)", value=23000)

st.divider()

# Strategy controls
extra_monthly = st.slider("Monthly Extra", 0, 1000, 300)
extra_yearly = st.slider("Yearly Bonus", 0, 10000, 2000)

# Simulation
interest, duration = simulate(balance, rate, months, extra_monthly, extra_yearly)

# Metrics
c1, c2 = st.columns(2)

c1.metric("💰 Total Interest", f"{interest:,.0f} €")
c2.metric("⏱️ Duration", f"{duration} months")

# AI Advisor
st.subheader("🧠 AI Advisor")

gap = interest - target

if gap < 0:
    st.success("🔥 You are below target — optimize less aggressively")
elif gap < 2000:
    st.warning("⚠️ Slight deviation — small adjustment needed")
else:
    st.error("🔴 High deviation — increase prepayments")

# Optimization
st.subheader("🤖 True Optimization AI")

if st.button("Run Optimization Engine"):

    best = optimize(balance, rate, months, target)

    st.success("Best Strategy Found")

    st.write(f"💰 Monthly Extra: {best['monthly_extra']} €")
    st.write(f"🎁 Yearly Extra: {best['yearly_extra']} €")
    st.write(f"📊 Interest: {best['interest']:,.0f} €")
    st.write(f"⏱️ Duration: {best['duration']} months")

# Chart
st.subheader("📈 Balance Simulation")

_, _ = simulate(balance, rate, months, extra_monthly, extra_yearly)
