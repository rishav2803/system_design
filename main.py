from in_mem_db.command_registry import CommandRegistry
from in_mem_db.db import InMemDB
import in_mem_db.command


def start_shell(db_instance: InMemDB, command_registry: CommandRegistry):
    while True:
        print("$ ", end="")
        input_line = input().strip()
        if not input_line:
            continue

        if input_line.upper() in {"QUIT", "EXIT"}:
            print("Exiting...")
            break

        parts = input_line.split()
        command = parts[0].strip().upper()

        try:
            cmd_cls = command_registry.create(command)
            command_instance = cmd_cls.from_input(parts[1:], db_instance)
            command_instance.execute()
        except ValueError as ve:
            print("Error:", ve)
            continue


if __name__ == "__main__":
    db_instance = InMemDB()

    command_registry = CommandRegistry.get_instance()
    start_shell(db_instance=db_instance, command_registry=command_registry)
