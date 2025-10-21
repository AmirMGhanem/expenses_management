# Google Sheets Setup Guide

## 📊 Headers for Your Expense Sheet

Add these headers in **Row 1** of your Google Sheet (Sheet1):

| Column A | Column B | Column C | Column D | Column E | Column F | Column G | Column H |
|----------|----------|----------|----------|----------|----------|----------|----------|
| **Date** | **Description** | **Amount** | **Currency** | **Category** | **Payment Method** | **User** | **Notes** |

### Header Details:

1. **Date** - Date of the expense (YYYY-MM-DD format)
2. **Description** - What was purchased or paid for
3. **Amount** - Numeric value of the expense
4. **Currency** - Currency code (USD, EUR, AED, etc.)
5. **Category** - Expense category (from predefined list)
6. **Payment Method** - How the payment was made
7. **User** - Name of the person who made the expense
8. **Notes** - Additional details or comments

## 📁 Available Categories

The bot will automatically categorize expenses into one of these:

- **Food & Dining** - Restaurants, cafes, takeout
- **Transportation** - Taxi, Uber, fuel, parking
- **Groceries** - Supermarket shopping
- **Shopping** - Clothing, electronics, general shopping
- **Entertainment** - Movies, concerts, games
- **Bills & Utilities** - Electricity, water, internet, phone
- **Healthcare** - Doctor visits, pharmacy, medical
- **Travel** - Hotels, flights, vacation expenses
- **Education** - Courses, books, training
- **Personal Care** - Haircuts, spa, beauty
- **Home & Garden** - Furniture, repairs, plants
- **Sports & Fitness** - Gym, equipment, activities
- **Gifts & Donations** - Presents, charity
- **Business** - Work-related expenses
- **Subscriptions** - Netflix, Spotify, software
- **Other** - Anything else

## 💳 Payment Methods

- Cash
- Credit Card
- Debit Card
- Bank Transfer
- Digital Wallet
- Other

## 📝 Example Data

Here's how your data will look:

| Date | Description | Amount | Currency | Category | Payment Method | User | Notes |
|------|-------------|--------|----------|----------|----------------|------|-------|
| 2025-10-21 | Coffee at Starbucks | 5.50 | USD | Food & Dining | Credit Card | John | Morning coffee |
| 2025-10-21 | Taxi to office | 15 | AED | Transportation | Cash | Sarah | |
| 2025-10-21 | Grocery shopping | 85.30 | EUR | Groceries | Debit Card | Mike | Weekly groceries |

## 🚀 Quick Setup Steps

1. Open your spreadsheet: https://docs.google.com/spreadsheets/d/1l0RayNrG0ogeIq3_1iOMxyMx-1ArjXu6mip6GRXG1Q4/edit
2. In Row 1, add the 8 headers exactly as shown above
3. Make sure the service account has Editor access
4. Start sending expense messages to your bot!

## 💡 Tips

- The bot will auto-detect the category based on the description
- You can mention payment method in your message: "Coffee $5 paid with credit card"
- Dates are auto-detected from your message or default to today
- The bot cleans and formats all data automatically

## 🎯 Example Messages

Try sending these to your bot:

- `"Lunch at McDonald's 25 AED"`
- `"Taxi ride to airport 45 USD paid with cash"`
- `"Netflix subscription 15.99 EUR on credit card"`
- `"Bought groceries for 120 AED"`
- `"Doctor visit 200 USD yesterday"`

