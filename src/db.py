import os
from sqlalchemy import create_engine


def get_engine():
    """
    Creates and returns a SQLAlchemy engine
    using environment variables.
    """
    user = os.getenv("NOMAD_DB_USER")
    password = os.getenv("NOMAD_DB_PASSWORD")
    host = os.getenv("NOMAD_DB_HOST")
    port = os.getenv("NOMAD_DB_PORT")
    db = os.getenv("NOMAD_DB_NAME")

    if not all([user, password, host, port, db]):
        raise ValueError("❌ Missing one or more DB environment variables")

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    )

    return engine
