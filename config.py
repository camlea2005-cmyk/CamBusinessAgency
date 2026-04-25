from pathlib import Path

APP_NAME = "Caisse Boutique CI V1"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "caisse_boutique_ci_v1.db"

THEME_MODE = "light"
COLOR_THEME = "blue"

DATA_DIR.mkdir(parents=True, exist_ok=True)
