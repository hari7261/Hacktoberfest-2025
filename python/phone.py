import phonenumbers
from phonenumbers import geocoder

while(True):
    user_input = input("Enter a phone number with country code (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    try:
        phone_number = phonenumbers.parse(user_input)
        location = geocoder.description_for_number(phone_number, "en")
        print(f"Location: {location}\n")
    except phonenumbers.NumberParseException:
        print("Invalid phone number. Please try again.\n")



