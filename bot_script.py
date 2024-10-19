import os
import requests
import telepot
import time

# Function to fetch crypto prices
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,binancecoin,the-open-network,solana,dogecoin,pepe',
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
            'Pepe': f"{data['pepe']['usd']:.8f}"
        }
    except Exception as e:
        print(f"Error fetching crypto prices: {e}")
        return None

# Function to fetch weather data
def fetch_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Securely fetching the API key from GitHub Secrets
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

# Function to send a message via Telegram bot
def send_message_via_telegram(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Securely fetching the bot token from GitHub Secrets
    chat_id = os.getenv("CHAT_ID")  # Securely fetching the chat ID from GitHub Secrets
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
    while True:
        prices = fetch_crypto_prices()
        weather_chisinau = fetch_weather('Chisinau')
        weather_abu_dhabi = fetch_weather('Abu Dhabi')

        if prices and weather_chisinau and weather_abu_dhabi:
            message = (
                f"Привет, сосунки! Я ваш крипто босс😎.\n"
                f"Вот вам курс крипты на сегодня, держите краба🦀\n\n"
                f"Crypto Prices Update:\n"
                f"Bitcoin: ${prices['Bitcoin']}\n"
                f"Ethereum: ${prices['Ethereum']}\n"
                f"Binance Coin: ${prices['Binance Coin']}\n"
                f"TON: ${prices['TON']}\n"
                f"Solana: ${prices['Solana']}\n"
                f"Dogecoin: ${prices['Dogecoin']}\n"
                f"Pepe: ${prices['Pepe']}\n\n"
                f"Weather Updates:\n"
                f"Chisinau: {weather_chisinau['Temperature']}°C, {weather_chisinau['Description']}\n"
                f"Abu Dhabi: {weather_abu_dhabi['Temperature']}°C, {weather_abu_dhabi['Description']}"
            )
            print(message)  # For local testing
            send_message_via_telegram(message)

        # Wait for 30 seconds before sending the next message
        time.sleep(30)
