from app.database.base import Base


def test_database_metadata_uses_predictable_constraint_names() -> None:
    convention = Base.metadata.naming_convention

    assert convention is not None
    assert convention["pk"] == "pk_%(table_name)s"
    assert convention["fk"].startswith("fk_")
