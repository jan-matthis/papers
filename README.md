# Papers

Simple reference manager in Python. Uses folders instead of a database. Bibliographic information is stored in bibtex. Generates a website to browse papers.


## Installation

```commandline
$ pip install papers
```

In addition, [ImageMagick](https://imagemagick.org/script/download.php) needs to be installed in order to generate PDF previews. Note that you may need to grant [special permissions for ImageMagick to read PDF files on Linux](https://cromwell-intl.com/open-source/pdf-not-authorized.html).


## Usage

Import papers from arXiv from an identifier, or import PDFs from URLs:
```commandline
$ papers-import --path ~/Papers arxiv ID
$ papers-import --path ~/Papers pdf URL --title ...
```

See `papers-import --help` for full list of options.

The bibliography can be exported to a bib-file, or a website containing the full index:

```
$ papers-export --path ~/Papers bib
$ papers-export --path ~/Papers web
```

See `papers-export --help` for full list of options.


## Demo

[![Screenshot](https://raw.githubusercontent.com/jan-matthis/papers/master/screenshot.png)](https://papers-demo.netlify.app)


## Credits

PDF previews inspired by [Andrej Karpathy's Arxiv Sanity Preserver](http://www.arxiv-sanity.com/). Favicon by [fibo junior](https://thenounproject.com/term/literature/2273532/) under [CCBY](https://creativecommons.org/licenses/by/3.0/us/legalcode).


## License

MIT
