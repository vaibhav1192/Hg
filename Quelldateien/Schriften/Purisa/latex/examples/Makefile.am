EXAMPLES = teststd.tex

EXTRA_DIST = $(EXAMPLES)

if INCLUDE_LATEX

examplesdir = $(docdir)/examples
examples_DATA = $(EXAMPLES)

CLEANFILES = *.log *.aux *.ttex *.pdf

SUFFIXES = .tex .pdf

.tex.pdf:
	swath -f latex -u u,u < $< > $@.ttex
	pdflatex $@.ttex
	pdflatex $@.ttex
	mv $@.pdf $@

endif # INCLUDE_LATEX
