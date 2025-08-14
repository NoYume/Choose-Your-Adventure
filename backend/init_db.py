from db.database import create_tables
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Creating database tables...")
        create_tables()
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise


if __name__ == "__main__":
    main()
