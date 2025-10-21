# Telegram Expense Bot

A Telegram bot that processes expense messages using Google Gemini AI and stores them in Google Sheets with automatic categorization and smart data extraction.

## Project Structure

```
telegram-expense-bot/
├── api/
│   └── webhook.py     # FastAPI handler (entry point)
├── requirements.txt
├── service_account.json  # Google Service Account credentials
├── vercel.json          # Vercel deployment configuration
├── .env                 # Environment variables (not in git)
├── .env.example         # Environment variables template
└── README.md
```

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your `TELEGRAM_TOKEN` from [@BotFather](https://t.me/botfather)
   - Add your `OPENAI_API_KEY` from [OpenAI](https://platform.openai.com/api-keys)

4. **Set up Google Sheets**
   - Create a Google Cloud project
   - Enable Google Sheets API
   - Create a service account and download the JSON key
   - Save it as `service_account.json`
   - Share your Google Sheet with the service account email

5. **Deploy to Vercel**
   ```bash
   vercel
   ```

6. **Set webhook for Telegram**
   ```bash
   curl -X POST https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-vercel-app.vercel.app/"}'
   ```

## 📊 Google Sheets Setup

**Add these headers in Row 1 of your Google Sheet:**

```
Date | Description | Amount | Currency | Category | Payment Method | User | Notes
```

See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for detailed setup instructions.

## 🎯 Features

- **Smart Parsing** - Natural language expense extraction using Google Gemini AI
- **Auto-Categorization** - 16 predefined categories (Food, Transport, etc.)
- **Payment Methods** - Track how you paid (Cash, Credit Card, etc.)
- **Multi-Currency** - Supports USD, EUR, AED, and more
- **Date Detection** - Auto-detects dates or uses current date
- **Rich Telegram Response** - Formatted confirmation with emoji

## 💡 Usage Examples

Send expense messages to your Telegram bot in natural language:

```
"Lunch at Starbucks 25 USD"
"Taxi ride 15 AED paid with cash"
"Grocery shopping 85 EUR on credit card"
"Doctor visit 200 USD yesterday"
"Netflix subscription 15.99"
```

The bot will:
1. Parse the message using Gemini AI
2. Extract: date, description, amount, currency, category, payment method
3. Auto-categorize the expense
4. Store it in Google Sheets
5. Send a formatted confirmation message

## 📁 Categories

- Food & Dining
- Transportation
- Groceries
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Travel
- Education
- Personal Care
- Home & Garden
- Sports & Fitness
- Gifts & Donations
- Business
- Subscriptions
- Other

## 🔌 API Endpoints

- `GET /` - Health check
- `GET /categories` - Get list of available categories and payment methods
- `POST /test` - Test endpoint for manual testing (in Swagger docs)
- `POST /` - Telegram webhook endpoint

## 🌐 Environment Variables

- `TELEGRAM_TOKEN` - Your Telegram bot token from [@BotFather](https://t.me/botfather)
- `GEMINI_API_KEY` - Your Google Gemini API key (FREE tier available)

## License

MIT

# expenses_management
