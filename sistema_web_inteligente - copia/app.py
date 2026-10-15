
from flask import Flask, render_template, request, jsonify
import requests

# 3. Crear la aplicación web
app = Flask(__name__)


# 4. Mostrar la página principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobreNosotros.html")
def sobre_nosotros():
    return render_template("sobreNosotros.html")


@app.route("/contacto.html")
def contacto():
    return render_template("contacto.html")


@app.route("/api/status")
def api_status():
    try:
        respuesta = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        respuesta.raise_for_status()
    except requests.exceptions.RequestException:
        return jsonify({
            "en_linea": False,
            "estado": "Ollama no está disponible"
        }), 503

    return jsonify({
        "en_linea": True,
        "estado": "Ollama disponible"
    })

# 5. Recibir preguntas y consultar a la IA
@app.route("/api/chat", methods=["POST"])
def chat():
    datos_usuario = request.get_json(silent=True) or {}
    pregunta = datos_usuario.get("mensaje", "").strip()

    if not pregunta:
        return jsonify({"error": "Escribe una pregunta."}), 400

    try:
        respuesta = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:3b",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Eres Yanko AI, el asistente del portafolio "
                            "de Yanko. Responde en español, de forma "
                            "clara, amable y útil. Habla sobre el "
                            "proyecto y sus tecnologías cuando corresponda."
                        )
                    },
                    {
                        "role": "user",
                        "content": pregunta
                    }
                ],
                "stream": False
            },
            timeout=180
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

        return jsonify({
            "respuesta": datos["message"]["content"]
        })
    except requests.exceptions.ConnectionError:
        app.logger.exception("Ollama no está disponible")
        return jsonify({
            "error": "No se encuentra Ollama. Ábrelo e inténtalo de nuevo."
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "La IA tardó demasiado. Inténtalo de nuevo."
        }), 504
    except Exception:
        app.logger.exception("Error al consultar Ollama")
        return jsonify({
            "error": "No se pudo obtener una respuesta de la IA."
        }), 500


# 6. Iniciar el servidor local
if __name__ == "__main__":
    app.run(debug=True)
