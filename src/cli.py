"""CLI mínima para registro de usuarios e historial de uso."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.storage.sqlite_repository import SQLiteUserRepository


def _get_repository() -> SQLiteUserRepository:
    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "data" / "chatbot.sqlite3"
    return SQLiteUserRepository(str(db_path))


def cmd_register(args: argparse.Namespace) -> int:
    repo = _get_repository()
    user = repo.register_user(args.user_id, name=args.name, language_level=args.level)
    print(json.dumps(user, ensure_ascii=False, indent=2))
    repo.close()
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    repo = _get_repository()
    users = repo.list_users()
    print(json.dumps(users, ensure_ascii=False, indent=2))
    repo.close()
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    repo = _get_repository()
    payload = {"type": args.type, "message": args.message}
    if args.question:
        payload["question"] = args.question
    if args.answer:
        payload["answer"] = args.answer

    entry = repo.record_interaction(args.user_id, payload, event_type=args.type)
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    repo.close()
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    repo = _get_repository()
    history = repo.get_user_history(args.user_id, limit=args.limit)
    print(json.dumps(history, ensure_ascii=False, indent=2))
    repo.close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI mínima para chatbot bilingüe")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register = subparsers.add_parser("register", help="Registrar un usuario")
    register.add_argument("user_id")
    register.add_argument("--name", default="")
    register.add_argument("--level", default="A1")
    register.set_defaults(func=cmd_register)

    users = subparsers.add_parser("list-users", help="Listar usuarios")
    users.set_defaults(func=cmd_list)

    log = subparsers.add_parser("log", help="Registrar una interacción")
    log.add_argument("user_id")
    log.add_argument("--type", default="interaction")
    log.add_argument("--message", default="")
    log.add_argument("--question", default="")
    log.add_argument("--answer", default="")
    log.set_defaults(func=cmd_log)

    history = subparsers.add_parser("history", help="Mostrar historial del usuario")
    history.add_argument("user_id")
    history.add_argument("--limit", type=int, default=20)
    history.set_defaults(func=cmd_history)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
