import json
import os
from json import JSONDecodeError
class HistoryService:
    DATA_FOLDER = "data"
    ENCODING = "utf-8"
    @classmethod
    def get_file_path(cls, filename):
        os.makedirs(
            cls.DATA_FOLDER,
            exist_ok=True
        )
        return os.path.join(
            cls.DATA_FOLDER,
            filename
        )
    @classmethod
    def load(cls, filename):
        file_path = cls.get_file_path(
            filename
        )
        if not os.path.exists(file_path):
            with open(
                file_path,
                "w",
                encoding=cls.ENCODING
            ) as file:
                json.dump(
                    [],
                    file,
                    indent=4
                )
            return []
        try:
            with open(
                file_path,
                "r",
                encoding=cls.ENCODING
            ) as file:
                history = json.load(file)
                if isinstance(
                    history,
                    list
                ):
                    return history
                return []
        except JSONDecodeError:
            return []
        except Exception:
            return []
    @classmethod
    def save(
        cls,
        filename,
        messages
    ):
        file_path = cls.get_file_path(
            filename
        )
        with open(
            file_path,
            "w",
            encoding=cls.ENCODING
        ) as file:
            json.dump(
                messages,
                file,
                indent=4,
                ensure_ascii=False
            )