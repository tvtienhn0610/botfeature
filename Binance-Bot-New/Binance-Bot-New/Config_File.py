##fill in your API keys here to be accessed by other scripts
API_KEY = 'lmRl0bcG4my9tvoNDdgUCEuFKASmzwEPSUnvl4GIm3OUdNpdloQtGiTZcYioDen8'
API_SECRET = 'DgRJaDCnJvx5FJbx1qXbiduBbcLqtXxxjtxl360gC7RJnErlzQ5FnIC6hWa5Ydh3'

################## settings, these are very strategy dependant ensure you have enough data for your chosen strategy ##################################
order_Size = .02
leverage = 10
start_string = '4 hour ago' ## Buffer of candle sticks be careful if you don't provide enough the bot will throw an error
Interval = '1m' ##candle sticks you want to trade
Max_Number_Of_Trades = 1  ## How many positions we can have open at once
use_heikin_ashi = 0 ## Create heikin ashi candles that can be referenced in Bot_Class.Bot.make_decision()
use_trailing_stop = 0 ##If on we will use our TP value as the Activation price for a trailing stop loss
trailing_stop_callback = 0.1 ##trailing stop percent, this is .1% range is [.1% - 5%] .ie [0.1 - 5]
##################################################################################
###################### Coins Traded ##############################################
##Trade All Coins if True, can also specify a list of coins to trade instead. Example: symbol = ['ETHUSDT','BTCUSDT'] & set Trade_All_Coins = False
Trade_All_Coins = True
symbols = ['BTCUSDT','ETHUSDT','XRPUSDT','MATICUSDT','DENTUSDT','SOLUSDT','AVAXUSDT','DOGEUSDT','BNBUSDT','AXSUSDT','TLMUSDT','DGBUSDT','CELOUSDT','ADAUSDT','LINKUSDT','NEOUSDT']  ## If Trade_All_Coins is False then we list the coins we want to trade here, otherwise the bot will automatically get all coins and trade them

# symbols = ['BTCUSDT'] 
## If you are getting a rate limit error on startup this will add a delay for downloading candlesticks to start
RATE_LIMIT_WAIT = False ## It will not slow down the bot, it will only slow down the startup by about (4 x (number of coins you're trading)) seconds

token_telegram = "2095464082:AAHw8loNeTSCtaoXgwBtpZdDz7vzIJW6MbY"
chatId_telegram = "1221651999"