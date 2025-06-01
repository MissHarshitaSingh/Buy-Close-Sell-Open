from AlgorithmImports import *


class Tradedow(QCAlgorithm):
    def Initialize(self):
        # set start and end date for backtest
        self.set_start_date(2002, 8, 5)
        self.set_end_date(2024, 8, 5)

        # initialize cash balance
        self.set_cash(1000000)
        
        # add an equity
        self.security = self.add_equity("SPY", Resolution.MINUTE)
        

        # use Interactive Brokers model for fees
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN)

        # benchmark against S&P 500
        self.set_benchmark("SPY")

        # initialize closingOrderSent variable to track whether the market onClose order has been sent
        self.closingOrderSent = False

        # schedule a function to run every day just after the market opens
        self.schedule.on(self.date_rules.every_day(self.security.Symbol), self.time_rules.after_market_open(self.security.Symbol, 1), self.SellOpen)


    def SellOpen(self):
        # if we are invested at the open, liquidate our holdings
        if self.portfolio.invested:
            self.liquidate()
            self.closingOrderSent = False


    def OnData(self, data):
        # send a market on close order if it's the last hour of the day, we are not invested, and we have not sent it yet
        if self.time.hour == 15 and not self.portfolio.invested and not self.closingOrderSent:
            # calculate quantity of shares needed to use 100% of our cash
            quantity = self.calculate_order_quantity(self.security.Symbol, 1)
            # send the market on close order
            self.market_on_close_order(self.security.Symbol, quantity)
            # reset the closingOrderSent variable for the next day
            self.closingOrderSent = True
