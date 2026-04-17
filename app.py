import streamlit as st
import matplotlib.pyplot as plt

# --- Functions ---
def monthly_payment(balance, annual_rate, months):
    r = annual_rate / 12
    if r == 0:
        return balance / months
    return balance * (r * (1 + r) ** months) / ((1 + r) ** months - 1)


def simulate(balance, rate, months, extra_monthly=0, extra_yearly=0):
    r = rate / 12
    total_interest = 0

    balances = []
    interests = []

    for m in range(1, months + 1):
        if balance <= 0:
            break

        extra = extra_monthly
        if m % 12 == 0:
            extra += extra_yearly

        balance -= extra

        remaining = months - m + 1
        payment = monthly_payment(balance, rate, remaining)

        interest = balance * r
        principal = payment - interest

        if principal > balance:
            principal = balance

        balance -= principal
        total_interest += interest

        balances.append(balance)
        interests.append(total_interest)

    return balances, interests, total_interest, m


def find_best_strategy(balance, rate, months, target_interest):
    best = None

    for monthly in range(0, 801, 50):
        for yearly in range(0, 5001, 500):

            _, _, total_int, duration = simulate(
                balance, rate, months, monthly, yearly
            )

            deviation = abs(total_int - target_interest)

            if not best or deviation < best["deviation"]:
                best = {
                    "monthly_extra": monthly,
                    "yearly_extra": yearly,
                    "interest": int(total_int),
                    "duration": duration,
                    "deviation": deviation
                }

    return best


# --- UI ---
st.set_page_config(page_title="Loan Optimizer", layout="wide")

st.title("🏦 Loan Optimization Platform")

# Inputs
col1, col2, col3 = st.columns(3)

balance = col1.number_input("Loan Balance (€)", value=94000)
rate = col2.number_input("Interest Rate (%)", value=4.42) / 100
months = col3.number_input("Remaining Months", value=242)

target_interest = st.number_input("🎯 Target Interest (€)", value=23000)

st.markdown("---")

colA, colB = st.columns(2)
extra_monthly = colA.slider("Monthly Extra (€)", 0, 1000, 300)
extra_yearly = colB.slider("Yearly Bonus (€)", 0, 5000, 2000)

# Simulation
balances, interests, total_interest, duration = simulate(
    balance, rate, months, extra_monthly, extra_yearly
)

# Results
st.markdown("## 📊 Results")

c1, c2, c3 = st.columns(3)
c1.metric("💰 Interest", f"{total_interest:,.0f} €")
c2.metric("⏱️ Months", duration)
c3.metric("📅 Years", f"{duration/12:.1f}")

# Alerts
if total_interest < target_interest:
    st.success("🔥 Below target")
elif total_interest < target_interest * 1.1:
    st.warning("⚠️ Near target")
else:
    st.error("❌ Too much interest")

# Charts
st.markdown("## 📈 Charts")

fig, ax = plt.subplots()
ax.plot(balances)
ax.set_title("Remaining Balance")
st.pyplot(fig)

fig2, ax2 = plt.subplots()
ax2.plot(interests)
ax2.set_title("Cumulative Interest")
st.pyplot(fig2)

# Optimizer
st.markdown("## 🤖 Auto Optimizer")

if st.button("Find Best Strategy"):
    best = find_best_strategy(balance, rate, months, target_interest)

    st.success("Best Strategy Found")

    st.write(f"💰 Monthly Extra: {best['monthly_extra']} €")
    st.write(f"🎁 Yearly Bonus: {best['yearly_extra']} €")
    st.write(f"📊 Interest: {best['interest']} €")
    st.write(f"⏱️ Duration: {best['duration']} months")
