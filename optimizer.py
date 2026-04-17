import numpy as np
from engine import simulate

def optimize(balance, rate, months, target_interest):
    best = None

    monthly_range = range(0, 1001, 50)
    yearly_range = range(0, 10001, 500)

    for m_extra in monthly_range:
        for y_extra in yearly_range:

            interest, duration = simulate(
                balance, rate, months,
                m_extra,
                y_extra
            )

            score = abs(interest - target_interest)

            if best is None or score < best["score"]:
                best = {
                    "monthly_extra": m_extra,
                    "yearly_extra": y_extra,
                    "interest": interest,
                    "duration": duration,
                    "score": score
                }

    return best
