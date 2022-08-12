import pyalgotrade.logger
from schemas.live_trading_schemas import GetTickerPriceModel


logger = pyalgotrade.logger.getLogger("SpLiveTrade")

prod_code = GetTickerPriceModel.prodCode