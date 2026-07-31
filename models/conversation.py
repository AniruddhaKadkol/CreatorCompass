from datetime import datetime
import uuid

from services.history_service import HistoryService


class Conversation:

    PREVIEW_LENGTH = 45

    def __init__(self, filename):

        self.filename = filename

        self.messages = HistoryService.load(filename)

    # =====================================================
    # ADD MESSAGE
    # =====================================================

    def add_message(self, role, content):

        role = role.strip()
        content = content.strip()

        if not role or not content:
            return

        message = {

            "id": str(uuid.uuid4()),

            "role": role,

            "content": content,

            "time": datetime.now().strftime("%d %b %Y • %I:%M %p")

        }

        self.messages.append(message)

        HistoryService.save(

            self.filename,

            self.messages

        )

    # =====================================================
    # GET MESSAGES
    # =====================================================

    def get_messages(self):

        return self.messages.copy()

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.messages = []

        HistoryService.save(

            self.filename,

            self.messages

        )

    # =====================================================
    # TIMELINE
    # =====================================================

    def get_timeline(self):

        timeline = []

        for message in self.messages:

            if message["role"] != "user":
                continue

            title = message["content"].strip()

            # Remove extra spaces/newlines
            title = " ".join(title.split())

            # Shorten long titles
            if len(title) > self.PREVIEW_LENGTH:

                title = title[:self.PREVIEW_LENGTH - 3] + "..."

            timeline.append({

                "id": message["id"],

                "time": message["time"],

                "title": title

            })

        return timeline