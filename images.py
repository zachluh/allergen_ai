import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def curate(text, client):
    with open("recipe_unsorted.txt", "w") as f:
        f.write(text)
    with open("recipe_unsorted.txt", "r") as f:
        lines = f.readlines()

    open('recipe.txt', 'w').close()

    i=0
    after_steps = False
    step_count = 1
    for line in lines:

        if len(line) > 5:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user",
                     "content": f"Correct the spelling or grammar mistakes in the following line, and do not output anything else: {line}"}
                ]

            )

            lines[i] = completion.choices[0].message.content

            if after_steps:
                step = lines[i]
                if step[0].isdigit() is False:
                    lines[i] = f"{step_count}. {step}"
                step_count += 1


            if "steps" in lines[i].lower() or "instructions" in lines[i].lower():
                after_steps = True


        i += 1




    for line in lines:
        with open("recipe.txt", "a") as f:
            f.write(f"{line}\n")



def read(client):
    for file in os.listdir(os.getcwd()):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            image = Image.open(file).convert('L')
            text = pytesseract.image_to_string(image)
            curate(text, client)






