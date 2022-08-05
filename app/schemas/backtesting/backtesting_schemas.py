from typing import List, Optional
from pydantic import BaseModel, validator, StrictInt
from schemas.backtesting.bar_summary_schemas import BarSummary
from schemas.backtesting.product_schemas import Product

class BacktestingModel(BaseModel):
    prodCode: List[Product] # Collect list of product indicators here
    portfolioValue: float = 1000000 # avFund # Default value should be the user's portfolio size
    boundaryValue: Optional[float] = 0
    liveTrade: Optional[bool] = False
    days: Optional[StrictInt] = 2 # Consistent between products in list
    barSummary: BarSummary # Bar summarizes the trading activity during barSummary seconds # Consistent between products in list

    @validator('portfolioValue')
    def portfolio_check(cls, portfolio_val):
        if portfolio_val <= 0: 
            raise ValueError('Portfolio value should not be equal to or less than 0.')
        return portfolio_val

    @validator('boundaryValue')
    def boundary_check(cls, boundary, values):
        if 'portfolioValue' in values and boundary >= values.get('portfolioValue'):
            raise ValueError('Boundary value should not be equal to or greater than portfolio value.')
        elif boundary < 0:
            raise ValueError('Boundary value should not be less than 0.')
        return boundary

    @validator('days')
    def day_check(cls, day):
        if day < 0: raise ValueError('Days should be an integer and larger than 0.')
        return day
