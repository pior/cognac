#!/usr/bin/env python

import argparse

import cognac


class BugsnagWrapper(cognac.Wrapper):

    def run(self, context: cognac.Context, args: argparse.Namespace) -> None:
        # client = bugsnag.Client(...)

        try:
            self._next_func(context, args)
        except Exception as exc:
            print(f'Reporting an exception: {exc}')
            # client.notify(exc)
            raise


class Foo(cognac.Command):
    """This is my help description field. """

    def run(self, context: cognac.Context, args: argparse.Namespace) -> None:
        context.write_output('starting something...')
        raise cognac.Error('Oups!')


main = cognac.build(Foo, [BugsnagWrapper])


if __name__ == '__main__':
    main()
