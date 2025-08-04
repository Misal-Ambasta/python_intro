# Q: 4 - Financial Trading System with Multiple Inheritance

## Problem Statement
Create a sophisticated trading platform with multiple inheritance for different trading capabilities.

## Base Classes:

### TradingAccount:
- Basic account management

### RiskManagement:
- Risk assessment methods

### AnalyticsEngine:
- Market analysis capabilities

### NotificationSystem:
- Alert and reporting functionality

## Derived Classes:

### StockTrader(TradingAccount, RiskManagement, AnalyticsEngine):
- Stock trading with risk management

### CryptoTrader(TradingAccount, RiskManagement, NotificationSystem):
- Cryptocurrency trading with alerts

### ProfessionalTrader(StockTrader, CryptoTrader):
- Full-featured trader with all capabilities

## Requirements:

- Implement method resolution order correctly
- Override methods appropriately in each class
- Handle conflicts in multiple inheritance
- Implement portfolio tracking and performance metrics