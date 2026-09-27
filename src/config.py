from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT / os.getenv("DATABASE_PATH", "data/enterprise.db")
POLICY_PATH = ROOT / "data" / "policies.md"
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
TOP_K = int(os.getenv("TOP_K", "3"))
