KEYWORDS = $(shell cat keywords.txt)

SCORES = $(KEYWORDS:%=scores/%)

all : results.html

results.html : scores
	cat $(SCORES) | ./make-table.py > $@

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
	rm -f results.html

pristine : clean
	rm -rf data

.PHONY : all clean pristine

.PRECIOUS : data/github/% data/libraries/%
