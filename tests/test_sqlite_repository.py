import os

from src.storage.sqlite_repository import SQLiteUserRepository


def test_register_and_get_user(tmp_path):
    db_path = tmp_path / "chatbot.sqlite3"
    repo = SQLiteUserRepository(str(db_path))

    user = repo.register_user("demo_user", name="Demo User")
    stored = repo.get_user("demo_user")

    assert user["user_id"] == "demo_user"
    assert stored["name"] == "Demo User"

    repo.record_interaction("demo_user", {"type": "ask", "question": "Necesito ayuda"})
    history = repo.get_user_history("demo_user")

    assert history[-1]["type"] == "ask"
    assert history[-1]["question"] == "Necesito ayuda"

    repo.close()
    assert os.path.exists(db_path)
