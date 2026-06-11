import asyncio
import os
from aiohttp import web
from telegram import Bot, LinkPreviewOptions

BOT_TOKEN = "8929884157:AAH2_l-iYqOOTUmMayvrSIIPGmEQba64sOk"
CHANNEL_ID = "@KAZELIDERMODS"

bot = Bot(token=BOT_TOKEN)

# 1. TEMPLATE PARA SA MLBB UPDATE
MLBB_MESSAGE = """<b>UPDATE FOR (VIP USER) ONLY v2.8.0</b>

<a href="https://t.me/KAZELIDERMODS/2001"> 📁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗜𝗻𝘁𝗲𝗿𝗻𝗮𝗹 </a>v̶̶2̶.̶8̶.̶0̶
✓ ᴅᴏɴ'ᴛ ᴛʀʏ ᴛᴏ ᴄʀᴀᴄᴋ 🤭
✓ ᴍʟʙʙ ᴠɪᴘ ᴋᴇʏ: ʙᴜʏ ɴᴏᴡ! ɴᴏ ꜰʀᴇᴇ!

mlbb issues need help?
Message: <a href="https://t.me/phia_maganda">𝑷𝒉𝒊𝒂 𝑭𝒆𝒍𝒊𝒄𝒊𝒂</a>"""

# 2. TEMPLATE PARA SA CODM
CODM_MESSAGE = """<a href="https://t.me/KAZELIDERMODS/380">𝘊𝘖𝘋𝘔 𝘎𝘈𝘙𝘌𝘕𝘈 𝘍𝘙𝘌𝘌 𝘛𝘙𝘐𝘈𝘓...</a>"""

# 3. TEMPLATE PARA SA PROMO (Naka-Quote + Malinis na Italic Fonts)
PROMO_MESSAGE = """<blockquote>𝘗𝘙𝘖𝘔𝘖 &lt; 30𝘋𝘈𝘠𝘚 &gt; (𝘔𝘓𝘉𝘉 𝘝𝘪𝘗)
  
   𝘍𝘜𝘓𝘓 𝘝𝘌𝘙𝘚𝘐𝘖𝘕 𝘞𝘐𝘛𝘏 𝘉𝘠𝘗𝘈𝘚𝘚!!

₱599 || $10.16 &gt; 30𝘋𝘈𝘠𝘚 &lt; 

𝘋𝘔: <a href="https://t.me/phia_maganda">@phia_maganda</a>/<a href="https://t.me/TADOOOHULOL">@TADOOOHULOL</a>
💥 𝘸𝘢𝘯𝘵 𝘵𝘰 𝘣𝘦 𝘳𝘦𝘴𝘦𝘭𝘭𝘦𝘳?</blockquote>"""

# Tatlong templates na magsalitan sa 2-minute loop
ALL_MESSAGES = [MLBB_MESSAGE, CODM_MESSAGE, PROMO_MESSAGE]

async def loop_spam():
    print("Spammer bot started (Alternating MLBB, CODM, and PROMO + 2 mins delay)...")
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

            # 2. BIBILANG NG 2 MINUTO (120 SECONDS) BAGO BURAHIN
            await asyncio.sleep(120)

            # 3. BURAHIN PAGKATAPOS NG 2 MINUTO
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
   
