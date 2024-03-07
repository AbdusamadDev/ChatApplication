from openai import OpenAI
client = OpenAI(api_key="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")

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)