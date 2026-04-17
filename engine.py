def monthly_payment(balance, annual_rate, months):
    r = annual_rate / 12
    if r == 0:
        return balance / months
    return balance * (r * (1 + r) ** months) / ((1 + r) ** months - 1)


def simulate(balance, rate, months, extra_monthly=0, extra_yearly=0):
    r = rate / 12
    total_interest = 0

    for m in range(1, months + 1):
        if balance <= 0:
            break

        extra = extra_monthly + (extra_yearly if m % 12 == 0 else 0)

        balance -= extra

        remaining = months - m + 1
        payment = monthly_payment(balance, rate, remaining)

        interest = balance * r
        principal = payment - interest

        if principal > balance:
            principal = balance

        balance -= principal
        total_interest += interest

    return total_interest, m
