
import forecastio
api_key = '22c395cec196961c2ee209164e4ca0a0'
lat = -31.967819
lng = 115.87718

forecast = forecastio.load_forecast(api_key, lat, lng)

byHour = forecast.hourly()
current = forecast.currently()
print(byHour)
print(byHour.summary)
print(current)
print(byHour.icon)

for hourlyData in byHour.data:
	print(hourlyData.temperature)


