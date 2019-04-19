# Elaine: Beyond Social Print-kiosk-ii

A text based conversational interface to the Beyond Social wiki, which returns a print publication for each user.

## Run
`./print-sequence.py`
* \# 1 - start questionnaire
	* calls `questionnaire()` from  `./questionnaire.py`
	* which create `articles_index`
* \# 2 - create a print-queue stored in `latex/queue.json` from the *articles_index* based on `articles_index` and `all_pages.json`
* \# 3 - produce the PDF
	* in tmp/queue.timestamp.pdf
	* by running queue2pdf() - **is breaking due to `--latex-engine has been removed.  Use --pdf-engine instead.`**
* \# 4 - prepare the Shadow Library PDF selection 
```
from irc import irc
irc("bs_user") #start the IRC chat
```
* \# 5 - resize pdf
	* requires `pdfjam` installed
* \# 6 Print squence
	* \# P1 - print questionnaire PDF 
	* \# P2 - print shadow library PDF 
	* \# P3 - print annex PDF 
* \# 7 receipt printer: cut


### questionnaire.py
Runs the questions asked to the user generate the Articles' index

The list of pages is shrinking depending on the answers given to each question

* \#1: Load pages index: all_pages.json
* \#2: Starts questionnaire

# TODO:
depending on pandoc version
when running queue2pdf()provide option: 
* `--latex-engine`
* `--pdf-engine` 