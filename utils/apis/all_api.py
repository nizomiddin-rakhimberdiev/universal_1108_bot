import requests
import wikipediaapi

response = requests.get('http://cbu.uz/uz/arkhiv-kursov-valyut/json/').json()


def get_weather(city):
    api_key = "151ba04fd90792c7e8fc1ea5a18e52b6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    weather_response = requests.get(url).json()
    if weather_response.get("cod") != 200:
        return "Shahar topilmadi"
    temp = weather_response["main"]["temp"]
    description = weather_response["weather"][0]["description"]
    return f"Shahar: {city}\nTemperatura: {temp}℃\nMa'lumot: {description}"


def get_wikipedia_summary(topic):
    wiki = wikipediaapi.Wikipedia('uz', user_agent='WeatherTranslateBot/1.0 (admin@mybot.com)')  # User-agent qo'shildi
    page = wiki.page(topic)
    if not page.exists():
        return "Mavzu topilmadi"
    return page.summary[:500]




