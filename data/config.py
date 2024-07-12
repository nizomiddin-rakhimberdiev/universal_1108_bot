from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# OPENAI_API_KEY = env.str("OPENAI_API_KEY")
REMOVE_BG = env.str("REMOVE_BG_API_KEY")
IP = env.str("ip")  # Xosting ip manzili
