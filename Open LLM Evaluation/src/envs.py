import os

from huggingface_hub import HfApi

# Info to change for your repository
# ----------------------------------
TOKEN = os.environ.get("TOKEN") # A read/write token for your org

DEVICE = "cpu" # "cuda:0" if you add compute
LIMIT = None # !!!! Should be None for actual evaluations!!!
# ----------------------------------

OWNER = "openlifescienceai"
REPO_ID = f"{OWNER}/open_medical_llm_leaderboard"
QUEUE_REPO = f"{OWNER}/requests"
RESULTS_REPO = f"{OWNER}/results"


# If you setup a cache later, just change HF_HOME
CACHE_PATH=os.getenv("HF_HOME", ".")

# Local caches
EVAL_REQUESTS_PATH = os.path.join(CACHE_PATH, "eval-queue")
EVAL_RESULTS_PATH = os.path.join(CACHE_PATH, "eval-results")
EVAL_REQUESTS_PATH_BACKEND = os.path.join(CACHE_PATH, "eval-queue")
EVAL_RESULTS_PATH_BACKEND = os.path.join(CACHE_PATH, "eval-results")

API = HfApi(token=TOKEN)
