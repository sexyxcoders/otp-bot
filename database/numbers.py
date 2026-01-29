from database.mongo import numbers

# Get a free number for a country
def get_free(country):
    return numbers.find_one({"country": country, "status": "free"})

# Mark number as used
def mark_used(num_id):
    numbers.update_one({"_id": num_id}, {"$set": {"status": "used"}})

# Free a number (e.g., on expiry)
def free_number(phone):
    numbers.update_one({"phone": phone}, {"$set": {"status": "free"}})

# Add new number
def add_number(country, phone, session):
    numbers.insert_one({
        "country": country,
        "phone": phone,
        "session": session,
        "status": "free"
    })