import random
import datetime

# List of quotes
quotes = [
    "The best way to predict the future is to invent it. - Alan Kay",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "If you want to lift yourself up, lift up someone else. - Booker T. Washington"
]

# Select a random quote
quote = random.choice(quotes)

# Get the current date
date = datetime.date.today()

# Print the quote and the date
print(f"{quote}\n- {date}")