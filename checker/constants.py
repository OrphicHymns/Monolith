MOJANG_AUTH = "https://authserver.mojang.com/authenticate"

JSON_POST_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.164 Safari/537.36 "
}
HTTP_HEADERS = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.164 Safari/537.36"
}
HTTPS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.164 Safari/537.36"
}

CONFIG = """[Monolith]
debug = true
"""


ASCII_TITLE = """ ███▄ ▄███▓ ▒█████   ███▄    █  ▒█████   ██▓     ██▓▄▄▄█████▓ ██░ ██ 
▓██▒▀█▀ ██▒▒██▒  ██▒ ██ ▀█   █ ▒██▒  ██▒▓██▒    ▓██▒▓  ██▒ ▓▒▓██░ ██▒
▓██    ▓██░▒██░  ██▒▓██  ▀█ ██▒▒██░  ██▒▒██░    ▒██▒▒ ▓██░ ▒░▒██▀▀██░
▒██    ▒██ ▒██   ██░▓██▒  ▐▌██▒▒██   ██░▒██░    ░██░░ ▓██▓ ░ ░▓█ ░██ 
▒██▒   ░██▒░ ████▓▒░▒██░   ▓██░░ ████▓▒░░██████▒░██░  ▒██▒ ░ ░▓█▒░██▓
░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░▓  ░░▓    ▒ ░░    ▒ ░░▒░▒
░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ░ ▒  ░ ▒ ░    ░     ▒ ░▒░ ░
░      ░   ░ ░ ░ ▒     ░   ░ ░ ░ ░ ░ ▒    ░ ░    ▒ ░  ░       ░  ░░ ░
       ░       ░ ░           ░     ░ ░      ░  ░ ░            ░  ░  ░
                                                                     """

COMBO_REG = ".+?@.+?\..+?:.+?"
