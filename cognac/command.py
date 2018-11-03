import abc
from typing import Optional, Callable

import argparse

from .context import Context

CommandFunc = Callable[[Context, argparse.Namespace], None]


class BaseCommand(abc.ABC):

    @abc.abstractmethod
    def __init__(self) -> None:
        """Initialize the command object."""
        raise NotImplementedError()

    @abc.abstractclassmethod
    def name(cls) -> str:
        """Return the name of this command."""
        raise NotImplementedError()

    @abc.abstractclassmethod
    def description(cls) -> Optional[str]:
        """Return the description of this command, used in the command help."""
        raise NotImplementedError()

    @abc.abstractclassmethod
    def setup_arguments(cls, parser: argparse.ArgumentParser) -> None:
        """Specify the arguments for this command on a prepared ArgumentParser."""
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self, context: Context, args: argparse.Namespace) -> None:
        """The command logic."""
        raise NotImplementedError()


class Command(BaseCommand):

    def __init__(self) -> None:
        pass

    @classmethod
    def name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def description(cls) -> Optional[str]:
        return cls.__doc__

    @classmethod
    def setup_arguments(cls, parser: argparse.ArgumentParser) -> None:
        """Make this method optional, for commands without arguments."""
        pass
