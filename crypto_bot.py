import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Get token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Debugging output
print(f"Loaded TOKEN: {TELEGRAM_BOT_TOKEN}")
print(f"Loaded CHAT ID: {TELEGRAM_CHAT_ID}")

# Stop script if variables are missing
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing! Check your .env file.")

# Function to get top 10 crypto prices
def get_top_crypto_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
    response = requests.get(url).json()
    return response

def format_top_crypto_prices():
    prices = get_top_crypto_prices()
    message = "\U0001F4C8 *Top 10 Cryptos by Market Cap:*\n"
    for crypto in prices:
        message += f"\U0001F539 {crypto['name']} ({crypto['symbol'].upper()}): ${crypto['current_price']}\n"
    return message

# Function to get specific crypto prices
def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple,solana&vs_currencies=usd"
    response = requests.get(url).json()
    return response

# Function to fetch top crypto news
def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    response = requests.get(url).json()
    return response["Data"][:5]

async def crypto_news(update: Update, context: CallbackContext):
    news = get_crypto_news()
    message = "\U0001F4F0 *Top Crypto News:*\n"
    for article in news:
        message += f"\U0001F4D6 [{article['title']}]({article['url']})\n"
    await update.message.reply_text(message, parse_mode="Markdown")

# Command: /start
async def start(update: Update, context: CallbackContext):
    message = (
        "\U0001F680 Welcome to the *Crypto Tracker Bot*!\n\n"
        "\U0001F4C8 /price - Get BTC, ETH, XRP, and SOL prices.\n"
        "\U0001F4CA /startprice - Get the top 10 cryptos by market cap.\n"
        "\U0001F503 /changes - Get 24-hour price changes for the top 5 cryptos.\n"
        "\U0001F525 /trending - See which cryptos are trending now.\n"
        "\U0001F4B0 /btcdominance - Get Bitcoin's market dominance.\n"
        "\U0001F4F0 /news - Get the latest crypto news.\n"
        "\U0001F914 /feargreed - Check the Fear & Greed Index.\n\n"
        "Use any of the commands above to get started!"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# Command: /price
async def get_price(update: Update, context: CallbackContext):
    prices = get_crypto_prices()
    message = "\n".join([f"{crypto.upper()}: ${price['usd']}" for crypto, price in prices.items()])
    await update.message.reply_text(f"\U0001F4B8 Current Prices:\n{message}")

# Command: /startprice (Top 10 Cryptos)
async def start_price(update: Update, context: CallbackContext):
    message = format_top_crypto_prices()
    await update.message.reply_text(message, parse_mode="Markdown")

# Main function to start the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", get_price))
    application.add_handler(CommandHandler("startprice", start_price))
    application.add_handler(CommandHandler("news", crypto_news))

    print("Crypto Bot is now running...")
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
