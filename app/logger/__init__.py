import logging
from configs.app import NAME
from configs.log import LEVEL

def setup_logger():
    file_path = f"./app/logs/{NAME}.log"
    logging.basicConfig(
        filename=file_path,
        # format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=LEVEL
    )
    # Set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging.getLogger(__name__)
