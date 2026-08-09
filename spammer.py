import asyncio
import os
from aiohttp import web
from telegram import Bot, LinkPreviewOptions

BOT_TOKEN = "8929884157:AAH2_l-iYqOOTUmMayvrSIIPGmEQba64sOk"
CHANNEL_ID = "@SliderModMenuMlbb"

bot = Bot(token=BOT_TOKEN)

# 1. TEMPLATE PARA SA MLBB UPDATE
MLBB_MESSAGE = """<blockquote expandable="true"><i><a href="https://t.me/SliderModMenuMlbb/6270">Latest Update:
Mobile Legends: Bang Bang
v2.1.95.12053 || Mod v3.1.7</a>

NEED KEY LOGIN ??? :
For inquiries and availment, send a direct message ~ <a href="https://t.me/phia_maganda">Phia Felicia</a>

No Free 🫪 GETS!?</i></blockquote>"""

# 2. TEMPLATE PARA SA CODM
CODM_MESSAGE = """<blockquote expandable="true"><i><a href="https://t.me/SliderModMenuMlbb/380">Latest Update: Call of Duty v1.6.56
Garena Injector v2.8.0
Global Injector v1.2.5</a>

NEED KEY LOGIN ??? :
For inquiries and availment, send a direct message ~ <a href="https://t.me/phia_maganda">𝑷𝒉𝒊𝒂 𝑭𝒆𝒍𝒊𝒄𝒊𝒂</a>

<a href="https://slidermodmenucodm-registerdeviceid-garena.onrender.com/free">Try Trial Key Here:</a></i></blockquote>"""

# 3. BAGONG TEMPLATE PARA SA PROMO (May expandable quote at bagong link)
PROMO_MESSAGE = """<blockquote expandable="true"><i><a href="https://t.me/SliderModMenuMlbb/8279">Promo Available :
For Mobile Legends: Bang Bang
Discounted price : up-to 50%</a>

AVAIL NOW! :
For inquiries and availment, send a direct message ~ <a href="https://t.me/phia_maganda">Phia Felicia</a></i></blockquote>"""

# Tatlong templates na magsalitan sa loop
ALL_MESSAGES = [MLBB_MESSAGE, CODM_MESSAGE, PROMO_MESSAGE]

async def loop_spam():
    print("Spammer bot started (Alternating MLBB, CODM, and PROMO)...")
    index = 0
    
    while True:
        try:
            current_message = ALL_MESSAGES[index % len(ALL_MESSAGES)]
            
            # 1. IPAPALAPAG ANG CURRENT MESSAGE
            sent_message = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=current_message,
                parse_mode="HTML",
                disable_notification=False,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            print(f"Message sent! (Index: {index} | ID: {sent_message.message_id})")

            # 2. BIBILANG NG ORAS BAGO BURAHIN (3600 seconds = 1 hour)
            await asyncio.sleep(3600)          

            # 3. BURAHIN PAGKATAPOS
            await bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=sent_message.message_id
            )
            print(f"Deleted Message ID: {sent_message.message_id}")

            # 4. AGWAT BAGO MAG-SEND ULIT NG KASUNOD NA MESSAGE (3 seconds)
            await asyncio.sleep(3)
            
            index += 1

        except Exception as e:
            print("Error sa loop:", e)
            await asyncio.sleep(10)

# --- RENDER WEB SERVER CONFIGURATION ---
async def handle_index(request):
    return web.Response(text="Bot is running smoothly on Render!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    print(f"Starting dummy web server on port {port} for Render...")
    await site.start()
    
    await loop_spam()

if __name__ == "__main__":
    asyncio.run(main())
