# URL for awslambda/function.py
LAMBDA_URL: str = None

# GPIO connected to beam
LED_GPIO: int = 4

# Github repo
REPO: dict = dict(
    user="tbruno25",
    repo="micro-beam",
    branch="main",
    working_dir="src",
    files=["boot.py", "main.py", "beam.py"],
)
