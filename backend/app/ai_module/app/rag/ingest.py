"""
Knowledge Ingestion Script

Run this ONCE to populate the vector database with investment knowledge.
After running, the RAG system can retrieve this knowledge during advice generation.

Usage:
  python -m app.ai_module.app.rag.ingest
"""

from app.ai_module.app.rag.rag_store import add_documents


# Our investment knowledge base — these are the "documents" stored in the vector DB
# In a real system you'd load these from PDFs, websites, or databases
INVESTMENT_KNOWLEDGE = [
    """
    Modern Portfolio Theory (MPT) — Harry Markowitz
    MPT says you can maximize returns for a given level of risk by diversifying across 
    assets that don't move together (low correlation). The key insight: a portfolio's 
    risk is less than the weighted average of individual asset risks when assets are 
    not perfectly correlated. This is why mixing stocks, bonds, and international 
    assets reduces overall risk without sacrificing all returns.
    """,

    """
    Asset Allocation by Age — The 110 Rule
    A simple rule: subtract your age from 110 to get your stock percentage.
    Age 30 → 80% stocks, 20% bonds.
    Age 50 → 60% stocks, 40% bonds.
    Age 65 → 45% stocks, 55% bonds.
    This rule accounts for the fact that younger investors have more time to recover 
    from market downturns. Older investors need capital preservation over growth.
    """,

    """
    Dollar-Cost Averaging (DCA)
    Instead of investing a lump sum, invest the same fixed amount regularly 
    (e.g., $500/month). This automatically buys more shares when prices are low 
    and fewer when prices are high. Over time, this averages out the cost per share.
    DCA reduces emotional decision-making and is especially effective in volatile markets.
    Perfect strategy for salaried employees with regular income.
    """,

    """
    Emergency Fund First
    Before any investment, always maintain 3-6 months of living expenses in a 
    liquid savings account. This prevents you from being forced to sell investments 
    at a loss during emergencies. Emergency funds should be in high-yield savings 
    accounts or money market funds — not stocks or crypto.
    """,

    """
    Index Funds vs Active Management
    Studies consistently show that 80-90% of actively managed funds underperform 
    their benchmark index over 10+ years, after fees. Low-cost index funds (like 
    Vanguard S&P 500 ETF, VTI) offer broad market exposure with very low expense 
    ratios (0.03-0.10%). For most retail investors, index funds are the optimal 
    long-term strategy. "Don't look for a needle in a haystack. Just buy the haystack."
    """,

    """
    Cryptocurrency Risk Profile
    Cryptocurrencies like Bitcoin and Ethereum are highly speculative assets with:
    - Extreme volatility (can drop 80%+ in bear markets)
    - No underlying cash flows or dividends
    - Regulatory uncertainty
    - 24/7 trading that amplifies emotional decisions
    Recommended allocation: 0-5% for conservative investors, 5-15% for aggressive.
    Never invest more in crypto than you can afford to lose entirely.
    """,

    """
    Bond Basics for Defensive Investing
    Bonds are loans you make to governments or corporations. They pay regular interest 
    (coupon) and return principal at maturity. Key concepts:
    - When interest rates rise, bond prices fall (inverse relationship)
    - Government bonds (Treasuries) are safest but lowest yield
    - Corporate bonds pay more but carry default risk
    - Bond funds (BND, AGG) provide easy diversification
    Bonds serve as a shock absorber in a portfolio — when stocks crash, bonds often rise.
    """,

    """
    Compound Interest — The 8th Wonder of the World
    $10,000 invested at 8% annually:
    - After 10 years: $21,589
    - After 20 years: $46,610
    - After 30 years: $100,627
    The key is time. Starting at 25 vs 35 can double your final wealth.
    Reinvesting dividends dramatically accelerates compounding.
    Even small regular contributions transform into large sums over decades.
    """,

    """
    Tax-Advantaged Accounts (USA)
    401(k): Employer-sponsored retirement account. Contributions are pre-tax (reduces 
    taxable income now). Max contribution 2024: $23,000/year. Always contribute enough 
    to get full employer match — this is FREE money.
    Roth IRA: Contributions are post-tax but ALL growth is TAX FREE. Max: $7,000/year.
    Best for younger investors in lower tax brackets.
    HSA: Health Savings Account — triple tax advantage. Great for medical + retirement.
    """,

    """
    Rebalancing Strategy
    Over time, winning assets grow larger than intended, increasing portfolio risk.
    Rebalancing means selling some winners and buying laggards to restore target allocation.
    - Annual or threshold-based (rebalance when any asset drifts >5% from target)
    - Reduces risk of being overexposed to any single asset class
    - Enforces "buy low, sell high" discipline automatically
    - Can be done tax-efficiently by directing new contributions to underweight assets
    """,
]


def run_ingestion():
    """Main function to load all knowledge into the vector store."""
    print("Starting knowledge ingestion...")
    add_documents(INVESTMENT_KNOWLEDGE)
    print("Knowledge ingestion complete! Vector store is ready.")


if __name__ == "__main__":
    run_ingestion()
