# KisanVikas WhatsApp Chatbot 🌾

KisanVikas is a WhatsApp chatbot designed to assist farmers with various agricultural tasks, including crop disease detection, irrigation management, soil health monitoring, market price alerts, and weather forecasts. The chatbot is interactive, multilingual, and can be customized according to the user's preferences.

## Features

- **Multilingual Support**: Users can select their preferred language from English, Hindi, Bengali, Tamil, and Telugu.
- **Crop Disease Detection**: Users can send images of crops for disease detection.
- **Irrigation Management**: Provides tips and advice on proper irrigation techniques.
- **Soil Health Monitoring**: Offers detailed information on soil health and fertilizers.
- **Market Price Alerts**: Users can check the latest market prices for various commodities.
- **Weather Forecast**: Provides weather updates based on the user's location.

## Installation

To set up the KisanVikas chatbot on your local machine, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/kisanvikas-whatsapp-bot.git
   cd kisanvikas-whatsapp-bot
Install Dependencies
Make sure you have Python installed. Then, install the necessary Python packages:

bash
Copy code
pip install flask twilio googletrans requests
Set Up API Keys

OpenWeatherMap API Key: Obtain an API key from OpenWeatherMap and replace 'YOUR_OPENWEATHERMAP_API_KEY' in the get_weather() function.
Commodity Price API Key: Obtain an API key from Ninja API and replace 'YOUR_API_NINJAS_KEY' in the get_market_price() function.
Run the Flask App

bash
Copy code
python app.py
The app will start running on http://127.0.0.1:5000.

Configure Twilio

Set up a Twilio account and create a WhatsApp Sandbox.
Configure the webhook in the Twilio console to point to your Flask server's endpoint (e.g., http://your-ngrok-url.ngrok.io/whatsapp).
Usage
Once the setup is complete, users can interact with the chatbot via WhatsApp. The chatbot will prompt the user to select a preferred language and then provide various options to address their farming needs.

Example Commands
Send KisanVikas to start interacting with the bot.
Choose a task by replying with the corresponding number:
1 for Crop Disease Detection
2 for Irrigation Management
3 for Soil Health Monitoring
4 for Market Price Alerts
5 for Weather Forecast
User Interaction
For yes/no questions, respond with 1 for Yes or 2 for No.
To end the conversation, type exit, bye, or dhanyawad.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code follows best practices and is well-documented.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Twilio for providing the WhatsApp API.
Google Translate for translation services.
OpenWeatherMap for weather data.
Ninja API for market price data.
