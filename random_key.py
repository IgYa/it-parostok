from secrets import token_bytes
from base64 import b64encode


# генеруємо ключ для створення токену,
# та копіюємо його до файлу .env, поле AUTH_KEY=
print(b64encode(token_bytes(32)).decode())