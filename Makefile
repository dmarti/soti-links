KEYWORDS = $(shell cat keywords.txt)

# GITDATA = $(KEYWORDS:%=data/github/%)
# LIBRARIESDATA = $(KEYWORDS:%=data/libraries/%)

SCORES = $(KEYWORDS:%=scores/%)

# data : $(GITDATA) $(LIBRARIESDATA)

scores : $(SCORES)

data/github/% : curl-github.sh
	./curl-github.sh $@

data/libraries/% : curl-libraries.sh
	./curl-libraries.sh $@

scores/% : Makefile ./parse.py data/github/% data/libraries/% 
	mkdir -p scores
	./parse.py $@ > $@

clean : 
	rm -rf scores

pristine : clean
	rm -rf data scores

.PHONY : all clean pristine

