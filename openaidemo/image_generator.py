from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

def generate_image():
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5",
        input="Generate an image of a futuristic AI website logo called Cloudmart",
        tools = [{"type": "image_generation"}]
    )

    image_data = [output.result for output in response.output if output.type == "image_generation_call"]
    if image_data:
        print(f"Image generation successful, size: {len(image_data)}")
        image_base64 = image_data[0]
        with open("cloudmart_logo.png", "wb") as img_file:
            img_file.write(base64.b64decode(image_base64))
    else:
        print("No image generated.")
        print(response)


if __name__ == "__main__":
    generate_image()
