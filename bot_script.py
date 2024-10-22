import os
import requests
import telepot
from datetime import datetime, timedelta

# Function to fetch crypto prices from cryptorank.io
def fetch_crypto_prices_cr():
    url = "https://api.cryptorank.io/v1/currencies"
    api_key = os.getenv("CRYPTO_RANK_API_KEY")
    params = {
        'api_key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['data']

        crypto_data = {}
        for crypto in data:
            name = crypto['name']
            values = crypto['values']['USD']

            crypto_data[name] = {
                'Price': values['price'],
                'Volume (24h)': values['volume24h'],
                'High (24h)': values['high24h'],
                'Low (24h)': values['low24h'],
                'Market Cap': values['marketCap'],
                'Percent Change (24h)': values['percentChange24h'],
                'Percent Change (7d)': values['percentChange7d'],
                'Percent Change (30d)': values['percentChange30d'],
                'Percent Change (3m)': values['percentChange3m'],
                'Percent Change (6m)': values['percentChange6m']
            }

        return crypto_data

    except Exception as e:
        print(f"Error fetching crypto prices: {e}")
        return None

# Function to fetch market cap dominance (BTC, ETH)
def fetch_market_cap_dominance_cr():
    url = "https://api.cryptorank.io/v1/global"
    api_key = os.getenv("CRYPTO_RANK_API_KEY")
    params = {
        'api_key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['data']

        return {
            'BTC Dominance': data['btcDominance'],
            'ETH Dominance': data['ethDominance']
        }
    except Exception as e:
        print(f"Error fetching market cap dominance: {e}")
        return None

# Helper function to get the correct emoji based on percentage change
def get_trend_emoji(value):
    # Ensure the value is a number (default to 0 if None)
    value = value if value is not None else 0
    return "📈" if value > 0 else "📉"

# Helper function to safely format values, replacing None with 'N/A' or default
def safe_format(value, default='N/A', precision=2):
    return f"{value:.{precision}f}" if value is not None else default

# Function to create message for specific cryptocurrency
def create_crypto_message_cr(name, details, dominance=None):
    # Only include dominance if it's provided
    dominance_line = f"🌐 Dominance: {safe_format(dominance)}%\n" if dominance is not None else ""

    # Safely format values
    price = safe_format(details.get('Price'))
    volume_24h = safe_format(details.get('Volume (24h)'))
    high_24h = safe_format(details.get('High (24h)'))
    low_24h = safe_format(details.get('Low (24h)'))
    market_cap = safe_format(details.get('Market Cap'))
    percent_change_24h = safe_format(details.get('Percent Change (24h)'))
    percent_change_7d = safe_format(details.get('Percent Change (7d)'))
    percent_change_30d = safe_format(details.get('Percent Change (30d)'))
    percent_change_3m = safe_format(details.get('Percent Change (3m)'))
    percent_change_6m = safe_format(details.get('Percent Change (6m)'))

    # Generate the message with emojis
    return (
        f"💰 {name}:\n"
        f"💵 Price: ${price}\n"
        f"{dominance_line}"
        f"📊 Volume (24h): ${volume_24h}\n"
        f"📈 High (24h): ${high_24h}\n"
        f"📉 Low (24h): ${low_24h}\n"
        f"🏦 Market Cap: ${market_cap}\n"
        f"{get_trend_emoji(details.get('Percent Change (24h)', 0))} Percent Change (24h): {percent_change_24h}%\n"
        f"{get_trend_emoji(details.get('Percent Change (7d)', 0))} Percent Change (7d): {percent_change_7d}%\n"
        f"{get_trend_emoji(details.get('Percent Change (30d)', 0))} Percent Change (30d): {percent_change_30d}%\n"
        f"{get_trend_emoji(details.get('Percent Change (3m)', 0))} Percent Change (3m): {percent_change_3m}%\n"
        f"{get_trend_emoji(details.get('Percent Change (6m)', 0))} Percent Change (6m): {percent_change_6m}%\n"
        f"\n"
    )

# Function to fetch crypto prices
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,binancecoin,the-open-network,solana,dogecoin,pepe,floki',
        'vs_currencies': 'usd',
        'include_market_cap': 'true'  # Include market cap in the response
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Fetch Bitcoin market cap
        btc_market_cap = data['bitcoin']['usd_market_cap']

        # Fetch the total cryptocurrency market cap from a global endpoint
        total_market_cap_url = "https://api.coingecko.com/api/v3/global"
        total_market_cap_response = requests.get(total_market_cap_url)
        total_market_cap_response.raise_for_status()
        total_market_cap_data = total_market_cap_response.json()
        total_market_cap = total_market_cap_data['data']['total_market_cap']['usd']

        # Calculate Bitcoin market cap dominance
        btc_dominance = (btc_market_cap / total_market_cap) * 100

        return {
            'Bitcoin': data['bitcoin']['usd'],
            'Bitcoin Dominance': btc_dominance,  # Include Bitcoin dominance
            'Ethereum': data['ethereum']['usd'],
            'Binance Coin': data['binancecoin']['usd'],
            'TON': data['the-open-network']['usd'],
            'Solana': data['solana']['usd'],
            'Dogecoin': data['dogecoin']['usd'],
            'Pepe': f"{data['pepe']['usd']:.8f}",
            'Floki': data['floki']['usd']
        }
    except Exception as e:
        print(f"Error fetching crypto prices: {e}")
        return None


# Function to format UNIX timestamps into human-readable time
def format_time(unix_timestamp, timezone_offset):
    return datetime.utcfromtimestamp(unix_timestamp + timezone_offset).strftime('%H:%M %p')


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

        weather_info = {
            'City': city,
            'Temperature': data['main']['temp'],
            'Feels Like': data['main']['feels_like'],
            'Min Temp': data['main']['temp_min'],
            'Max Temp': data['main']['temp_max'],
            'Humidity': data['main']['humidity'],
            'Wind Speed': data['wind']['speed'],
            'Weather Description': data['weather'][0]['description'].capitalize(),
            # 'Icon': data['weather'][0]['icon'],  # Weather icon code
            'Sunrise': format_time(data['sys']['sunrise'], data['timezone']),
            'Sunset': format_time(data['sys']['sunset'], data['timezone'])
        }
        return weather_info
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

        trending_coin['Market Cap'] = coin_details['market_data']['market_cap']['usd'] if 'market_cap' in coin_details[
            'market_data'] else 'N/A'
        trending_coin['Total Volume'] = coin_details['market_data']['total_volume']['usd'] if 'total_volume' in \
                                                                                              coin_details[
                                                                                                  'market_data'] else 'N/A'

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

# Function to determine if it's morning or evening based on UTC+4
def get_greeting():
    # Get the current time in UTC and add 4 hours
    current_time_utc = datetime.utcnow()
    adjusted_time = current_time_utc + timedelta(hours=12)

    # Check if the adjusted time is before or after 12 PM
    if adjusted_time.hour < 12:
        return "Доброе утро"
    else:
        return "Добрый вечер"


# Function to create the message content
def create_message():
    greeting = get_greeting()  # Get the appropriate greeting based on time
    prices = fetch_crypto_prices()
    crypto_prices = fetch_crypto_prices_cr()
    dominance = fetch_market_cap_dominance_cr()
    weather_chisinau = fetch_weather('Chisinau')
    weather_abu_dhabi = fetch_weather('Abu Dhabi')
    trending_coin = fetch_trending_coin()
    exchange_rates = fetch_exchange_rates()

    if prices and weather_chisinau and weather_abu_dhabi and trending_coin and exchange_rates:
        message = (
            f"📢\n"
            f"{greeting}, криптанам!😎\n"  # Use the greeting here
            f"Update на сегодня, держите краба🦀\n\n"
            f"☂️Weather Updates:\n"
            f"Chisinau: {weather_chisinau['Temperature']}°C, {weather_chisinau['Weather Description']}\n"
            f"  💁🏻‍♂️Feels like: {weather_chisinau['Feels Like']}°C\n"
            f"  ⬇️Min Temp: {weather_chisinau['Min Temp']}°C, ⬆️Max Temp: {weather_chisinau['Max Temp']}°C\n"
            f"  🌅Sunrise: {weather_chisinau['Sunrise']}, 🌇Sunset: {weather_chisinau['Sunset']}\n\n"
            f"Abu Dhabi: {weather_abu_dhabi['Temperature']}°C, {weather_abu_dhabi['Weather Description']}\n"
            f"  💁🏻‍♂️Feels like: {weather_abu_dhabi['Feels Like']}°C\n"
            f"  ⬇️Min Temp: {weather_abu_dhabi['Min Temp']}°C, ⬆️Max Temp: {weather_abu_dhabi['Max Temp']}°C\n"
            f"  🌅Sunrise: {weather_abu_dhabi['Sunrise']}, 🌇Sunset: {weather_abu_dhabi['Sunset']}\n\n"
            f"🐸Crypto Prices Update:\n"
            f"{create_crypto_message_cr("Bitcoin", crypto_prices['Bitcoin'], dominance['BTC Dominance'])}"
            f"{create_crypto_message_cr("Ethereum", crypto_prices['Ethereum'], dominance['ETH Dominance'])}"
            f"🪙Binance Coin: ${prices['Binance Coin']}\n"
            f"🪙TON: ${prices['TON']}\n"
            f"🪙Solana: ${prices['Solana']}\n"
            f"🪙Dogecoin: ${prices['Dogecoin']}\n"
            f"🪙Pepe: ${prices['Pepe']}\n"
            f"🪙Floki: ${prices['Floki']}\n\n"
            f"📈🪙Trending Coin for Today:\n"
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
            f"UAH: {exchange_rates['USD to UAH']:.2f}\n"
        )
        return message
    return None


# Function to send message via Telegram
def send_message_via_telegram(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Securely fetching the bot token
    chat_id = os.getenv("CHAT_ID")  # Securely fetching the chat ID
    bot = telepot.Bot(bot_token)
    bot.sendMessage(chat_id, message)


if __name__ == "__main__":
    message = create_message()
    if message:
        send_message_via_telegram(message)
        print("Message sent successfully!")
    else:
        print("Failed to fetch data or create the message.")
