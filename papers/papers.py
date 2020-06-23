import argparse
import base64
import os
import re
import shutil
import sys
from distutils.dir_util import copy_tree
from glob import glob
from pathlib import Path

import jinja2.sandbox
import requests
from pybtex import PybtexEngine
from pybtex.database import BibliographyData, Entry, parse_file
from pybtex.database.input import bibtex

from papers.utils.arxiv import arxiv2dict
from papers.utils.bibtex import clean_folder_bib, make_citekey, write_bibtex
from papers.utils.formatters import (
    _author_fmt,
    _author_list,
    _extra_urls,
    _keyword_list,
    _main_url,
    _month_name,
    _sortkey,
    _title,
    _venue,
    _venue_type,
)
from papers.utils.imagemagick import preview


def export_bib(path="~/Papers", aux=None, output="index.bib", **kwargs):
    # Aux files
    if aux is not None:
        aux = Path(aux.replace("\\", "")).expanduser().absolute()
        txt = ""
        for match in glob(str(aux)):
            with open(match, "r") as f:
                txt += "\n" + f.read()
        regex = r"\\citation{(.*?)}"
        matches_presplit = re.findall(regex, txt)
        matches = [ms for match in matches_presplit for ms in match.split(",")]

    path = Path(path).expanduser().absolute()
    bib = {}
    ext = "*/*.bib"
    for i in path.rglob(ext):
        if "_" == str(i.parent.name)[0] or str(i.name) in ["index.bib", "library.bib"]:
            continue

        bib_data = parse_file(i)
        if len(bib_data.entries) != 1:
            print(
                "Skipping {} since bibtex contains more than one entry".format(i.name)
            )
            continue

        bib_data, citekey = clean_folder_bib(
            i.parent, bib_data.entries.items()[0][1]
        )

        if aux is not None:
            if citekey not in matches:
                continue
        else:
            bib[citekey] = bib_data

    output = Path(output).expanduser().absolute()
    return write_bibtex(bib, output)


def export_citation(key, path="~/Papers", style="plain", **kwargs):
    path = Path(path).expanduser().absolute()
    print(
        PybtexEngine().format_from_file(
            filename=path / Path(f"{key}/{key}.bib"),
            style=style,
            output_backend="text",
        )[4:]
    )


def export_web(path="~/Papers", inline=False, regenerate_all_previews=False, **kwargs):
    papers_path = Path(path).expanduser().absolute()

    # Get template
    tenv = jinja2.sandbox.SandboxedEnvironment()
    tenv.filters["author_fmt"] = _author_fmt
    tenv.filters["author_list"] = _author_list
    tenv.filters["keyword_list"] = _keyword_list
    tenv.filters["title"] = _title
    tenv.filters["venue_type"] = _venue_type
    tenv.filters["venue"] = _venue
    tenv.filters["main_url"] = _main_url
    tenv.filters["extra_urls"] = _extra_urls
    tenv.filters["monthname"] = _month_name
    template_path = Path(os.path.realpath(__file__)).parent / "templates/index.html"
    with open(template_path, "r+") as f:
        tmpl = tenv.from_string(f.read())

    # Make BibTeX file
    bibfile_path = export_bib(
        path=path,
        aux=None,
        output=papers_path / "index.bib",
    )

    # Parse the BibTeX file
    with open(bibfile_path, "r+") as f:
        db = bibtex.Parser().parse_stream(f)

    # Include the bibliography key in each entry
    for k, v in db.entries.items():
        v.fields["key"] = k

        paper_path = papers_path / f"{k}/{k}.pdf"
        preview_path = papers_path / f"{k}/preview.jpg"

        if paper_path.exists():
            if not preview_path.exists() or regenerate_all_previews:
                preview(fname_in=paper_path, fname_out=preview_path)

        if inline and preview_path.exists():
            v.fields["preview"] = base64.b64encode(
                open(preview_path, "rb").read()
            ).decode("ascii")

    # Render the template
    bib_sorted = sorted(db.entries.values(), key=_sortkey, reverse=True)
    out = tmpl.render(entries=bib_sorted)

    # Write contents (overrides index.html)
    Path(papers_path / "index.html").write_text(out)


def import_arxiv(arxiv_id=None, tags=None, path="~/Papers", path_tmp="/tmp/", **kwargs):
    assert arxiv_id is not None
    papers_path = Path(path).expanduser().absolute()

    new_folder = (
        Path(path_tmp).expanduser().absolute() / f"papers_import_arxiv_{arxiv_id}"
    )
    new_file = new_folder / Path(arxiv_id + ".arxiv")

    if not new_file.exists():
        new_file.parent.mkdir(exist_ok=True)
        new_file.touch()

    if tags != None:
        tags = tags.split(",")
        for tag in tags:
            path = Path(new_folder, "#" + tag.strip())
            if not path.exists():
                path.touch()

    # Get arxiv info
    info, xmldoc = arxiv2dict(arxiv_id)

    # Save xml
    xml = new_file.parent / (arxiv_id + ".arxiv")
    with open(xml, "w+") as f:
        f.write(xmldoc.toxml())

    # Cite key
    citekey = make_citekey(
        info["first_author_surname"].lower(), info["year"], info["title"]
    )

    # PDF
    pdf_name = citekey + ".pdf"
    files_pdf = list(new_file.parent.glob("*.pdf"))
    if len(files_pdf) == 0:  # get pdf
        response = requests.get(info["url_pdf"])
        with open(new_file.parent / pdf_name, "wb") as f:
            f.write(response.content)
    if len(files_pdf) == 1 and files_pdf[0] != pdf_name:
        files_pdf[0].rename(new_file.parent / pdf_name)

    # Write abstract.txt
    abstract = new_file.parent / "abstract.txt"
    with open(abstract, "w+") as f:
        f.write(info["abstract"].strip())

    # Bib entry
    ref_entry = {
        citekey: Entry(
            "article",
            [
                ("author", " and ".join(info["author"])),
                ("title", str(info["title"])),
                ("year", str(info["year"])),
                ("eprint", str(info["id"])),
                ("journal", "arXiv preprint"),
            ],
        ),
    }

    # Write bib file
    ref = new_file.parent / f"{citekey}.bib"
    with open(ref, "w+") as f:
        f.write(BibliographyData(ref_entry).to_string("bibtex"))

    # Rename parent folder according to citekey
    new_folder_renamed = Path(new_file.parent.parent / citekey)
    Path(new_file.parent).rename(new_folder_renamed)

    # Move folder
    shutil.move(str(new_folder_renamed), str(papers_path / citekey))


def import_url_pdf(
    url=None, author=None, year=None, title=None, journal=None, tags=None, path="~/Papers", **kwargs
):
    assert url is not None
    papers_path = Path(path).expanduser().absolute()

    authors = "".join([i for i in author if not i.isdigit()])
    author_string = ""
    author_parts = authors.split(",")
    for i, author in enumerate(author_parts):
        name_parts = [name_part.strip() for name_part in author.strip().split(" ")]
        author_string += name_parts[-1] + ","
        if i == 0:
            last_name = name_parts[-1].lower()
        for j in range(len(name_parts) - 1):
            author_string += " " + name_parts[j]
        if i < len(author_parts) - 1:
            author_string += " and "

    citekey = make_citekey(last_name, year, title)

    new_folder = papers_path / citekey
    new_folder.mkdir()

    bib_template = """@article{{{citekey},
    author    = "{author}",
    title     = "{title}",
    journal   = "{journal}",
    year      = "{year}",
    url       = "{url}"
}}
    """

    bib_contents = bib_template.format(
        citekey=citekey,
        url=url,
        author=author_string,
        title=title,
        year=year,
        journal=journal,
    )
    Path(new_folder / f"{citekey}.bib").write_text(bib_contents)
    
    response = requests.get(url)
    pdf_file = Path(new_folder, citekey + ".pdf")
    with open(pdf_file, "wb") as f:
        f.write(response.content)
    
    if tags != None:
        tags = tags.split(",")
        for tag in tags:
            path = Path(new_folder, "#" + tag.strip())
            if not path.exists():
                path.touch()
    
    print("Edit abstract.txt now:")
    print("vi {}".format(new_folder / "abstract.txt"))
