from environs import Env

env = Env()
env.read_env()


# Postgres credentials
PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
DATABASE = env.str("DATABASE")
HOST = env.str("HOST")