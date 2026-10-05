import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test_safecore.db"

from src.database import Base
from src.models import Incident  # noqa: F401
from src.models import Area, HazardCatalog, IPERRecord, Personnel, Plant  # noqa: F401


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///./test_safecore_tmp.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()
        Path("test_safecore_tmp.db").unlink(missing_ok=True)
