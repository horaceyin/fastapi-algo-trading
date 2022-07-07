from routers.authentication.login import loginRouter
from routers.dashboard.backtesting import backtestingRouter
from routers.dashboard.technical_analysis import taRouter

# defines all routers here
ROUTERS_LIST = [
    loginRouter,
    backtestingRouter,
    taRouter
]