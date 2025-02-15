import os
import discord
from discord.ext import commands
from logic import process_image
from config import TOKEN

# Initializing the bot
intents = discord.Intents.default()
intents.message_content = True  # Required for receiving message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Start command
@bot.command(name='start')
async def start(ctx):
    await ctx.send("Hello! Send me a photo, and I will blur the faces in it.")

# Handling images
@bot.event
async def on_message(message):
    # Checking that the message is not from the bot itself
    if message.author == bot.user:
        return
    
    # Checking that the message contains an attachment
    if message.attachments:
        try:
            attachment = message.attachments[0]
            # Checking that it is an image
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Determining the file extension
                file_ext = '.jpg' if attachment.filename.lower().endswith('.jpg') else '.png'
                
                # Setting paths for input and output files
                input_file_path = f"input{file_ext}"
                output_file_path = f"output{file_ext}"
                
                # Saving the input image
                await attachment.save(input_file_path)

                # Processing the image (blurring faces)
                process_image(input_file_path, output_file_path)

                # Sending the processed image
                await message.channel.send(file=discord.File(output_file_path))

                # Deleting temporary files
                os.remove(input_file_path)
                os.remove(output_file_path)
            else:
                await message.channel.send("Please send an image in PNG, JPG, or JPEG format.")
        
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")
    
    # Not forgetting to process commands
    await bot.process_commands(message)

# Info command
@bot.command(name='info')
async def help_command(ctx):
    await ctx.send("Send me a photo, and I will blur the faces in it.")

if __name__ == "__main__":
    bot.run(TOKEN)