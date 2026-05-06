"""
engines/simulation_engine.py
-----------------------------
Simulation Engine

Uses the compound interest formula: A = P(1 + r)^t
to project how an investment grows over time.

Also supports monthly contributions:
  A = P(1+r)^t + C * [((1+r)^t - 1) / r]
  where C = monthly contribution
"""

from app.ai_module.app.schemas import UserProfile, SimulationResult


def simulate_growth(
    profile: UserProfile,
    expected_annual_return: float,
    monthly_contribution: float = 0.0,
) -> SimulationResult:
    """
    Simulates portfolio growth year by year.
    
    Args:
        profile: user's financial details (savings, time horizon, goal)
        expected_annual_return: percentage like 8.5 (not 0.085)
        monthly_contribution: extra money added each month
    
    Returns:
        SimulationResult with year-by-year values
    """
    r = expected_annual_return / 100      # convert % to decimal
    principal = profile.savings
    years_list = list(range(0, profile.time_horizon + 1))
    values = []

    for t in years_list:
        if t == 0:
            values.append(round(principal, 2))
            continue

        # Compound growth on initial principal
        growth = principal * ((1 + r) ** t)

        # Add future value of monthly contributions (annuity formula)
        if monthly_contribution > 0 and r > 0:
            monthly_r = r / 12          # monthly rate
            months = t * 12
            contribution_growth = monthly_contribution * (((1 + monthly_r) ** months - 1) / monthly_r)
            growth += contribution_growth

        values.append(round(growth, 2))

    final_value = values[-1]
    total_invested = principal + (monthly_contribution * 12 * profile.time_horizon)
    total_gain = final_value - total_invested

    # How far along are they toward their goal?
    # We estimate goal amount as 20x annual income (rough retirement target)
    goal_target = profile.income * 20
    goal_progress = min(100.0, (final_value / goal_target) * 100)

    return SimulationResult(
        years=years_list,
        portfolio_values=values,
        final_value=round(final_value, 2),
        total_invested=round(total_invested, 2),
        total_gain=round(total_gain, 2),
        goal_progress_percent=round(goal_progress, 1),
    )


def compare_strategies(
    profile: UserProfile,
    aggressive_return: float = 12.0,
    conservative_return: float = 5.0,
) -> dict:
    """
    Compares two strategies side by side.
    Great for the "Your Plan vs Conservative Plan" feature.
    
    Returns dict with both simulations for the frontend to display.
    """
    aggressive = simulate_growth(profile, aggressive_return)
    conservative = simulate_growth(profile, conservative_return)

    return {
        "aggressive": {
            "label": "Your Current Plan",
            "return_rate": aggressive_return,
            "final_value": aggressive.final_value,
            "total_gain": aggressive.total_gain,
            "years": aggressive.years,
            "values": aggressive.portfolio_values,
        },
        "conservative": {
            "label": "Conservative Plan",
            "return_rate": conservative_return,
            "final_value": conservative.final_value,
            "total_gain": conservative.total_gain,
            "years": conservative.years,
            "values": conservative.portfolio_values,
        },
        "difference": round(aggressive.final_value - conservative.final_value, 2),
    }
