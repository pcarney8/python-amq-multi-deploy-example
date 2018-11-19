from argparse import ArgumentParser
from app import create_messenger, Messenger
from os import getenv
from proton.reactor import Container


def create_arg_parser():
    parser = ArgumentParser()

    parser.add_argument(
        '-b', '--broker-url',
        default=getenv('BROKER_URL', 'NOT_CONFIGURED'),
        help='the provider (default: env BROKER_URL or NOT_CONFIGURED)'
    )
    parser.add_argument(
        '-s', '--event-source',
        default=getenv('EVENT_SOURCE', 'NOT_CONFIGURED'),
        help=('the event destination '
              '(default: env EVENT_DESTINATION or pdr.discovered)')
    )
    parser.add_argument(
        '-d', '--event-destination',
        default=getenv('EVENT_DESTINATION', 'NOT_CONFIGURED'),
        help=('the event destination '
              '(default: env EVENT_DESTINATION or pdr.discovered)')
    )
    parser.add_argument(
        '-f', '--file-type',
        default=getenv('FILE_TYPE', 'SCIENCE'),
        help='the type of files to check in the granule (default: env FILE_TYPE or SCIENCE)'
    )

    return parser


def parse_args(parser, argv=None):
    if argv is None:
        return parser.parse_args()
    else:
        return parser.parse_args(argv)


def messenger_from_args(args):
    return create_messenger(
        args.broker_url,
        args.event_source,
        args.event_destination,
        args.file_type
    )


def main(argv=None):
    parser = create_arg_parser()
    args = parse_args(parser, argv=argv)
    messenger = messenger_from_args(args)
    Container(messenger).run()
