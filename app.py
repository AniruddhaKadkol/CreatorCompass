from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from models.conversation import Conversation
from services.ai_service import AIService


app = Flask(__name__)

# ==========================================================
# SERVICES
# ==========================================================

content_conversation = Conversation(
    "content_creator.json"
)

creative_conversation = Conversation(
    "creative_studio.json"
)

ai_service = AIService()

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# CONTENT CREATOR PAGE
# ==========================================================

@app.route("/content_creator")
def content_creator():

    return render_template(

        "content_creator.html",

        messages=content_conversation.get_messages(),

        timeline=content_conversation.get_timeline()

    )


# ==========================================================
# SEND CONTENT MESSAGE
# ==========================================================

@app.route(
    "/send_message",
    methods=["POST"]
)
def send_message():

    data = request.get_json()

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:

        return jsonify({

            "success": False,

            "error": "Message cannot be empty."

        })

    content_conversation.add_message(
        "user",
        message
    )

    ai_response = ai_service.content_creator(
        content_conversation.get_messages()
    )

    content_conversation.add_message(
        "assistant",
        ai_response
    )

    return jsonify({

        "success": True,

        "assistant": ai_response,

        "timeline": content_conversation.get_timeline()

    })


# ==========================================================
# CREATOR DASHBOARD
# ==========================================================

@app.route(
    "/analyze_content",
    methods=["POST"]
)
def analyze_content():

    data = request.get_json()

    content = data.get(
        "content",
        ""
    )

    dashboard = ai_service.analyze_content(
        content
    )

    return jsonify({

        "dashboard": dashboard

    })


# ==========================================================
# CREATIVE STUDIO PAGE
# ==========================================================

@app.route("/creative_studio")
def creative_studio():

    return render_template(

        "creative_studio.html",

        messages=creative_conversation.get_messages(),

        timeline=creative_conversation.get_timeline()

    )


# ==========================================================
# SEND CREATIVE STUDIO MESSAGE
# ==========================================================

@app.route(
    "/send_creative_message",
    methods=["POST"]
)
def send_creative_message():

    data = request.get_json()

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:

        return jsonify({

            "success": False,

            "error": "Message cannot be empty."

        })

    creative_conversation.add_message(
        "user",
        message
    )

    ai_response = ai_service.creative_studio(
        creative_conversation.get_messages()
    )

    creative_conversation.add_message(
        "assistant",
        ai_response
    )

    return jsonify({

        "success": True,

        "assistant": ai_response,

        "timeline": creative_conversation.get_timeline()

    })


# ==========================================================
# CLEAR CONTENT HISTORY
# ==========================================================

@app.route("/clear_content_history")
def clear_content_history():

    content_conversation.clear()

    return jsonify({

        "success": True

    })


# ==========================================================
# CLEAR CREATIVE STUDIO HISTORY
# ==========================================================

@app.route("/clear_creative_history")
def clear_creative_history():

    creative_conversation.clear()

    return jsonify({

        "success": True

    })


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )