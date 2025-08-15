import logging

from app.config.settings import settings


logging.basicConfig(
  level=settings.log_level,
  format="%(asctime)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d \
        [Th-%(thread)d] %(message)s"
)
logger = logging.getLogger(__name__)
