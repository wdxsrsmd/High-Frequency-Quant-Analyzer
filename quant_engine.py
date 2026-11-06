import numpy as np
import pandas as pd
from scipy import stats

class QuantAnalyzer:
    """
    A high-performance quantitative analysis engine for tick data.
    Demonstrates statistical modeling and risk management.
    """
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data = None

    def generate_mock_data(self, days=252):
        """Simulates high-frequency tick data for backtesting."""
        np.random.seed(42)
        # Simulate geometric brownian motion for stock prices
        returns = np.random.normal(loc=0.0005, scale=0.02, size=days)
        price = 100 * np.cumprod(1 + returns)
        
        self.data = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=days),
            'Price': price,
            'Returns': returns
        })
        print(f"[*] Generated {days} days of simulated data for {self.ticker}.")

    def calculate_risk_metrics(self):
        """Calculates Value-at-Risk (VaR) and Sharpe Ratio."""
        if self.data is None:
            raise ValueError("Data not initialized. Run generate_mock_data() first.")
            
        returns = self.data['Returns']
        
        # 1. Value at Risk (95% confidence level)
        var_95 = np.percentile(returns, 5)
        
        # 2. Sharpe Ratio (Assuming risk-free rate = 0 for simplicity)
        mean_return = returns.mean()
        std_dev = returns.std()
        sharpe_ratio = (mean_return / std_dev) * np.sqrt(252) # Annualized
        
        print("\n--- Risk Metrics ---")
        print(f"95% Daily VaR: {var_95:.4f} (Expected max loss)")
        print(f"Annualized Sharpe Ratio: {sharpe_ratio:.4f}")
        
        return var_95, sharpe_ratio

    def apply_mean_reversion_strategy(self):
        """Simple moving average strategy to find arbitrage signals."""
        self.data['SMA_10'] = self.data['Price'].rolling(window=10).mean()
        self.data['SMA_50'] = self.data['Price'].rolling(window=50).mean()
        
        # Generate signals
        self.data['Signal'] = 0
        self.data.loc[self.data['SMA_10'] > self.data['SMA_50'], 'Signal'] = 1 # Buy
        self.data.loc[self.data['SMA_10'] < self.data['SMA_50'], 'Signal'] = -1 # Sell
        
        print("\n--- Strategy Execution ---")
        print("Mean reversion signals generated successfully.")

if __name__ == "__main__":
    engine = QuantAnalyzer(ticker="AAPL")
    engine.generate_mock_data()
    engine.calculate_risk_metrics()
    engine.apply_mean_reversion_strategy()
