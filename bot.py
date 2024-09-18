import asyncio
import nest_asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Allow nested asyncio loops
nest_asyncio.apply()

# Fungsi untuk menangkap screenshot
async def capture_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://alps.dill.xyz/validators?pubkey=0x111111" # Ganti dengan pubkey Anda
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        # Inisialisasi WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        await asyncio.sleep(2)  # Tunggu agar halaman sepenuhnya dimuat
        screenshot_path = "screenshot.jpg"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        # Kirim gambar screenshot ke pengguna
        with open(screenshot_path, 'rb') as file:
            await update.message.reply_photo(photo=file)

        os.remove(screenshot_path)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Terjadi kesalahan saat mengambil screenshot.")

async def main() -> None:
    TOKEN = '754xxx:AAFxxxxx'  # Ganti dengan token bot Anda
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("capture", capture_website))
    
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
