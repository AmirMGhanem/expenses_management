from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from pydantic import BaseModel
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file (local only)
load_dotenv()

app = FastAPI()

# Get environment variables (lazy loaded)
def get_env(key: str, required: bool = True):
    """Get environment variable with error handling"""
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"{key} not found in environment variables")
    return value

# Google Sheets setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Global variables (initialized on first request)
gemini_model = None
client = None
sheet = None
bot = None

def initialize_services():
    """Initialize all services (called on first request)"""
    global gemini_model, client, bot
    
    if gemini_model is None:
        # Initialize Gemini
        GEMINI_API_KEY = get_env("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    if client is None:
        # Initialize Google Sheets
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        
        if service_account_json:
            # Production: Load from environment variable
            service_account_info = json.loads(service_account_json)
            creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        else:
            # Local: Load from file
            creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        
        client = gspread.authorize(creds)
    
    if bot is None:
        # Initialize Telegram bot
        TELEGRAM_TOKEN = get_env("TELEGRAM_TOKEN")
        bot = Bot(token=TELEGRAM_TOKEN)

# Predefined expense categories
EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Groceries",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Healthcare",
    "Travel",
    "Education",
    "Personal Care",
    "Home & Garden",
    "Sports & Fitness",
    "Gifts & Donations",
    "Business",
    "Subscriptions",
    "Other"
]

# Payment methods
PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Digital Wallet", "Other"]

def get_sheet():
    """Lazy load the Google Sheet"""
    global sheet, client
    initialize_services()  # Ensure services are initialized
    
    if sheet is None:
        # Open by spreadsheet ID
        spreadsheet = client.open_by_key("1l0RayNrG0ogeIq3_1iOMxyMx-1ArjXu6mip6GRXG1Q4")
        sheet = spreadsheet.sheet1
    return sheet

def parse_expense(text: str) -> dict:
    """Parse expense message using Gemini AI"""
    global gemini_model
    initialize_services()  # Ensure services are initialized
    
    categories_list = ", ".join(EXPENSE_CATEGORIES)
    payment_methods_list = ", ".join(PAYMENT_METHODS)
    
    prompt = f"""
    Extract structured data from this expense message:
    "{text}"
    
    Analyze and extract:
    1. Amount (numeric value only)
    2. Currency (USD, EUR, AED, etc.)
    3. Description (what was purchased/paid for)
    4. Category (choose the most appropriate from: {categories_list})
    5. Payment method if mentioned (from: {payment_methods_list})
    6. Date if mentioned (format: YYYY-MM-DD), otherwise use today
    7. Notes or additional details
    
    Return ONLY a valid JSON object with these fields:
    {{
        "amount": "number",
        "currency": "string",
        "description": "string",
        "category": "string",
        "payment_method": "string or null",
        "date": "YYYY-MM-DD",
        "notes": "string or null"
    }}
    """
    
    try:
        response = gemini_model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up response - remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        
        # Validate and set defaults
        if not parsed.get("amount"):
            parsed["amount"] = "0"
        if not parsed.get("currency"):
            parsed["currency"] = "USD"
        if not parsed.get("description"):
            parsed["description"] = text
        if not parsed.get("category") or parsed["category"] not in EXPENSE_CATEGORIES:
            parsed["category"] = "Other"
        if not parsed.get("date"):
            parsed["date"] = datetime.now().strftime("%Y-%m-%d")
        if not parsed.get("payment_method"):
            parsed["payment_method"] = ""
        if not parsed.get("notes"):
            parsed["notes"] = ""
            
        return parsed
    except Exception as e:
        # Fallback if parsing fails
        return {
            "amount": "0",
            "currency": "USD",
            "description": text,
            "category": "Other",
            "payment_method": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "notes": f"Parse error: {str(e)}"
        }

class TestExpense(BaseModel):
    text: str
    user_name: str = "Test User"

@app.get("/")
async def root():
    """Root endpoint"""
    return {"status": "Bot is running!", "version": "2.0"}

@app.get("/categories")
async def get_categories():
    """Get list of available expense categories"""
    return {
        "categories": EXPENSE_CATEGORIES,
        "payment_methods": PAYMENT_METHODS
    }

@app.post("/test")
async def test_expense(expense: TestExpense):
    """Test endpoint - Parse an expense message without Telegram"""
    # Parse the expense using Gemini
    parsed = parse_expense(expense.text)
    
    # Write to Google Sheets
    current_sheet = get_sheet()
    current_sheet.append_row([
        parsed["date"],
        parsed["description"],
        parsed["amount"],
        parsed["currency"],
        parsed["category"],
        parsed["payment_method"],
        expense.user_name,
        parsed["notes"]
    ])

    return {
        "status": "success",
        "message": f"✅ Added {parsed['description']} ({parsed['amount']} {parsed['currency']})",
        "parsed_data": parsed
    }

@app.post("/")
async def webhook(request: Request):
    """Telegram webhook endpoint"""
    global bot
    initialize_services()  # Ensure services are initialized
    
    data = await request.json()
    update = Update.de_json(data, bot)
    text = update.message.text
    
    # Parse the expense using Gemini
    parsed = parse_expense(text)
    
    # Write to Google Sheets
    current_sheet = get_sheet()
    current_sheet.append_row([
        parsed["date"],
        parsed["description"],
        parsed["amount"],
        parsed["currency"],
        parsed["category"],
        parsed["payment_method"],
        update.message.from_user.first_name,
        parsed["notes"]
    ])
    
    # Send confirmation message
    message = f"✅ *Expense Added*\n\n"
    message += f"📝 {parsed['description']}\n"
    message += f"💰 {parsed['amount']} {parsed['currency']}\n"
    message += f"📁 Category: {parsed['category']}\n"
    if parsed['payment_method']:
        message += f"💳 Payment: {parsed['payment_method']}\n"
    message += f"📅 Date: {parsed['date']}"
    
    await update.message.reply_text(message, parse_mode='Markdown')

    return {"ok": True}

