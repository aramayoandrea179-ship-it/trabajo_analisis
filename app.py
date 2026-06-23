import asyncio
import threading
from flask import Flask, render_template, request, jsonify
from telegram import Bot
from telegram.ext import Application, CommandHandler

# 🔑 Credenciales de tu bot
TOKEN = "8714287310:AAHxSBhNi2J8Jy_wLFb4k2y3jKbuNR4InRk"
CHAT_ID = "7091936081"

# --- Flask App ---
app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/factura", methods=["POST"])
def factura():
    data = request.json
    mensaje = (
        "📄 SOLICITUD DE FACTURA\n\n"
        f"Nombre: {data['nombre']}\n"
        f"NIT: {data['nit']}\n"
        f"Monto: Bs. {data['monto']}"
    )
    try:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=mensaje))
        return jsonify({"ok": True, "mensaje": "Factura enviada"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

@app.route("/soporte", methods=["POST"])
def soporte():
    data = request.json
    mensaje = (
        "💬 NUEVO MENSAJE DE SOPORTE\n\n"
        f"Cliente: {data['nombre']}\n\n"
        f"Consulta:\n{data['mensaje']}"
    )
    try:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=mensaje))
        return jsonify({"ok": True, "respuesta": "Gracias por contactarnos. Un operador revisará su consulta."})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

@app.route("/calificacion", methods=["POST"])
def calificacion():
    data = request.json
    mensaje = (
        "⭐ NUEVA CALIFICACIÓN\n\n"
        f"Puntuación: {data['calificacion']} estrellas\n\n"
        f"Comentario:\n{data['comentario']}"
    )
    try:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=mensaje))
        return jsonify({"ok": True})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

# --- Nuevos Endpoints ---
@app.route("/imagen", methods=["POST"])
def enviar_imagen():
    data = request.json
    try:
        asyncio.run(bot.send_photo(chat_id=CHAT_ID, photo=data["url"]))
        return jsonify({"ok": True, "mensaje": "Imagen enviada"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

@app.route("/documento", methods=["POST"])
def enviar_documento():
    data = request.json
    try:
        asyncio.run(bot.send_document(chat_id=CHAT_ID, document=data["url"]))
        return jsonify({"ok": True, "mensaje": "Documento enviado"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

@app.route("/audio", methods=["POST"])
def enviar_audio():
    data = request.json
    try:
        asyncio.run(bot.send_audio(chat_id=CHAT_ID, audio=data["url"]))
        return jsonify({"ok": True, "mensaje": "Audio enviado"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

@app.route("/ubicacion", methods=["POST"])
def enviar_ubicacion():
    data = request.json
    try:
        asyncio.run(bot.send_location(chat_id=CHAT_ID, latitude=data["lat"], longitude=data["lon"]))
        return jsonify({"ok": True, "mensaje": "Ubicación enviada"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"ok": False})

# --- Telegram Bot con comandos ---
def run_telegram_bot():
    app_bot = Application.builder().token(TOKEN).build()

    async def start(update, context):
        await update.message.reply_text("👋 Hola, soy tu bot de soporte. Usa /help para ver opciones.")

    async def help_command(update, context):
        await update.message.reply_text(
            "📌 Comandos disponibles:\n"
            "/start - Iniciar conversación\n"
            "/help - Ver ayuda\n"
            "/ubicacion - Enviar ubicación\n"
            "/soporte - Contactar soporte"
        )

    async def ubicacion(update, context):
        await update.message.reply_location(latitude=-17.9647, longitude=-67.1060)

    async def soporte(update, context):
        await update.message.reply_text("💬 Escribe tu consulta y un operador te responderá.")

    # Registrar comandos
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_command))
    app_bot.add_handler(CommandHandler("ubicacion", ubicacion))
    app_bot.add_handler(CommandHandler("soporte", soporte))

    print("🤖 Bot escuchando en Telegram...")
    app_bot.run_polling()

# --- Ejecutar Flask y Bot en paralelo ---
if __name__ == "__main__":
    # Hilo para el bot de Telegram
    threading.Thread(target=run_telegram_bot, daemon=True).start()

    # Flask App
    app.run(debug=True, host="0.0.0.0", port=5000)