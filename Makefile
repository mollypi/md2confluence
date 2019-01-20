MAKEFLAGS += --no-builtin-rules

PYTHON  ?= python3
DESTDIR ?= out

SOURCES := $(shell find * -type f -name '*.md' -not -path $(DESTDIR))
TARGET_HTMLS := $(patsubst %.md, $(DESTDIR)/%.html, $(SOURCES))
TARGET_DIRS := $(sort $(dir $(TARGET_HTMLS)))
TARGETS := $(TARGET_HTMLS) $(TARGET_DIRS)

all: $(TARGET_HTMLS)

# see: http://ismail.badawi.io/blog/2017/03/28/automatic-directory-creation-in-make/
$(DESTDIR)/:
	mkdir -p $@

$(DESTDIR)%/:
	mkdir -p $@

.SECONDEXPANSION:

$(DESTDIR)/%.html: %.md Makefile convert.py | $$(@D)/
	$(PYTHON) -mconvert < $< > $@

clean: Makefile
	git clean -dfx $(DESTDIR)

.PHONY: all clean
.PRECIOUS: $(TARGET_DIRS)
.SUFFIXES: