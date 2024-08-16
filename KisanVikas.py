from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator
import requests

app = Flask(__name__)  # Server Part
translator = Translator()

# Dictionary to store user language preferences and location
user_language_preferences = {}
user_locations = {}
user_soil_health_stage = {}

# Language options dictionary
language_options = {
    "1": ("en", "Language set to English."),
    "2": ("hi", "भाषा हिंदी में सेट की गई है।"),
    "3": ("bn", "ভাষা বাংলায় সেট করা হয়েছে।"),
    "4": ("ta", "மொழி தமிழ் செட்டாகி உள்ளது."),
    "5": ("te", "భాష తెలుగు లో సెట్ చేయబడింది.")
}

def translate_text(text, target_language):
    if target_language == 'en':
        return text  
    translation = translator.translate(text, dest=target_language)
    return translation.text

def get_weather(city_name, language_code):
    # Use OpenWeatherMap API
    api_key = '11aadbe8c1069f916e29aea3edd36110'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    # Debugging information
    print(f"Weather API Response: {data}")
    
    if data.get('cod') != 200:
        error_message = data.get('message', 'City not found. Please try again.')
        return translate_text(f"Error: {error_message}", language_code)
    
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    weather_info = f"The current weather in {city_name} is {weather_description} with a temperature of {temperature}°C."
    return translate_text(weather_info, language_code)

# Function to get Market price
def get_market_price(commodity, language_code):
    api_url = f'https://api.api-ninjas.com/v1/commodityprice?name={commodity}'
    headers = {'X-Api-Key': '0g8NxxBZh+bXo/f3plS//g==XypNrhl6yV42Sa9h'}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == requests.codes.ok:
        data = response.json()
        print(f"Market Price API Response: {data}")
        
        if isinstance(data, dict):
            if 'price' in data:
                price_description = f"The current price of {commodity} is {data.get('price', 'N/A')} per {data.get('unit', 'unit')}."
            else:
                price_description = 'Price information not available.'
        else:
            price_description = 'Price information not available.'
        
        return translate_text(price_description, language_code)
    else:
        error_message = 'Unable to fetch market prices. Please try again later.'
        return translate_text(f"Error: {error_message}", language_code)

def get_soil_health_info(language_code):
    # Provide general information about soil health
    soil_info = """
    Soil health is critical for successful farming. Here are some key points:
    
    1️⃣ *Soil Testing:* It's important to test your soil regularly to understand its nutrient levels. You can use DIY soil test kits or visit a nearby agricultural lab.
    
    2️⃣ *Fertilizer Recommendations:* Based on the soil test results, you can choose the right type and quantity of fertilizer. Nitrogen, phosphorus, and potassium are the primary nutrients.
    
    3️⃣ *pH Level Monitoring:* The pH level of the soil affects nutrient availability. Most crops prefer a pH between 6 and 7. Use lime to raise pH or sulfur to lower it.
    
    4️⃣ *Soil Moisture Levels:* Maintaining proper moisture is essential. Consider using drip irrigation or mulching to retain moisture.
    
    5️⃣ *Nutrient Deficiency:* Symptoms like yellowing leaves or stunted growth can indicate nutrient deficiencies. Adjust fertilization accordingly.
    """
    return translate_text(soil_info, language_code)

# Function to get response from the user
def get_response_message(language_code, key):
    responses = {
        "kisanvikas": "Please select an option to address:\n1️⃣ Crop Disease Detection\n2️⃣ Irrigation Management\n3️⃣ Soil Health Monitoring\n4️⃣ Market Price Alerts\n5️⃣ Weather Forecast",
        "detection": "Please send an image of the crop for disease detection.",
        "irrigation": "For irrigation management, ensure you are using the correct amount of water for your crops. Would you like specific tips?",
        "soil": "Soil health is critical for successful farming. Regular testing and proper fertilization are essential. Do you need more detailed information?",
        "market": "Please provide the commodity name.",
        "weather": "Please provide your city name for the weather forecast."
    }
    message = responses.get(key, "Sorry, I couldn't process your request.")
    return translate_text(message, language_code)

# Function to get response message for soil health monitoring
def get_soil_health_response(stage, language_code):
    responses = {
        "start": "Let's assess your soil health. Do you know your soil type? (Yes/No)",
        "soil_type": "Please specify your soil type (e.g., Sandy, Clay, Loam).",
        "ph_check": "Have you tested your soil pH recently? (Yes/No)",
        "ph_value": "Please enter the pH value.",
        "fertility_check": "Is the soil fertility adequate for your crops? (Yes/No)",
        "final_advice": "Based on your inputs, here are some recommendations for improving soil health."
    }
    message = responses.get(stage, "Sorry, I couldn't process your request.")
    return translate_text(message, language_code)

@app.route("/whatsapp", methods=['POST'])  # Main code starts here
def whatsapp_reply():
    
    incoming_msg = request.values.get('Body', '').strip().lower()
    user_number = request.values.get('From', '')
    media_url = request.values.get('MediaUrl0', '')
    response = MessagingResponse()

    # Check if user is ending the conversation
    if incoming_msg in ["exit", "bye", "dhanyawad", "धन्यवाद"]:
        response_text = "Thank you for using KisanVikas! Have a great day! 🌾"
        language_code = user_language_preferences.get(user_number, 'en')  # Default to English if no preference
        translated_text = translate_text(response_text, language_code)
        response.message(translated_text)
        user_language_preferences.pop(user_number, None)
        user_locations.pop(user_number, None)
        user_soil_health_stage.pop(user_number, None)
        return str(response)

    # Check if the user has already set a language preference
    if user_number not in user_language_preferences:
        # Handle language selection
        if incoming_msg in language_options:
            language_code, welcome_message = language_options[incoming_msg]
            user_language_preferences[user_number] = language_code
            response.message(translate_text(f"{welcome_message} Welcome to KisanVikas! 🌾 We're here to assist you with all your farming needs.", language_code))
        else:
            # Prompt user to select language
            response.message(
                "Please select your preferred language:\n"
                "1️⃣ For English, press 1\n"
                "2️⃣ हिंदी के लिए 2 दबाएं\n"
                "3️⃣ বাংলার জন্য ৩ টিপুন\n"
                "4️⃣ தமிழ் உடன் தொடர 4ஐ அழுத்தவும்\n"
                "5️⃣ తెలుగు లో కొనసాగించడానికి 5 నొక్కండి"
            )
    else:
        # Get the user's preferred language
        language_code = user_language_preferences[user_number]

        # Handle "KisanVikas" to select feature
        if incoming_msg == "kisanvikas":
            response_message = get_response_message(language_code, "kisanvikas")
            response.message(response_message)
        elif incoming_msg == "1":
            response_message = get_response_message(language_code, "detection")
            response.message(response_message)
        elif incoming_msg == "2":
            response_message = get_response_message(language_code, "irrigation")
            response.message(response_message)
        elif incoming_msg == "3":  # Soil Health Monitoring option
            stage = user_soil_health_stage.get(user_number, "start")
            response_message = get_soil_health_response(stage, language_code)
            response.message(response_message)

            # Update the conversation stage based on user input
            if stage == "start":
                if incoming_msg in ["yes", "no"]:
                    if incoming_msg == "yes":
                        user_soil_health_stage[user_number] = "ph_check"
                    else:
                        user_soil_health_stage[user_number] = "soil_type"
            elif stage == "soil_type":
                user_soil_health_stage[user_number] = "ph_check"
            elif stage == "ph_check":
                if incoming_msg in ["yes", "no"]:
                    if incoming_msg == "yes":
                        user_soil_health_stage[user_number] = "ph_value"
                    else:
                        user_soil_health_stage[user_number] = "fertility_check"
            elif stage == "ph_value":
                user_soil_health_stage[user_number] = "fertility_check"
            elif stage == "fertility_check":
                if incoming_msg in ["yes", "no"]:
                    user_soil_health_stage[user_number] = "final_advice"
            elif stage == "final_advice":
                # Provide final advice and reset the stage
                final_advice = translate_text("Your soil health information has been assessed. Based on the details you provided, here are some suggestions for improving your soil's health. Thank you for using KisanVikas!", language_code)
                response.message(final_advice)
                user_soil_health_stage[user_number] = "start"
        elif incoming_msg == "4":
            response_message = get_response_message(language_code, "market")
            response.message(response_message)
        elif incoming_msg == "5":
            response_message = get_response_message(language_code, "weather")
            response.message(response_message)
        else:
            # If no specific input, treat it as either a location for weather or commodity for market price
            if "market" in incoming_msg:
                commodity = incoming_msg.replace("market", "").strip()
                market_price_info = get_market_price(commodity, language_code)
                response.message(market_price_info)
            else:
                # Assuming it's a city name for weather
                weather_info = get_weather(incoming_msg, language_code)
                response.message(weather_info)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
