from django.http import JsonResponse
import requests

# Define your API URL (replace this with the actual API URL)
API_URL = "https://api.github.com/users"

def get_data(request):
    """
    Fetch data from an external API and return it as JSON response.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
