import logging

from the_world_after.utils.logs import init_logger

from .bot import run_bot
from .settings import settings

init_logger(settings.LOG_CONFIG)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    run_bot()
