[![PyPI version](https://badge.fury.io/py/papers.svg)](https://badge.fury.io/py/papers)
[![GitHub license](https://img.shields.io/github/license/jan-matthis/papers)](https://github.com/jan-matthis/papers/blob/master/LICENSE)

# Papers

Simple reference manager in Python. Uses folders instead of a database, storing bibliographic information in bibtex. Generates a website to browse papers.


## Demo

Website generated from bibliography stored in `demo/`:

[![Screenshot](https://raw.githubusercontent.com/jan-matthis/papers/master/screenshot.png)](https://papers-demo.netlify.app)


## Installation

```commandline
$ pip install papers
```

In addition, [ImageMagick](https://imagemagick.org/script/download.php) needs to be installed in order to generate PDF previews. Note that you may need to grant [special permissions for ImageMagick to read PDF files on Linux](https://cromwell-intl.com/open-source/pdf-not-authorized.html).


## Usage

Import papers from arXiv using an identifier, or import PDFs using URLs:
```commandline
$ papers-import --path ~/Papers arxiv ID
$ papers-import --path ~/Papers pdf URL --title ...
```

See `papers-import --help` for full list of options.

The bibliography can be exported to a single bib-file, or a website containing the full index:

```
$ papers-export --path ~/Papers bib
$ papers-export --path ~/Papers web
```

See `papers-export --help` for full list of options.


## Credits

Previews inspired by [Andrej Karpathy's Arxiv Sanity Preserver](http://www.arxiv-sanity.com/).


## License

MIT
