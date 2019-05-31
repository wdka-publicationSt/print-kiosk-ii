#!/usr/bin/env python3
import json
import os, re, subprocess
import pypandoc
from bs4 import BeautifulSoup
import datetime
from utility_scripts.functions import remove_wiki_elements, get_yaml_data



# * * * * * * * * * * * * * * * * * *
# queue.tmp.json > queue.tmp.html
#

# --- load all contributors
def load_all_contributors(data):
    print(data)
    f = open(data, 'r').read()
    data = json.loads(f)
    all_pages_contributors = []
    for page, _ in data.items():
        page_contributors = data[page]['contributors']
        for contributor in  page_contributors:
            all_pages_contributors.append(contributor)
    all_pages_contributors = sorted(list(set(all_pages_contributors)))
    return all_pages_contributors


# --- load print queue
def load_print_queue(data):
    print(data)
    f = open(data, 'r').read()
    queue = json.loads(f)
    #pprint(queue)
    return queue


# --- Pre-process the content html
def text_replacements(html):
    soup = BeautifulSoup(html, "html5lib")
    imgs = soup.find_all("img")
    for img in imgs:
        src = ((img['src'].split('/'))[-1])
        src = re.sub(r'^\d{1,3}px\-', '', src)
        img['src'] = 'images/'+ src 
    html = remove_wiki_elements(soup)

    with open('test-before.html', 'w') as tmp:
        tmp.write(html)
        tmp.close()
    
    html = re.sub(r'<span class="mw-editsection-bracket">\[</span>.*?edit.*?<span class="mw-editsection-bracket">]', '', html)
    html = re.sub(r'<span class=\"smw-highlighter\" .*?The wikipage input value is empty .*?</div></span>\n', '', html) # to remove the semantic mediawiki error that is displayed as content in some pages, which is caused by empty fields in the article forms.
    html = html.replace('[[File: | ]]', '') # to remove empty image tags
    html = re.sub(r'<table.*?</table>', '', html) # to remove tables from the print queue (unfortunately, \longtables give us the following error: "! Package longtable Error: longtable not in 1-column mode.")
    html = re.sub(r'width=".*?"', '', html) # to force images to template size - this is hacky, should perhaps be done with a html parser!
    html = re.sub(r'height=".*?"', '', html) # to force images to template size - this is hacky, should perhaps be done with a html parser!
    # to remove the TOC that is generated by the wiki
    html = html.replace('<div class="toc" id="toc"><div class="toctitle" id="toctitle"><h2>Contents</h2></div>', '')
    html = html.replace('id="contents"', '')

    html_out = []
    lines = html.split('\n')
    for line in lines:
        if 'toclevel' not in line: # hmm... bit ugly ?
            html_out.append(line)
    html = '\n'.join(html_out)

    with open('test-after.html', 'w') as tmp:
        tmp.write(html)
        tmp.close()

    return html

def base_header_shift(content):
    content_shifted_headers = pypandoc.convert_text(content, 'html', format='html', extra_args=['--base-header-level=2'])

    with open('test-after2.html', 'w') as tmp:
        tmp.write(content_shifted_headers)
        tmp.close()

    return content_shifted_headers

# --- Place content html in template, add information to the article from the all_pages.json
def get_article_template(title, contributors, categories, first_rev, first_rev_user, recent_rev, recent_rev_user, content):
    content = text_replacements(content)
    if len(categories) == 0:
        categories_string = 'Nobody categorized this page yet.'
    else:
        categories_string = ''
        for i, c in enumerate(categories):
            string = '<em>{}</em>'.format(c)
            if i == 0:
                categories_string = categories_string + string
            else:
                categories_string = categories_string + ' & ' + string

    template = '''<div class="article_wrapper">
        <h1 class="article_title">{}</h1>
        <div class="article_metadata">CONTRIBUTOR(s) {}</div>
        <hr>
        <div class="article_metadata">CATEGORIZED as {}</div>
        <hr>
        <div class="article_metadata">CREATED at {} by <em>{}</em></div>
        <hr>
        <div class="article_metadata">LAST EDITED at {} by <em>{}</em></div>
        <hr>
        <div class="article_content">{}</div>
    </div>'''.format(title, ' & '.join(contributors), categories_string, first_rev, first_rev_user, recent_rev, recent_rev_user, content)
    return template

# --- Write metadata file
def create_metadata_authors_string(authors):
    ''' authors = [] '''
    string = ''
    for author in authors:
        tmp = '- name: {}'.format(author)
        string = string +'\n'+ tmp
    return string
    # print(string)

def create_metadata_file(metadata_filename, authors):
    ''' authors = [] '''
    ''' categories = [] '''
    authors_string = create_metadata_authors_string(authors)
    metadata = '''---
title: PRINT KIOSK II
subtitle: 
author:
{}
abstract: ................................................................................................... PRINT KIOSK II - A semi-automated publishing performance of content that digests itself. The material uploaded on Beyond Social—an information repository generated by students, teachers, and the extended network of the WdKA Social Practices—was first re-read and then digested by humans and machines, through programming scripts and in conversations between faculty and alumni. Their idea was to understand how the department's pedagogy has made itself public on Beyond Social for the last four years. Simultaneously, a network of conversation between machines and humans--their roles sometimes confused by a Wizard of Oz method--produces a printed digest of content that previously existed on Beyond Social and its Shadow Library. These digests are allegedly personalized according to the interests of each visitor. Rather than conceive of "writing" a new publication by commissioning new material, this iteration of Print Kiosk prefers to reassemble what is already there, acknowledging the value of what came before whilst knowing that what came before needs retooling. Pedagogy is positioned as a building of knowledge that requires reassembling, re-understanding, rejecting, and/or rediscovering its own positions, in a process of renewal. ELAINE (Electronic Library Artificial Intelligence Networked Entity) An artificially artificial intelligence; a cyborg librarian; a budding xenofeminist whose aspirations are in peer-review with Catherine Somzé; an accidental homage to Elaine de Kooning; modeled after and in collaboration with Elaine W. Ho (Display Distribute); performed and developed collectively by humans at WdKA Social Practices; borrowing some infrastructure from Piet Zwart Institute and WdKA Publication Station; through servers maintained by the WdKA ICT department.'''.format(authors_string)
    out = open(metadata_filename, 'w+')
    out.write(metadata)
    out.close()
    print('*{} written*'.format(metadata_filename))

# --- write queue to html
def queue2html(queue, html_filename):
    queue_html = ''
    keywords = []
    for page, _ in queue.items():
        if '<table>' not in queue[page]['text']: # the tables make the latex generation break, so unfortunately we filter pages that use a table out...
            # collect content
            title = queue[page]['title']
            contributors = queue[page]['contributors']
            categories = queue[page]['categories']
            first_rev_values = queue[page]['revisions']['first_revision_time']
            first_rev = '{} {} {}, {}:{}h'.format(first_rev_values[2], datetime.date(first_rev_values[0], first_rev_values[1], 1).strftime('%B'), first_rev_values[0], first_rev_values[3], first_rev_values[4])
            first_rev_user = queue[page]['revisions']['first_revision_user']
            first_rev_comment = ''
            # first_rev_comment = queue[page]['revisions']['first_revision_comment']
            recent_rev_values = queue[page]['revisions']['recent_revision_time']
            recent_rev = '{} {} {}, {}:{}h'.format(recent_rev_values[2], datetime.date(recent_rev_values[0], recent_rev_values[1], 1).strftime('%B'), recent_rev_values[0], recent_rev_values[3], recent_rev_values[4])
            recent_rev_user = queue[page]['revisions']['recent_revision_user']
            recent_rev_comment = ''
            # recent_rev_comment = queue[page]['revisions']['recent_revision_comment']
            content = queue[page]['text']
            current_page_html = get_article_template(title, contributors, categories, first_rev, first_rev_user, recent_rev, recent_rev_user, content)
            queue_html += current_page_html

    queue_html = base_header_shift(queue_html)  
    out = open(html_filename, 'w')
    out.write(queue_html)
    out.close()
    print('*{} written*'.format(html_filename))


# * * * * * * * * * * * * * * * * * *
# queue.tmp.html > queue.pdf
#

# --- check pandoc version
def check_pandoc_version():
    request = subprocess.run(["pandoc", "--version"], capture_output=True)
    version_text = request.stdout.decode().split('\n')
    version_string = version_text[0].replace('pandoc ', '').split('.')
    version = int(version_string[0])
    return version

# --- use pandoc to convert the html file into a pdf with the LaTeX engine
def html2pdf(html_tmp_filename, metadata_filename, pdf_filename):
    
    # pandoc variables
    # (these are notes)
    # 
    # -V or --variable = insert variable
    # -N or --number-sections = Number section headings in LaTeX, ConTeXt, HTML, or EPUB output. By default, sections are not numbered. Sections with class unnumbered will never be numbered, even if --number-sections is specified.
    # --template=template.tex 
    # --number-offset=1 

    # latex variables
    # 
    # lof = list of figures
    # pagestyle=headings
    # logo=/path/to/image
    # fontsize=100 (doesn't work...)
    # documentclass=twocolumn, article, report, book, memoir

    # parse metadata
    # version of pandoc used in pi cannot read yaml
    # so individual metadata key:value are given
     
    metadata = get_yaml_data(metadata_filename)
    metadata_authors_option = ['--metadata=author:"{}"'.format(authorname) for authorname in metadata['authors'] ]
    metadata_authors_option = (" ").join(metadata_authors_option)
    pandoc_version_installed = check_pandoc_version()
    if pandoc_version_installed < 2:
        pandoc_pdf_engine_arg = '--latex-engine'
    else:
        pandoc_pdf_engine_arg = '--pdf-engine'

    cmd = '''pandoc -f html -t latex {pdf_engine_arg} xelatex --template=templates/latex.twocolumns.tex --title "PRINT KIOSK II" --metadata=title:"{title}" --metadata=abstract:"{abstract}" {authors} -N -V papersize=a4 -V version=2.0 -V thanks="Thank you!" -V toc-title="Table of Contents" {inputfile} --toc -o {outputfile}'''.format(
            pdf_engine_arg = pandoc_pdf_engine_arg,
            title = metadata['title'],
            abstract = metadata['abstract'],
            authors = metadata_authors_option,
            inputfile=html_tmp_filename,
            outputfile=pdf_filename)

    # cmd = '''pandoc -f html -t latex {pdf_engine_arg} xelatex -s --title "PRINT KIOSK II" --metadata=title:"{title}" --metadata=abstract:"{abstract}" {authors} -N -V papersize=a4 -V version=2.0 -V thanks="Thank you!" -V toc-title="Table of Contents" {inputfile} --toc -o {outputfile}'''.format(
    #         pdf_engine_arg = pandoc_pdf_engine_arg,
    #         title = metadata['title'],
    #         abstract = metadata['abstract'],
    #         authors = metadata_authors_option,
    #         inputfile=html_tmp_filename,
    #         outputfile=pdf_filename)

    os.system(cmd)
    print('*done! {} written*'.format(pdf_filename))

# --- main function, generate the pdf
def queue2pdf(data_json_file, queue_json_file, html_tmp_filename, metadata_filename, pdf_filename):

    # --- load contributors metadata + print queue
    all_pages_contributors = load_all_contributors(data_json_file)
    queue = load_print_queue(queue_json_file)

    # --- queue2html
    queue2html(queue, html_tmp_filename)

    # --- metadata.yaml
    create_metadata_file(metadata_filename, all_pages_contributors)
    
    # --- html2pdf
    html2pdf(html_tmp_filename, metadata_filename, pdf_filename)

if __name__ == '__main__':
    queue2pdf('all_pages.json', 'queue.tmp.json', 'queue.tmp.html', 'latex.metadata.yaml', 'test.pdf')

    # pandoc -f html -t latex --pdf-engine xelatex --template=templates/latex.twocolumns.tex --title "PRINT KIOSK II" --metadata=title:"Elaine" --metadata=abstract:"ABSTRACT PLACEHOLDER" --metadata=author:"AUTHOR PLACEHOLDER" -N -V papersize=a4 -V version=2.0 -V thanks="Thank you!" -V toc-title="Table of Contents" queue.tmp.html --toc -o test.pdf


    # pandoc -f html -t latex --pdf-engine xelatex -s --title "PRINT KIOSK II" --metadata=title:"Elaine" --metadata=abstract:"ABSTRACT PLACEHOLDER" --metadata=author:"AUTHOR PLACEHOLDER" -N -V papersize=a4 -V version=2.0 -V thanks="Thank you!" -V toc-title="Table of Contents" queue.tmp.html --toc -o test.pdf

