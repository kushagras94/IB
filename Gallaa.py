import os
import discord
import requests
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

# Set up your Discord bot token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up your Hugging Face API token
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


# Create a new Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.image'):
        parts = message.content.split(' ', 1)

        # Ensure that we have a valid command
        if len(parts) < 2:
            await message.channel.send("Please provide a prompt for the image generation.")
            return

        prompt = parts[1]

        # Inform the user that the image is being generated
        await message.channel.send("Generating image, please wait...")
        
        try:
            # Use Hugging Face API to generate image
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 28,
                    "guidance_scale": 7.0,
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code != 200:
                error_message = f"An error occurred: Status {response.status_code}"
                try:
                    error_details = response.json()
                    error_message += f"\nDetails: {error_details}"
                except:
                    pass
                await message.channel.send(error_message)
                return

            # The response content is the image data
            image_data = BytesIO(response.content)
            
            # Send the generated image to the Discord channel
            await message.channel.send(file=discord.File(image_data, 'generated_image.png'))
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

# Run the Discord bot
client.run(DISCORD_BOT_TOKEN)
