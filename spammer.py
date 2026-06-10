import asyncio
import os
from aiohttp import web
from telegram import Bot, LinkPreviewOptions

BOT_TOKEN = "8929884157:AAH2_l-iYqOOTUmMayvrSIIPGmEQba64sOk"
CHANNEL_ID = "@KAZELIDERMODS"

bot = Bot(token=BOT_TOKEN)

# 1. TEMPLATE PARA SA MLBB
MLBB_MESSAGE = """<b>UPDATE FOR (VIP USER) ONLY v2.8.0</b>

<a href="https://t.me/KAZELIDERMODS/2001"> 📁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗜𝗻𝘁𝗲𝗿𝗻𝗮𝗹 </a>v̶̶2̶.̶8̶.̶0̶
✓ ᴅᴏɴ'ᴛ ᴛʀʏ ᴛᴏ ᴄʀᴀᴄᴋ 🤭
✓ ᴍshared_ʟʙʙ ᴠɪᴘ ᴋᴇʏ: ʙᴜʏ ɴᴏᴡ! ɴᴏ ꜰʀᴇᴇ!

mlbb issues need help?
Message: <a href="https://t.me/phia_maganda">𝑷𝒉𝒊𝒂 𝑭𝒆𝒍𝒊𝒄𝒊𝒂</a>"""

# 2. TEMPLATE PARA SA CODM (Naka-link sa post /380)
CODM_MESSAGE = """<a href="https://t.me/KAZELIDERMODS/380">𝘊𝘖𝘋𝘔 𝘎𝘈𝘙𝘌𝘕𝘈 𝘍𝘙𝘌𝘌 𝘛𝘙𝘐𝘈𝘓...</a>"""

# Inilagay natin sa isang listahan para magsalitan sila
ALL_MESSAGES = [MLBB_MESSAGE, CODM_MESSAGE]

async def loop_spam():
    # In-update ang log message para sa 2 minutes
    print("Spammer bot started (Alternating MLBB and CODM + 2 mins delay)...")
    index = 0
    
    while True:
        try:
            # Pipiliin kung MLBB o CODM ang isesend base sa ikot ng loop
            current_message = ALL_MESSAGES[index % len(ALL_MESSAGES)]
            
            # 1. IPAPALAPAG ANG CURRENT MESSAGE
            sent_message = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=current_message,
                parse_mode="HTML",
                disable_notification=False,
                link_preview_options=LinkPreviewOptions(is_disabled=True) # Pinatay ang preview para malinis
            )
            print(f"Message sent! (Index: {index} | ID: {sent_message.message_id})")

            # ========================================================
            # 2. BIBILANG NG 2 MINUTO (120 SECONDS) BAGO BURAHIN
            # ========================================================
            await asyncio.sleep(120)

            # 3. BURAHIN PAGKATAPOS NG 2 MINUTO
            await bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=sent_message.message_id
            )
            print(f"Deleted Message ID: {sent_message.message_id}")

            # 4. AGWAT BAGO MAG-SEND ULIT NG KASUNOD NA MESSAGE
            await asyncio.sleep(3)
            
            # Dagdagan ang index para sa susunod na ikot, iba naman ang ise-send
            index += 1

        except Exception as e:
            print("Error sa loop:", e)
            await asyncio.sleep(10)

# --- RENDER WEB SERVER CONFIGURATION ---
async def handle_index(request):
    return web.Response(text="Bot is running smoothly on Render!")

async def main():
    # Gagawa ng dummy HTTP server para kay Render
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    # Awtomatikong kukunin ang PORT na binibigay ni Render, kung wala default sa 8080
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    print(f"Starting dummy web server on port {port} for Render...")
    await site.start()
    
    # Sabay na patatakbuhin ang server at ang spam loop mo
    await loop_spam()

if __name__ == "__main__":
    asyncio.run(main())
