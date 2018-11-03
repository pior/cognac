import abc
import argparse
import sys
from typing import Type, Sequence, List

from .command import BaseCommand, CommandFunc
from .context import Context
from .error import Error


class BaseWrapper(abc.ABC):

    @abc.abstractmethod
    def __init__(self, next_func: CommandFunc) -> None:
        pass

    @abc.abstractmethod
    def run(self, context: Context, args: argparse.Namespace) -> None:
        raise NotImplementedError()


class Wrapper(BaseWrapper):

    def __init__(self, next_func: CommandFunc) -> None:
        self._next_func = next_func


class ErrorHandlerWrapper(Wrapper):

    def run(self, context: Context, args: argparse.Namespace) -> None:
        try:
            self._next_func(context, args)
        except KeyboardInterrupt:
            context.write_output('')
        except Error as err:
            sys.exit(f'Error: {err}')


class Runner:

    def __init__(self, command_class: Type[BaseCommand], wrapper_classes: List[Type[BaseWrapper]]) -> None:
        self.__command_class = command_class
        self.__wrapper_classes = wrapper_classes

    def __call__(self) -> None:
        """This is the main function, usually defined as console-script."""

        context = Context.from_environment()

        command = self.__command_class()

        parser = argparse.ArgumentParser(description=command.description())
        command.setup_arguments(parser)
        args = parser.parse_args()

        func: CommandFunc = command.run
        for wrapper_class in self.__wrapper_classes + [ErrorHandlerWrapper]:
            func = wrapper_class(func).run

        func(context, args)


def build(command_class: Type[BaseCommand], wrappers: Sequence[Type[BaseWrapper]] = None) -> Runner:
    wrappers = [] if wrappers is None else list(wrappers)
    return Runner(command_class, wrappers)
