import argparse
from pathlib import Path

from papers.papers import (
    export_bib,
    export_citation,
    export_web,
    import_arxiv,
    import_url_pdf,
)
from papers.utils.argparse import _HelpAction
import sys
from papers.utils.debug import pdb_hook


def cli_export():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="papers", 
        description="Export papers",
        add_help=False
    )
    parser.add_argument(
        "--path", 
        type=str, 
        default="~/Papers", 
        help="Path to papers"
    )
    parser.add_argument(
        "-h", "--help", 
        action=_HelpAction, 
        help="Usage info"
    )

    subparsers = parser.add_subparsers(dest="task")
    subparsers.required = True

    parser_bib = subparsers.add_parser(
        "bib", 
        description="Export references to .bib file", 
        add_help=False
    )
    parser_bib.add_argument(
        "--output",
        type=str,
        default="~/Papers/library.bib",
        help="Destination of output bibtex",
    )
    parser_bib.add_argument(
        "--aux",
        type=str,
        default=None,
        help="If specified, only citations appearing in .aux file will be exported",
    )
    parser_bib.set_defaults(func=export_bib)

    parser_cite = subparsers.add_parser(
        "cite", 
        description="Export single citation",
        add_help=False
    )
    parser_cite.add_argument(
        "key",
        type=str,
        help="Citation key",
    )
    parser_cite.add_argument(
        "--style",
        type=str,
        default="plain",
        help="Citation style",
    )
    parser_cite.set_defaults(func=export_citation)

    parser_web = subparsers.add_parser(
        "web", 
        description="Export references to website. Will create `index.html` and `index.bib` in `--path`.", 
        add_help=False
    )
    parser_web.add_argument(
        "--inline", 
        dest="inline", 
        action="store_true",
        help="Inline preview images"
    )
    parser_web.add_argument(
        "--no-inline", 
        dest="inline", 
        action="store_false",
        help="Do not inline preview images"
    )
    parser_web.set_defaults(inline=False)
    parser_web.set_defaults(func=export_web)
    # fmt: on

    sys.excepthook = pdb_hook

    args, unknownargs = parser.parse_known_args()
    args.unknownargs = unknownargs

    args.func(**vars(args))


def cli_import():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="papers", 
        description="Import papers",
        add_help=False
    )
    parser.add_argument(
        "--path", 
        type=str, 
        default="~/Papers", 
        help="Path to papers"
    )
    parser.add_argument(
        "-h", "--help", 
        action=_HelpAction, 
        help="Usage info"
    )

    subparsers = parser.add_subparsers(dest="task")
    subparsers.required = True

    parser_arxiv = subparsers.add_parser(
        "arxiv", 
        description="Import paper from arXiv", 
        add_help=False
    )
    parser_arxiv.add_argument(
        "arxiv_id", 
        type=str, 
        help="arXiv ID"
    )
    parser_arxiv.add_argument(
        "--tags", type=str, default=None, help="Tags separated by comma"
    )
    parser_arxiv.set_defaults(func=import_arxiv)

    parser_url_pdf = subparsers.add_parser(
        "pdf", 
        description="Import using URL to PDF.",
        add_help=False
    )
    parser_url_pdf.add_argument(
        "url", 
        type=str, 
        help="URL to PDF"
    )
    parser_url_pdf.add_argument(
        "--author",
        type=str,
        required=True,
        help="Author(s), formatted as firstname lastname, separated by comma",
    )
    parser_url_pdf.add_argument(
        "--year", 
        type=str, 
        required=True, 
        help="Year"
    )
    parser_url_pdf.add_argument(
        "--title", 
        type=str, 
        required=True, 
        help="Title"
    )
    parser_url_pdf.add_argument(
        "--journal", 
        type=str, 
        required=True, 
        help="Journal"
    )
    parser_url_pdf.add_argument(
        "--tags", 
        type=str, 
        default=None, 
        help="Tags separated by comma"
    )
    parser_url_pdf.set_defaults(func=import_url_pdf)
    # fmt: on

    sys.excepthook = pdb_hook

    args, unknownargs = parser.parse_known_args()
    args.unknownargs = unknownargs

    args.func(**vars(args))
