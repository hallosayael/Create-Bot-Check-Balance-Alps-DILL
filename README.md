# Membuat BOT Telegram Untuk Check Balance Validator Alps DILL
## Ikuti step by step <br>

### 1. Buat Bot di Telegram <br>
Buka Telegram dan cari @BotFather. <br>
Mulai percakapan dan kirim perintah /newbot. <br>
Ikuti petunjuk untuk memberi nama dan username bot. <br>
Setelah selesai, BotFather akan memberikan token API. Simpan token ini, karena akan digunakan untuk berinteraksi dengan bot. <br>

### 2. Persiapan di VPS
#### Create folder dengan nama telegram-bot (atau terserah kalian)
```
mkdir telegram-bot
```
#### Masuk ke folder tersebut
```
cd telegram-bot
```
#### Buat file python dengan nama bot.py
```
nano bot.py
```
#### Paste code ini ke dalam file bot.py
### CATAT! GANTI url dengan PUBKEY KALIAN & bagian TOKEN dengan TOKEN BOT KALIAN
```
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
```
Lalu ctrl X dan save

### 3. Installasi <br>
#### Update Sistem:
```
sudo apt update
```
#### Install lib:
```
pip3 install python-telegram-bot
```
#### Install Dependencies:
```
sudo apt install wget gnupg2
```
#### Download dan Install Google Chrome:
```
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```
#### Verifikasi Instalasi:
```
google-chrome --version
```
#### Install Xvfb:
```
sudo apt-get install xvfb
```
#### Install screen:
```
sudo apt-get install screen
```
### 4. Eksekusi
#### Buat screen dengan nama cekdill
```
screen -R cekdill
```
#### Jalankan program
```
xvfb-run -a python3 bot.py
```
#### Cek di telegram kalian, buka bot yang sudah kalian buat dan ketik /capture
```
/capture
```
### 5. Selesai
----------------------------------------------------------------------------------------------------
### Tambahan
#### Keluar dari screen tanpa membuat program terhenti
```
tekan CTRL + A + D dengan keyboard
```
#### Cek list screen yang kalian buat
```
screen -ls
```
#### Buka screen
```
screen -r namascreen
```
#### Hapus screen
```
screen -S -X namascreen kill
```
#### Hentikan program
```
tekan CTRL + Z dengan keyboard
```
