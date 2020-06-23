import datetime
import os
from collections import OrderedDict
from pathlib import Path

import markdown2
from pybtex.database import BibliographyData
from unidecode import unidecode


def clean_folder_bib(folder, bib_data):
    bib = {}
    tags = []

    citekey = make_citekey(
        lastname_first_author=bib_data.persons["author"][0].last_names[0].lower(),
        year=bib_data.fields["year"],
        title=bib_data.fields["title"],
    )

    bib[citekey] = bib_data

    date_added = datetime.datetime.fromtimestamp(folder.stat().st_ctime).strftime(
        "%Y-%m-%d  %H:%M"
    )

    ext = "[!_]*.pdf"
    pdfs = list(folder.rglob(ext))
    pdf = None
    if len(pdfs) == 1:
        pdf = pdfs[0]
    elif "paper.pdf" in pdfs:
        pdf = "paper.pdf"
    elif len(pdfs) > 1:
        ext = format_lastname_first_author(bib_data.persons["author"][0].last_names[0])
        pdfs = list(folder.rglob(ext + "*.pdf"))
        if len(pdfs) == 1:
            pdf = pdfs[0]
        else:
            print(f"PDF filename was ambigious for {citekey}")

    if pdf is not None:
        dst = Path(folder / f"{citekey}.pdf")
        os.rename(src=str(Path(folder / pdf)), dst=str(dst))
        date_added = datetime.datetime.fromtimestamp(dst.stat().st_ctime).strftime(
            "%Y-%m-%d %H:%M"
        )

    new_folder = Path(folder.parent / f"{citekey}")
    os.rename(src=str(Path(folder)), dst=str(new_folder))

    paper_path = new_folder / f"{citekey}.pdf"
    if paper_path.exists():
        bib[citekey].fields["file"] = "file://" + str(paper_path)

    abstract_path = new_folder / "abstract.txt"
    if abstract_path.exists():
        bib[citekey].fields["summary"] = abstract_path.read_text()

    notes_path = new_folder / "notes.md"
    if notes_path.exists():
        bib[citekey].fields["note"] = markdown2.markdown(
            notes_path.read_text().replace("./", "./" + citekey + "/"),
            extras=["cuddled-lists", "nofollow"],
        )

    for tag in new_folder.rglob("#*"):
        tags.append(tag.name[1:])
    bib[citekey].fields["keywords"] = ",".join(tags)

    bib[citekey].fields["date-added"] = date_added

    # Write bibfile
    write_bibtex(bib, Path(new_folder / f"{citekey}.bib"))

    # Remove old bibfiles
    for bibfile in new_folder.rglob("*.bib"):
        if str(bibfile.name) != f"{citekey}.bib":
            os.remove(str(new_folder / bibfile.name))

    return bib[citekey], citekey


def format_lastname_first_author(lastname_first_author):
    return str(unidecode(lastname_first_author.replace("-","").lower()))


def make_citekey(lastname_first_author, year, title):
    lastname_first_author = format_lastname_first_author(lastname_first_author)
    year = year
    title_word = ""
    not_first_word = [
        "a",
        "about",
        "an",
        "are",
        "at",
        #"can",
        #"do",
        "is",
        "how",
        "on",
        "the",
        "why",
        "where",
        "when",
        "whether",
        "what",
        "which",
        "who",
    ]
    for word in title.lower().replace("-", " ").replace(":", " ").replace(",", " ").split(" "):
        if word in not_first_word:
            continue
        else:
            title_word = word
            break
    return f"{lastname_first_author}{year}{title_word}"


def write_bibtex(bib, output):
    bib_sorted = OrderedDict(sorted(bib.items()))
    with open(output, "w+") as f:
        f.write(
            BibliographyData(bib_sorted)
            .lower()
            .to_string("bibtex")
            .replace("\\_", "_")
            .replace("\\&", "&")
        )
    return output
