import logging

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_message(message):
    """Helper function to log important messages during ETL process."""
    logger.info(message)
