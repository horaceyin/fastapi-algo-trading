from fastapi import HTTPException, status
from schemas.backtesting_schemas import BacktestingMode


class BacktestingService:
    def __init__(self):
        pass

    @staticmethod
    def run_backtesting(request: BacktestingMode):
        print(request)
        # write backtesting code here