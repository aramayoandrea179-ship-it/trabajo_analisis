import os
import asyncio
from flask import Flask, render_template, request, jsonify
from telegram import Bot

# 🔑 Credenciales desde variables de entorno
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

# --- NUEVOS ENDPOINTS ---
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

if __name__ == "__main__":
    # Para pruebas locales
    app.run(debug=True, host="0.0.0.0", port=5000)
