# Papers

## Installation

```commandline
$ pip install papers
```

In addition, [ImageMagick](https://imagemagick.org/script/download.php) needs to be installed in order to generate PDF previews. Note that you may need to grant [special permissions for ImageMagick to read PDF files on Linux](https://cromwell-intl.com/open-source/pdf-not-authorized.html).


## Usage

Import papers from arXiv from an identifier, or import PDFs from URLs:
```commandline
$ papers-import arxiv ID
$ papers-import pdf URL --title ...
```

See `papers-import --help` for full list of options, e.g., how to specify the path of the folder containing papers.

Papers can be exported bib-files, a single citation, or a website containing the full index:

```
$ papers-export bib
$ papers-export cite CITEKEY
$ papers-export web
```

See `papers-export --help` for fill list of options.


## Demo

![Screenshot](https://raw.githubusercontent.com/jan-matthis/papers/master/screenshot.png)

[Demo of the web UI](https://papers-demo.netlify.app)/.


## Credits

PDF previews inspired by [Andrej Karpathy's Arxiv Sanity Preserver](http://www.arxiv-sanity.com/). Favicon by [fibo junior](https://thenounproject.com/term/literature/2273532/) under [CCBY](https://creativecommons.org/licenses/by/3.0/us/legalcode).


## License

MIT
