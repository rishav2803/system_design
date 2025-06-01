from abc import ABC, abstractmethod

from in_mem_db.command_registry import CommandRegistry
from in_mem_db.db import InMemDB

command_registry = CommandRegistry.get_instance()


class BaseCommand(ABC):
    @classmethod
    @abstractmethod
    def from_input(cls, args: list[str], db: InMemDB) -> "BaseCommand":
        pass

    @abstractmethod
    def execute(self):
        pass


@command_registry.register("SET")
class SetCommand(BaseCommand):
    def __init__(self, key, value, db_instance: InMemDB):
        self.key = key
        self.value = value
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if len(args) < 2:
            raise ValueError("SET requires key and value")
        value = " ".join(args[1:])
        return cls(args[0], value, db)

    def execute(self):
        # BEFORE SETTING WE WILL KEEP THE OLD SET COMMAND IN A STACK
        self.db_instance.undo_stack.append(
            SetCommand(self.key, self.value, self.db_instance)
        )
        self.db_instance.set(key=self.key, val=self.value)
        print(f"Inserted {self.key} in the DB")


@command_registry.register("GET")
class GetCommand(BaseCommand):
    def __init__(self, key, db_instance: InMemDB):
        self.key = key
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if len(args) != 1:
            raise ValueError("GET requires key")
        return cls(args[0], db)

    def execute(self):
        if self.key not in self.db_instance.db:
            raise ValueError(f"{self.key} not found")
        else:
            print(f"{self.key}: {self.db_instance.db[self.key]}")


@command_registry.register("LIST")
class ListCommand(BaseCommand):
    def __init__(self, db_instance: InMemDB):
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if len(args) != 0:
            raise ValueError("LIST takes no arguments")
        return cls(db)

    def execute(self):
        for key, val in self.db_instance.db.items():
            print(f"{key}: {val}")


@command_registry.register("BEGIN")
class BeginCommand(BaseCommand):
    def __init__(self, db_instance: InMemDB):
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if args:
            raise ValueError("BEGIN takes no arguments")
        return cls(db)

    def execute(self):
        self.db_instance.begin()


@command_registry.register("ROLLBACK")
class RollbackCommand(BaseCommand):
    def __init__(self, db_instance: InMemDB):
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if args:
            raise ValueError("ROLLBACK takes no arguments")
        return cls(db)

    def execute(self):
        self.db_instance.rollback()


@command_registry.register("COMMIT")
class CommitCommand(BaseCommand):
    def __init__(self, db_instance: InMemDB):
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if args:
            raise ValueError("COMMIT takes no arguments")
        return cls(db)

    def execute(self):
        self.db_instance.commit()


@command_registry.register("UNDO")
class UndoCommand(BaseCommand):
    def __init__(self, db_instance: InMemDB):
        self.db_instance = db_instance

    @classmethod
    def from_input(cls, args, db):
        if args:
            raise ValueError("UNDO takes no arguments")
        return cls(db)

    def execute(self):
        if not self.db_instance.undo_stack:
            print("Nothing to UNDO")
            return

        cmd_to_undo = self.db_instance.undo_stack.pop()
        print(f"Undoing: {type(cmd_to_undo).__name__}")
        cmd_to_undo.execute()
