# Elaine

Electronic Library Artificial Intelligence Networked Entity

Elaine is a text based conversational interface to the Beyond Social wiki. Elaine runs on her own infrastructure: a Raspberry Pi, a EPSON thermal printer and a Canon laserprinter, while being embedded in the WdKA's network.

# Requirements
## Beyond Social Shadow Library
* [BS Shadow Library](https://beyond-social.org/BS-Shadow-Library/) (zip file, 345MB) should be placed in `../`. The folder should be named `BS-Shadow-Library`.

## Software
* poppler-utils
* [pandoc](https://pandoc.org/) version? -- on the pi: use apt to install
* texlive-xetex (install TeX Live via net install, see <https://github.com/wdka-publicationSt/print-kiosk-ii/issues/2>)
* pdfjam 
* pandoc

* python3 Libraries (via pip3)
  * bs4 (BeuatifulSoup)
  * nltk
  * ircutils3
  * pypandoc
  * mwclient
  * html5lib
  * pprint
  * pyyaml

You can use the requirement.txt file to install them all at the same time: 

`$ pip3 install -r requirements.txt --user`

Elaine runs directly from the pi. Before she can be started, you need to download the content from the Beyond Social wiki (all pages and all images) to the pi, and let Elaine interact with it from there.

* run scripts that fetch content from the Beyond Social wiki:
 
`$ python3 download-all-pages.py`

`$ python3 download-images.py`
  
* install printer
  * connect the thermal printer to the pi (USB)
  * connect the laster printer to the pi (USB)

# Run Elaine

To execute Elaine use `run.py`.

A conversation with Elaine follows 2 scenes:.

## Scene 1 - Questionnaire (metadata + topics)

Based on a questionnaire, you retrieve wiki articles. 
First Elaine asks you questions that are based on **metadata**. 
Then she asks you questions about **Frictionary topics**.

## Scene 2 - Shadow Library (IRC librarian chat)

# Scripts

An overview of all the files and a short description of what they do can be found in the file `Elaine-files.csv`.

# Bird eye perspective
In a bird perspective, the plan at the moment is to work on ...

* download all wiki content (using API requests)
  * Article Index
  * API content gathering

* conversational interface with Elaine 
  * scene 1 = chat bot (questionnaire)
    * design of wiki articles using **LaTEX**
    * design of an **annex** using (?)
  * scene 2 = irc chat (chat with online librarians)
    * merging PDFs with PDFJam

-----

[Beyond Social](https://beyond-social.org)


