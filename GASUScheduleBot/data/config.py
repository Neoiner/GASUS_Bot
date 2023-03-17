import pytz
from environs import Env

env = Env()
env.read_env()


# Bot credentials
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")


# Postgres credentials
PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
DATABASE = env.str("DATABASE")
POSTGRES_IP = env.str("PG_IP")
POSTGRES_PORT = 5432
POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{DATABASE}"


# Redis credentials
REDIS_IP = env.str("REDIS_IP")

# Timezone
TIMEZONE = pytz.timezone(env.str("TIMEZONE"))
