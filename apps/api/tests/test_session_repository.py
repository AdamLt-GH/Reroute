from app.repositories.sessions import generate_session_token, hash_session_token


def test_session_tokens_are_random_and_store_only_a_hash() -> None:
    first = generate_session_token()
    second = generate_session_token()

    assert first != second
    assert len(first) >= 40
    assert hash_session_token(first) != first
    assert len(hash_session_token(first)) == 64


def test_session_token_hashing_is_consistent() -> None:
    token = "a test session token"

    assert hash_session_token(token) == hash_session_token(token)
