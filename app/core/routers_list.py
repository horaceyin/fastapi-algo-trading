from routers.authentication.login import loginRouter
from routers.dashboard.backtesting import backtestingRouter
from routers.dashboard.technical_analysis import taRouter
from routers.dashboard.live_trading import live_trading_router

# defines all routers here
ROUTERS_LIST = [
    loginRouter,
    backtestingRouter,
    taRouter,
    live_trading_router
]