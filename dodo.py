import os
import sys

source_path = "~/Dropbox (Princeton)/14_Software/"
source_path_esc = "~/Dropbox\ \(Princeton\)/14_Software/"

helpersPath = os.path.expanduser(source_path + "python/")
sys.path.insert(1, helpersPath)

import helpers

conda_env = "python37"

templatePath = "~/Dropbox\ \(Princeton\)/8_Templates/"

chapters_list = ["~/Github/gunboats/gunboats.md", "~/Github/epbt/epbt.md", "~/Github/tpsp/tpsp.md"]
figures_list = ["~/Github/gunboats/figure/", "~/Github/epbt/figure/", "~/Github/tpsp/figure/"]
# chapters_list = ["~/Github/gunboats/gunboats.md"]
# figures_list = ["~/Github/gunboats/figure/"]

figs_to_transfer = ["aLine.pdf"]

def task_setup():
    yield {
        'name':'setup',
        'actions':["mkdir -p chapters",
                   "mkdir -p figure"]
    }

def task_source():
    yield {
        'name': "migrating templates...",
        'actions': ["mkdir -p templates",
                    "cp -a " + templatePath + "cooley-diss-template.latex " + "templates/",
                    "cp -a " + templatePath + "puthesis.cls " + "."]
    }

def task_bibs():
    yield {
        'name': "sourcing bibs...",
        'actions':["mkdir -p bib/",
                   "cp -a " + templatePath + "python.bib " + "bib/python.bib",
                   "cp -a " + "~/Github/gunboats/bib/Rpackages.bib " + "bib/gunboats.bib",
                   "cp -a " + "~/Github/epbt/bib/Rpackages.bib " + "bib/epbt.bib",
                   "cp -a " + "~/Github/tpsp/bib/Rpackages.bib " + "bib/tpsp.bib"]
    }

def task_pull_chapters():
    """
    first place split.sh in chapters director and run chmod +x split.sh
    """
    for i in chapters_list:
        chapter_i_name = i.split("/")[-1]
        yield {
            'name':"pulling..." + i,
            'actions': ["mkdir -p chapters",
                        "cp " + i + " " + "chapters/",
                        "rm " + "chapters/" + chapter_i_name.split(".")[0] + "_short.md", 
                        "python splitter.py " + "chapters/" + chapter_i_name]
        }

def task_pull_figures():
    for i in figures_list:
        yield {
            'name':"pulling " + i + "...",
            'actions': ["cp -a " + i + " " + "figure/"]
        }

# pip install pdfCropMargins
def task_crop_figures():
    for i in helpers.getFiles("figure/"):
        fname_i = i.split("/")[1]
        yield {
            'name':"cropping " + i + "...",
            'actions':["pdf-crop-margins -mo -pf -su " + "\"backup\" " + i,
                       "rm " + "backup_" + fname_i]
        }

def task_diss():
    """Build paper"""
    yield {
        'name': "writing paper...",
        'actions':["R --slave -e \"set.seed(100);knitr::knit('diss.rmd')\"",
                   "pandoc -r markdown-auto_identifiers --template=templates/cooley-diss-template.latex --filter pandoc-citeproc -o diss.tex diss.md",
                   "pandoc -r markdown-auto_identifiers --template=templates/cooley-diss-template.latex --filter pandoc-citeproc -o diss.pdf diss.md"],
                   'verbosity': 2,
    }

def task_introduction():
    yield {
        'name':"writing introduction...",
        'actions':["cp -a " + templatePath + "cooley-short-article-template.tex " + "templates/",
                   "R --slave -e \"set.seed(100);knitr::knit('diss_intro.rmd')\"",
                   "pandoc --template=templates/cooley-short-article-template.tex --filter pandoc-citeproc -o diss_intro.pdf diss_intro.md"]
    }