"""
AI Financial Assistant Module for AI-Expense-Sales-Analyzer.
Integrates Gemini / OpenAI API or fallback intelligent rule-based engine to answer financial questions.
"""

import os
import sys

# Add parent dir to sys path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.data_loader import load_processed_data
from python.eda import generate_eda_summary
from ai.prompts import FINANCIAL_ANALYST_SYSTEM_PROMPT, USER_QUERY_TEMPLATE


class FinancialAIAssistant:
    def __init__(self, api_key=None, provider='gemini'):
        """
        Initializes AI Assistant with API key or detects env variables.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.provider = provider
        self.df = load_processed_data()
        self.stats = generate_eda_summary(self.df)

    def ask(self, query):
        """
        Answers a financial question about sales, expenses, or profit.
        Uses API model if configured, otherwise falls back to statistical NLP engine.
        """
        query_lower = query.lower()
        context_str = self._format_context()

        # If API key is available, try invoking Google GenAI API or OpenAI API
        if self.api_key:
            try:
                if self.provider == 'gemini':
                    from google import genai
                    client = genai.Client(api_key=self.api_key)
                    prompt = f"{FINANCIAL_ANALYST_SYSTEM_PROMPT}\n\n{USER_QUERY_TEMPLATE.format(context_data=context_str, user_query=query)}"
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    return response.text
            except Exception as e:
                print(f"[!] API call failed ({e}). Falling back to offline AI engine.")

        # Offline Intelligent Fallback Engine
        return self._offline_response(query_lower)

    def _format_context(self):
        """Formats high-level metrics for LLM context."""
        return (
            f"Total Revenue: ${self.stats['total_revenue']:,.2f} | "
            f"Total Expenses: ${self.stats['total_expense']:,.2f} | "
            f"Net Profit: ${self.stats['total_net_profit']:,.2f} ({self.stats['overall_profit_margin_pct']}% margin) | "
            f"Transactions: {self.stats['total_transactions']}"
        )

    def _offline_response(self, query):
        """Generates dynamic analytical response based on dataset statistics."""
        rev = self.stats['total_revenue']
        exp = self.stats['total_expense']
        profit = self.stats['total_net_profit']
        margin = self.stats['overall_profit_margin_pct']

        if 'revenue' in query or 'sales' in query or 'income' in query:
            top_cat = self.stats['category_summary'][0]
            return (
                f"### 📊 Revenue & Sales Performance Analysis\n"
                f"- **Total Revenue Generated:** `${rev:,.2f}` across **{self.stats['total_transactions']:,}** completed transactions.\n"
                f"- **Average Transaction Value:** `${self.stats['avg_order_value']:,.2f}`.\n"
                f"- **Top Revenue Category:** **{top_cat['Product_Category']}** generating `${top_cat['Revenue']:,.2f}` "
                f"({(top_cat['Revenue']/rev*100):.1f}% of total sales).\n"
                f"- **Top Geographical Region:** **{self.stats['region_summary'][0]['Region']}** region with `${self.stats['region_summary'][0]['Revenue']:,.2f}` revenue."
            )
        elif 'expense' in query or 'cost' in query or 'spending' in query:
            cogs = self.stats['total_cogs']
            mkt = self.stats['total_marketing']
            ship = self.stats['total_shipping']
            ops = self.stats['total_operating']
            return (
                f"### 💡 Cost & Expense Structure Analysis\n"
                f"- **Total Operating & Direct Expenses:** `${exp:,.2f}` (Expense Ratio: `{(exp/rev*100):.2f}%` of revenue).\n"
                f"- **Cost Breakdown:**\n"
                f"  - **COGS (Cost of Goods Sold):** `${cogs:,.2f}` ({(cogs/exp*100):.1f}% of total costs)\n"
                f"  - **Marketing Expense:** `${mkt:,.2f}` ({(mkt/exp*100):.1f}% of total costs)\n"
                f"  - **Operating Overhead:** `${ops:,.2f}` ({(ops/exp*100):.1f}% of total costs)\n"
                f"  - **Logistics & Shipping:** `${ship:,.2f}` ({(ship/exp*100):.1f}% of total costs)\n"
                f"- **Cost Optimization Tip:** Re-evaluate high COGS categories and optimize logistics routes to lower shipping costs."
            )
        elif 'profit' in query or 'margin' in query or 'net' in query:
            top_margin_cat = max(self.stats['category_summary'], key=lambda x: x['Profit_Margin_Pct'])
            return (
                f"### 📈 Profitability & Margin Overview\n"
                f"- **Total Net Profit:** `${profit:,.2f}`.\n"
                f"- **Overall Net Profit Margin:** `{margin}%`.\n"
                f"- **Highest Profit Margin Category:** **{top_margin_cat['Product_Category']}** with an impressive **{top_margin_cat['Profit_Margin_Pct']}%** profit margin.\n"
                f"- **Profit Growth Recommendation:** Scale high-margin product lines while reducing marketing spend on low-margin commodities."
            )
        elif 'recommend' in query or 'advise' in query or 'strategy' in query:
            return (
                f"### 🎯 Strategic Business Recommendations\n"
                f"1. **Optimize High-Expense Product Categories:** Audit vendor supplier costs for categories with cost ratios over 65%.\n"
                f"2. **Capitalize on High-Margin Segments:** Increase marketing budget for **Enterprise** and **Services** segments.\n"
                f"3. **Geographical Expansion:** Replicate sales playbooks from top region (**{self.stats['region_summary'][0]['Region']}**) into underperforming regions.\n"
                f"4. **Control Logistics Overhead:** Negotiate bulk shipping rates with freight carriers."
            )
        else:
            return (
                f"### 🤖 AI Financial Analysis Summary\n"
                f"- **Total Revenue:** `${rev:,.2f}`\n"
                f"- **Total Expenses:** `${exp:,.2f}`\n"
                f"- **Net Profit:** `${profit:,.2f}` (`{margin}%` Net Margin)\n"
                f"- **Total Volume:** `{self.stats['total_transactions']:,}` transactions processed.\n\n"
                f"*Feel free to ask detailed questions about sales trends, expense breakdowns, regional performance, or profit optimization strategies!*"
            )


if __name__ == '__main__':
    assistant = FinancialAIAssistant()
    print(assistant.ask("What is our overall revenue performance?"))
    print("\n" + "="*50 + "\n")
    print(assistant.ask("How are expenses distributed?"))
