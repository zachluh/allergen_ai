from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("API_KEY")
)

def read_from_image():
  pass

def work(meal, recipe, allergies):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a chef"},
      {"role": "user",
       "content": f"Change the following recipe for {meal} so that a person with these allergies: {allergies} can make it: {recipe}. The recipe cannot include any of the previously mentioned allergens. You must write the ingredients first, then list each step that has to be followed"}
    ]
  )

  #images.read(client)
  return completion.choices[0].message.content

def work_from_nothing(meal, allergies):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a chef"},
      {"role": "user",
       "content": f"Create a recipe for {meal} so that a person the following allergies: {allergies} can create it. The recipe cannot include any of the previously mentioned allergens. You must write the ingredients first, then list each step that has to be followed"}
    ]
  )

  return completion.choices[0].message.content

"""def cleanup():
  with open("recipe_unsorted.txt", 'r') as ru, open("recipe_unsorted.txt", 'w') as re:
    for line in ru:
      if line.rstrip():
        re.write(line)"""









