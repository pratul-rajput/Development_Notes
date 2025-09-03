#Read the documentation provided while creating the api key on google studio

#first create the api key from  google studio platform then pass your api key to the below snippet or keep in .env file and use it.

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyDZ25QpOlSTrbKJ86Smu8ROYVZQeR2FbVQ")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain about Amrita Vishwa Vidyapeetham Mysore"
)
print(response.text)
