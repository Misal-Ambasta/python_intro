# Base Classes

class TradingAccount:
    def __init__(self, account_id, balance=0.0):
        self.account_id = account_id
        self.balance = balance
        self.portfolio = {}  # {symbol: quantity}

    def deposit(self, amount):
        self.balance += amount
        print(f"[Account] Deposited ${amount}. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds.")
        self.balance -= amount
        print(f"[Account] Withdrawn ${amount}. New balance: ${self.balance:.2f}")

    def update_portfolio(self, symbol, qty):
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + qty
        print(f"[Account] Updated portfolio: {symbol} => {self.portfolio[symbol]} units")

    def get_portfolio_value(self, prices):
        return sum(qty * prices.get(sym, 0) for sym, qty in self.portfolio.items())


class RiskManagement:
    def assess_risk(self, symbol, quantity, price):
        exposure = quantity * price
        print(f"[Risk] Exposure for {symbol}: ${exposure:.2f}")
        return exposure <= 10000  # basic threshold

    def calculate_var(self, returns):
        if not returns:
            return 0
        var = min(returns) * 1.65  # 5% VaR
        print(f"[Risk] Calculated VaR: {var:.2f}")
        return var


class AnalyticsEngine:
    def analyze_market(self, symbol, data):
        trend = "uptrend" if data[-1] > data[0] else "downtrend"
        print(f"[Analytics] {symbol} shows a {trend}")
        return trend

    def moving_average(self, data, window=3):
        if len(data) < window:
            return []
        ma = [sum(data[i:i+window]) / window for i in range(len(data)-window+1)]
        print(f"[Analytics] Moving average: {ma}")
        return ma


class NotificationSystem:
    def send_alert(self, message):
        print(f"[Alert] {message}")

    def log_transaction(self, symbol, qty, price):
        print(f"[Log] Trade executed: {qty} units of {symbol} at ${price}")



# Derived Trader Classes

class StockTrader(TradingAccount, RiskManagement, AnalyticsEngine):
    def __init__(self, account_id, balance=0.0):
        TradingAccount.__init__(self, account_id, balance)

    def trade_stock(self, symbol, qty, price):
        if self.assess_risk(symbol, qty, price):
            cost = qty * price
            if cost > self.balance:
                print("[StockTrader] Trade failed: insufficient balance.")
                return
            self.withdraw(cost)
            self.update_portfolio(symbol, qty)
            print(f"[StockTrader] Bought {qty} shares of {symbol} at ${price}")
        else:
            print("[StockTrader] Trade rejected due to high risk.")


class CryptoTrader(TradingAccount, RiskManagement, NotificationSystem):
    def __init__(self, account_id, balance=0.0):
        TradingAccount.__init__(self, account_id, balance)

    def trade_crypto(self, symbol, qty, price):
        if self.assess_risk(symbol, qty, price):
            cost = qty * price
            if cost > self.balance:
                self.send_alert("Trade failed: insufficient balance.")
                return
            self.withdraw(cost)
            self.update_portfolio(symbol, qty)
            self.log_transaction(symbol, qty, price)
            self.send_alert(f"Bought {qty} {symbol} at ${price}")
        else:
            self.send_alert("Trade rejected due to high risk.")



# ProfessionalTrader (Multiple Inheritance)

class ProfessionalTrader(StockTrader, CryptoTrader):
    def __init__(self, account_id, balance=0.0):
        # Explicitly call base class constructor once to avoid duplication
        TradingAccount.__init__(self, account_id, balance)

    def full_portfolio_report(self, prices):
        total = self.get_portfolio_value(prices)
        print(f"[Report] Portfolio value: ${total:.2f}")
        print(f"[Report] Holdings: {self.portfolio}")
        return total

    # Resolves conflict between NotificationSystem and AnalyticsEngine if needed
    def notify(self, message):
        if hasattr(self, 'send_alert'):
            self.send_alert(message)
        else:
            print(f"[Notify] {message}")
