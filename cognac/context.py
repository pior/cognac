import os
import sys
from typing import Mapping, Tuple, TextIO

_EnvironType = Mapping[str, str]
_ArgvType = Tuple[str, ...]


class Environ:

    def __init__(self, environ: _EnvironType) -> None:
        self.__environ = environ

    def get_all_string(self) -> _EnvironType:
        return dict(self.__environ)

    def get_string(self, name: str) -> str:
        return self.__environ[name]

    def get_int(self, name: str) -> int:
        return int(self.__environ[name])


# class BaseContext(Protocol):

#     def environ(self) -> Environ:
#         ...

#     def argv(self) -> _ArgvType:
#         ...

#     def commandline_name(self) -> str:
#         ...

#     def commandline_arguments(self) -> _ArgvType:
#         ...

#     def write_output(self, *strings: str) -> None:
#         ...


# class BaseContext:

#     @abc.abstractclassmethod
#     @classmethod
#     def from_environment(cls) -> 'BaseContext':
#         raise NotImplementedError()

#     @abc.abstractmethod
#     def environ(self) -> Environ:
#         raise NotImplementedError()

#     @abc.abstractmethod
#     def argv(self) -> _ArgvType:
#         raise NotImplementedError()

#     @abc.abstractmethod
#     def commandline_name(self) -> str:
#         raise NotImplementedError()

#     @abc.abstractmethod
#     def commandline_arguments(self) -> _ArgvType:
#         raise NotImplementedError()

#     @abc.abstractmethod
#     def write_output(self, *strings: str) -> None:
#         raise NotImplementedError()


class Context:

    @classmethod
    def from_environment(cls) -> 'Context':
        return cls(
            argv=tuple(sys.argv[:]),
            environ=Environ(os.environ.copy()),
            output_fd=sys.stdout,
        )

    def __init__(self, argv: _ArgvType, environ: Environ, output_fd: TextIO) -> None:
        self.__argv = argv
        self.__environ = environ
        self.__output_fd = output_fd

    def environ(self) -> Environ:
        return self.__environ

    def commandline_name(self) -> str:
        return self.__argv[0]

    def commandline_arguments(self) -> _ArgvType:
        return self.__argv[1:]

    def write_output(self, *strings: str) -> None:
        print(*strings, file=self.__output_fd)
        self.__output_fd.flush()
