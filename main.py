from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, os
import discord
from discord.ext import commands

def check(card, amount, link, price):
	sent = False
	while True:
		os.system('cls')
		print('Waiting for better Offer...')
		print('Card: ' + str(card) + ' Amount: ' + str(amount) + ' Wanted_Price: ' + str(price))
		print()
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(options=chrome_options)
		driver.get(link)
		html_code = driver.page_source
		soup = BeautifulSoup(html_code, 'html.parser')
		best_seller = soup.find_all(class_='d-flex has-content-centered me-1')
		best_seller = [str(x)[:-11][73:].split('\"')[0] for x in best_seller][:10][0]
		best_price = soup.find_all(class_='color-primary small text-end text-nowrap fw-bold')[:20][0::2]
		best_price = [str(x)[:-7][63:] for x in best_price][0]
		print(best_price)
		print('Best Offer: ' + str(best_seller) + " " + str(best_price))
		driver.quit()
		if float(price) >= float(best_price[:-2].replace(',', '.')):
			print('There is a fitting offer!')
			print(best_seller.ljust(20, ' ') + str(best_price[1]))

			intents = discord.Intents.default()
			intents.typing = False
			intents.presences = False
			intents.messages = True 
			bot = commands.Bot(command_prefix="!", intents=intents)

			@bot.event
			async def on_ready():
				print(f"Bot is ready. Logged in as {bot.user.name} ({bot.user.id})")
				channel_id = 1129844765496725584
				channel = bot.get_channel(channel_id)
				if channel:
					user_mention = f'<@659833477478481950>'
					await channel.send(f"{user_mention}      {card}      Amount:      {amount}      {best_seller}       {best_price}")
					sent = True
					await bot.close()


			bot.run('ODUwNjMzNjI3ODUwMzc1MjA5.GMO_Kr.fuEIersPvAgy8z7yBBOfm')
			sent = True
		if sent:
			quit()
		for num in range(60):
			print('Waiting: ' + str(num), end='\r')
			time.sleep(1)


def search(card, how_many, max_price):
	chrome_options = Options()
	chrome_options.add_argument('--headless') 
	
	nums = '1234567890'
	for num in how_many:
		if num not in nums:
			how_many = '1'
			break
	driver = webdriver.Chrome(options=chrome_options)
	
	
	driver.get('https://www.cardmarket.com/de/YuGiOh/Products/Search?searchString=' + card) 
	
	
	
	html_code = driver.page_source
	
	soup = BeautifulSoup(html_code, 'html.parser')
	if 'Keine Ergebnisse für Ihre Anfrage' in str(soup):
		print('No Cards Not Found')
		return
	
	versions = [x.replace(':', '') for x in str(soup.find_all(class_='col-icon small'))[147:].split('\"')[1::2][0::8]]
	names = [x[:-5] for x in str(soup.find_all(class_="d-block small text-muted fst-italic")).split('>')[1::2]]
	
	
	pairs = []

	for index, (version, name) in enumerate(zip(versions, names)):
		pairs.append([version, name])
		print(f'[{index+1}]  ' + version.ljust(45, ' ') + '  ' + name)

	driver.quit()

	chosen = int(input('>'))
	chosen_card = pairs[chosen-1][0]
	driver = webdriver.Chrome(options=chrome_options)
	
	new_link = 'https://www.cardmarket.com/de/YuGiOh/Products/Singles/' + pairs[chosen-1][0].replace(" ", "-") + "/" + pairs[chosen-1][1].replace(' ', '-') + "?sellerCountry=7&language=1,3&amount=" + how_many
	driver.get(new_link) 
	
	
	print(new_link)
	html_code = driver.page_source
	soup = BeautifulSoup(html_code, 'html.parser')
	sellers = soup.find_all(class_='d-flex has-content-centered me-1')
	sellers2 = [str(x)[:-11][73:].split('\"')[0] for x in sellers][:10]
	prices = soup.find_all(class_='color-primary small text-end text-nowrap fw-bold')[:20][0::2]
	prices2 = [str(x)[:-7][63:] for x in prices]
	driver.quit()
	pack = list(zip(sellers2, prices2))
	
	for seller, price in pack:
		print(seller.ljust(20, ' '), price)
	print()
	if max_price == '':
		return
	
	first = pack[0]
	print(first)
	if float(max_price) >= float(first[1][:-2].replace(',', '.')):
		print('There is a fitting offer!')
		print(first[0].ljust(20, ' ') + first[1])
		return
		
	print()
	print('There is sadly no fitting offer!')
	print('Do you want to get notified? [y/N]')
	noti = input('>')
	if 'y' in noti:
		check(chosen_card, how_many, new_link, float(max_price))
	return
	
while True:
	print()
	card = input('Card: ').capitalize().replace(' ', '+')
	how_many = input('How Many: ')
	max_price = input('Max Price: ')

	search(card, how_many, max_price)
