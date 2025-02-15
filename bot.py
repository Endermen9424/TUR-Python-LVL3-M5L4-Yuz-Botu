import os
import discord
from discord.ext import commands
from logic import process_image
from config import TOKEN

# Botu başlatma
intents = discord.Intents.default()
intents.message_content = True  # Mesaj içeriğini almak için gerekli
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot hazır olduğunda gerçekleşen olay
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı.')

# Başlatma komutu
@bot.command(name='start')
async def start(ctx):
    await ctx.send("Merhaba! Bana bir fotoğraf gönderin, fotoğraftaki yüzleri bulanıklaştıracağım!")

# Görselleri işleme
@bot.event
async def on_message(message):
    # Mesajın botun kendisinden gelmediğini kontrol etme
    if message.author == bot.user:
        return
    
    # Mesajın bir ek içerip içermediğini kontrol etme
    if message.attachments:
        try:
            attachment = message.attachments[0]
            # Eklenen dosyanın bir görsel olduğunu kontrol etme
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Dosya uzantısını belirleme
                file_ext = '.jpg' if attachment.filename.lower().endswith('.jpg') else '.png'
                
                # Giriş ve çıkış dosyaları için yolları belirleme
                input_file_path = f"input{file_ext}"
                output_file_path = f"output{file_ext}"
                
                # Giriş görüntüsünü kaydetme
                await attachment.save(input_file_path)

                # Görüntüyü işleme (yüzleri bulanıklaştırma)
                process_image(input_file_path, output_file_path)

                # İşlenmiş görüntüyü gönderme
                await message.channel.send(file=discord.File(output_file_path))

                # Geçici dosyaları silme
                os.remove(input_file_path)
                os.remove(output_file_path)
            else:
                await message.channel.send("Lütfen PNG, JPG veya JPEG formatında bir görsel gönderin.")
        
        except Exception as e:
            await message.channel.send(f"Bir hata oluştu: {str(e)}")
    
    # Komutları işlemeyi unutmama
    await bot.process_commands(message)

# Bilgi komutu
@bot.command(name='info')
async def help_command(ctx):
    await ctx.send("Merhaba! Bana bir fotoğraf gönderin, fotoğraftaki yüzleri bulanıklaştıracağım!")

if __name__ == "__main__":
    bot.run(TOKEN)
