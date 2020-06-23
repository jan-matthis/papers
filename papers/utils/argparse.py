import argparse


class _HelpAction(argparse._HelpAction):
    # https://stackoverflow.com/a/24122778

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        print("\n")

        subparsers_actions = [
            action
            for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        ]

        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                # print("\nmode: '{}'".format(choice))
                print(subparser.format_help())
                print("\n")

        parser.exit()
