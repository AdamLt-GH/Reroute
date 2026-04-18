from app.database.session import build_engine, build_session_factory


def test_database_session_factory_uses_the_async_postgres_engine() -> None:
    engine = build_engine("postgresql+asyncpg://reroute:reroute@localhost:5432/reroute")
    session_factory = build_session_factory(engine)

    assert engine.dialect.name == "postgresql"
    assert session_factory.kw["expire_on_commit"] is False
