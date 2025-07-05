import json
import logging
import shlex

from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")

        # Jika input string kosong, langsung tolak
        if not string_datamasuk.strip():
            return json.dumps(dict(status='ERROR', data='input kosong'))

        # Coba baca sebagai JSON dulu
        try:
            data = json.loads(string_datamasuk)
            command = data.get("command", "").lower()
            params = data.get("params", [])
            if hasattr(self.file, command):
                method = getattr(self.file, command)
                result = method(params)
                return json.dumps(result)
            else:
                return json.dumps(dict(status='ERROR', data='perintah tidak dikenali'))
        except json.JSONDecodeError:
            # Jika bukan JSON, coba parsing manual sebagai plain string (contoh: UPLOAD)
            pass

        # Tangani format: COMMAND arg1 arg2 ...
        try:
            parts = shlex.split(string_datamasuk)
            if not parts:
                return json.dumps(dict(status='ERROR', data='perintah kosong'))

            command = parts[0].lower()
            params = parts[1:]

            if hasattr(self.file, command):
                method = getattr(self.file, command)
                result = method(params)
                return json.dumps(result)
            else:
                return json.dumps(dict(status='ERROR', data='perintah tidak dikenali'))

        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))

if __name__ == '__main__':
    fp = FileProtocol()
    contoh_list = json.dumps({"command": "list", "params": []})
    print(fp.proses_string(contoh_list))
