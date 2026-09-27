import os
import secrets
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Falta la variable de entorno BOT_TOKEN.")

def make_demo_result(user_input: str) -> str:
    # Datos deliberadamente ficticios y no utilizables como tarjetas de pago.
    demo_items = []
    for _ in range(8):
        demo_id = "TEST-" + secrets.token_hex(4).upper()
        month = secrets.randbelow(12) + 1
        year = datetime.now().year + secrets.randbelow(5) + 1
        demo_items.append(f"{demo_id} | {month:02d} | {year} | XXX")

    safe_input = user_input[:80].replace("\n", " ").strip() or "DEMO"

    return (
        "╔══════════「 ZeroTwoChk 」══════════╗\n"
        "║\n"
        f"♣ Input:\n{safe_input} | demo | demo | demo\n"
        "╚════════════「 TEST DATA 」══════════╝\n\n"
        + "\n".join(demo_items)
        + "\n\n"
        "╔════════════「 DETAILS 」════════════╗\n"
        "♣ Bank Information:\n"
        "DEMO BANK S.A.\n"
        "TEST CARD - NOT VALID\n"
        "ENVIRONMENT: SANDBOX\n"
        "╚════════════════════════════════════╝\n\n"
        "Generado por: ZeroTwoChk Safe Bot"
    )

def looks_like_payment_card(value: str) -> bool:
    # Rechaza entradas que parezcan números de tarjeta reales.
    digits = "".join(ch for ch in value if ch.isdigit())
    return 13 <= len(digits) <= 19

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bye.\n\n"
        "Comando disponible:\n"
        "/gen <texto>\n\n"
        "Este bot genera únicamente datos de prueba ficticios."
    )

async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args).strip()

    if not user_input:
        await update.message.reply_text(
            "Uso: /gen <texto>\n"
            "Ejemplo: /gen DEMO-123"
        )
        return

    if looks_like_payment_card(user_input):
        await update.message.reply_text(
            "No acepto números que parezcan tarjetas de pago. "
            "Usa un identificador de prueba, por ejemplo: /gen DEMO-123"
        )
        return

    await update.message.reply_text(make_demo_result(user_input))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen))

    print("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
