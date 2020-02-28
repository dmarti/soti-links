KEYWORDS = $(shell cat keywords.txt)

GITDATA = $(KEYWORDS:%=data/github/%)
LIBRARIESDATA = $(KEYWORDS:%=data/libraries/%)

data : $(GITDATA) $(LIBRARIESDATA)

data/github/% :
	./curl-github.sh $@

data/libraries/% :
	./curl-libraries.sh $@

clean : 
	true

pristine : clean
	rm -rf data

.PHONY : all clean pristine

