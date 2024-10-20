import os
import requests
import telepot


# Function to fetch crypto prices
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,binancecoin,the-open-network,solana,dogecoin,pepe,floki',
        'vs_currencies': 'usd'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            'Bitcoin': data['bitcoin']['usd'],
            'Ethereum': data['ethereum']['usd'],
            'Binance Coin': data['binancecoin']['usd'],
            'TON': data['the-open-network']['usd'],
            'Solana': data['solana']['usd'],
            'Dogecoin': data['dogecoin']['usd'],
            'Pepe': f"{data['pepe']['usd']:.8f}",
            'Floki': data['floki']['usd']  # Fetch Floki coin price
        }
    except Exception as e:
        print(f"Error fetching crypto prices: {e}")
        return None


# Function to fetch weather data
def fetch_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Securely fetching the API key
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            'City': city,
            'Temperature': data['main']['temp'],
            'Description': data['weather'][0]['description'].capitalize()
        }
    except Exception as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None


# Function to get the most trending coin for the day
def fetch_trending_coin():
    url = "https://api.coingecko.com/api/v3/search/trending"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        coin = data['coins'][0]['item']  # Get the first trending coin

        trending_coin = {
            'Name': coin['name'],
            'Symbol': coin['symbol'],
            'Thumb': coin['thumb'],
            'Price': f"${coin['price_btc']:.15f}",  # Assuming price is in BTC
        }

        # Fetch more details about the trending coin, like market cap and total volume
        coin_id = coin['id']
        coin_details_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        coin_details_response = requests.get(coin_details_url)
        coin_details_response.raise_for_status()
        coin_details = coin_details_response.json()

        trending_coin['Market Cap'] = coin_details['market_data']['market_cap']['usd'] if 'market_cap' in coin_details['market_data'] else 'N/A'
        trending_coin['Total Volume'] = coin_details['market_data']['total_volume']['usd'] if 'total_volume' in coin_details['market_data'] else 'N/A'

        return trending_coin
    except Exception as e:
        print(f"Error fetching trending coin: {e}")
        return None


# Function to fetch exchange rates
def fetch_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = data['rates']
        exchange_rates = {
            'USD to MDL': rates['MDL'],
            'USD to AED': rates['AED'],
            'USD to RON': rates['RON'],
            'USD to RUB': rates['RUB'],
            'USD to UAH': rates['UAH'],
            'EUR to MDL': rates['MDL'] / rates['EUR'],  # Calculate EUR to MDL
        }
        return exchange_rates
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None


# Function to create the message content
def create_message():
    prices = fetch_crypto_prices()
    weather_chisinau = fetch_weather('Chisinau')
    weather_abu_dhabi = fetch_weather('Abu Dhabi')
    trending_coin = fetch_trending_coin()
    exchange_rates = fetch_exchange_rates()

    if prices and weather_chisinau and weather_abu_dhabi and trending_coin and exchange_rates:
        message = (
            f"📢\n"
            f"Привет, сосунки! Я ваш крипто босс😎.\n"
            f"Мой хоязин запрограммировал меня и теперь каждый день я буду писать вам в 9 утром и вечером.\n\n"
            f"Вот вам курс крипты на сегодня, держите краба🦀\n\n"
            f"☂️Weather Updates:\n"
            f"Chisinau: {weather_chisinau['Temperature']}°C, {weather_chisinau['Description']}\n"
            f"Abu Dhabi: {weather_abu_dhabi['Temperature']}°C, {weather_abu_dhabi['Description']}\n\n"
            f"🐸Crypto Prices Update:\n"
            f"Bitcoin: ${prices['Bitcoin']}\n"
            f"Ethereum: ${prices['Ethereum']}\n"
            f"Binance Coin: ${prices['Binance Coin']}\n"
            f"TON: ${prices['TON']}\n"
            f"Solana: ${prices['Solana']}\n"
            f"Dogecoin: ${prices['Dogecoin']}\n"
            f"Pepe: ${prices['Pepe']}\n"
            f"Floki: ${prices['Floki']}\n\n"
            f"📈Trending Coin for Today:\n"
            f"Name: {trending_coin['Name']}\n"
            f"Symbol: {trending_coin['Symbol']}\n"
            f"Price: {trending_coin['Price']}\n"
            f"Market Cap: ${trending_coin['Market Cap']}\n"
            f"Total Volume: ${trending_coin['Total Volume']}\n"
            f"Thumbnail: {trending_coin['Thumb']}\n\n"
            f"💸Exchange Rates:\n"
            f"💵Exchange Rate for 1 USD:\n"
            f"MDL: {exchange_rates['USD to MDL']:.2f}\n"
            f"💶Exchange Rate for 1 EURO:\n"
            f"MDL: {exchange_rates['EUR to MDL']:.2f}\n"
            f"Exchange Rate for 1 USD (Other Currencies):\n"
            f"AED: {exchange_rates['USD to AED']:.2f}\n"
            f"RON: {exchange_rates['USD to RON']:.2f}\n"
            f"RUB: {exchange_rates['USD to RUB']:.2f}\n"
            f"UAH: {exchange_rates['USD to UAH']:.2f}"
        )
        return message
    return None


# Function to send a message via Telegram bot
def send_message_via_telegram(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Securely fetching the bot token
    chat_id = os.getenv("CHAT_ID")  # Securely fetching the chat ID
    if not bot_token or not chat_id:
        print("Error: Bot token or chat ID is missing.")
        return

    bot = telepot.Bot(bot_token)
    try:
        bot.sendMessage(chat_id, message)
        print(f"Message sent successfully to chat ID: {chat_id}")
    except Exception as e:
        print(f"Error sending message: {e}")


if __name__ == "__main__":
    # Send message when the script is run (on first deploy or cron job)
    message = create_message()
    if message:
        send_message_via_telegram(message)
