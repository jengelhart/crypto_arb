from kucoin.client import Client

# Creates client object with api-keys
client = Client('key1', 'key2')

# Welcome Message
print 'Bot is running'

def wait_until_filled(symbol):
	try:
		while len(client.get_active_orders(symbol)['SELL'] > 0 and client.get_active_orders(symbol)['BUY']) > 0:
			print 'Waiting for order to fill...'
		print 'Filled'
	except:
		wait_until_filled(symbol)

# Dumb loop to keep running
while True:
	# Pull order book data
	print 'Pulling data...'
	try:	
		eth_btc_orders = client.get_order_book('ETH-BTC', limit=1)
		rpx_eth_orders = client.get_order_book('RPX-ETH', limit=1)
		rpx_btc_orders = client.get_order_book('RPX-BTC', limit=1)
	except:
		eth_btc_orders = client.get_order_book('ETH-BTC', limit=1)
		rpx_eth_orders = client.get_order_book('RPX-ETH', limit=1)
		rpx_btc_orders = client.get_order_book('RPX-BTC', limit=1)
	
	eth_btc_bid = eth_btc_orders['BUY'][0][0]
	eth_btc_ask = eth_btc_orders['SELL'][0][0]
	
	rpx_eth_bid = rpx_eth_orders['BUY'][0][0]
	rpx_eth_ask = rpx_eth_orders['SELL'][0][0]
	
	rpx_btc_bid = rpx_btc_orders['BUY'][0][0]
	rpx_btc_ask = rpx_btc_orders['SELL'][0][0]
	
	# If RPX is cheaper in ETH
	if rpx_btc_bid / (rpx_eth_ask * eth_btc_ask) > 1.003:
		print 'Trade started...'
		rpx_amount = .005 / rpx_eth_ask
		print 'Buying RPX...'
		client.create_buy_order('RPX-ETH', rpx_eth_ask, rpx_amount)
		wait_until_filled('RPX-ETH')
		print 'Selling RPX...'
		client.create_sell_order('RPX-BTC', rpx_btc_bid, rpx_amount)
		wait_until_filled('RPX-BTC')
		print 'Buying ETH...'
		client.create_buy_order('ETH-BTC', eth_btc_ask, rpx_amount * rpx_btc_bid / eth_btc_ask)
		wait_until_filled('ETH-BTC')
		
	# IF RPX is cheaper in BTC
	elif (rpx_eth_bid * eth_btc_bid) / rpx_btc_ask > 1.003:
		print 'Trade started...'
		print 'Selling ETH...'
		client.create_sell_order('ETH-BTC', eth_btc_bid, 0.005)
		wait_until_filled('ETH-BTC')
		print 'Buying RPX...'
		btc_balance = client.get_coin_balance('BTC')['balance']
		client.create_buy_order('RPX-BTC', rpx_btc_ask, btc_balance / rpx_btc_ask)
		wait_until_filled('RPX-BTC')
		print 'Selling RPX...'
		rpx_balance = client.get_coin_balance('RPX')['balance']
		client.create_sell_order('RPX-ETH', rpx_eth_bid, rpx_balance)
		wait_until_filled('RPX-ETH')
		
	else:
		print 'Waiting for arb opportunity...'
		

