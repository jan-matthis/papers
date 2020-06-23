import urllib.request
from xml.dom import minidom


def arxiv2dict(xid):
    usock = urllib.request.urlopen("http://export.arxiv.org/api/query?id_list=" + xid)
    xmldoc = minidom.parse(usock)
    usock.close()

    d = xmldoc.getElementsByTagName("entry")[0]

    date = d.getElementsByTagName("updated")[0].firstChild.data
    text_year = date[:4]

    title = d.getElementsByTagName("title")[0]
    text_title = title.firstChild.data

    authorlist = []
    first = True
    for person_name in d.getElementsByTagName("author"):
        name = person_name.getElementsByTagName("name")[0]
        text_name = name.firstChild.data
        text_given_name = " ".join(text_name.split()[:-1])
        text_surname = text_name.split()[-1]
        authorlist.append(text_surname + ", " + text_given_name)

        if first:
            text_first_author_surname = text_surname
            first = False

    summary = d.getElementsByTagName("summary")[0].firstChild.data

    for link in d.getElementsByTagName("link"):
        link_title = link.getAttribute("title")
        if link_title == "pdf":
            pdf_link = link.getAttribute("href")
        elif link_title == "":
            arxiv_link = link.getAttribute("href")

    info = {
        "title": text_title,
        "author": authorlist,
        "year": text_year,
        "id": xid,
        "first_author_surname": text_first_author_surname,
        "url_id": "http://www.arxiv.org/abs/" + xid,
        "url_xml": arxiv_link,
        "url_pdf": pdf_link,
        "abstract": summary,
    }

    return info, xmldoc
