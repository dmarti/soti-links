KEYWORDS = $(shell cat keywords.txt)

SCORES = $(KEYWORDS:%=scores/%)

all : results.html results.csv

preview : results.html
	firefox results.html

results.html : make-table.py scores
	cat $(SCORES) | ./make-table.py html > $@

results.csv : make-table.py scores
	cat $(SCORES) | ./make-table.py csv > $@

scores : $(SCORES)

data/github/% : curl-github.sh
	./curl-github.sh $@

data/libraries/% : curl-libraries.sh
	./curl-libraries.sh $@

scores/% : Makefile ./parse.py data/github/% data/libraries/% 
	mkdir -p scores
	./parse.py $@ > $@

clean :
	find . -type f -size 0 -delete
	rm -rf scores
	rmdir data || true
	rm -f results.html results.csv

pristine : clean
	rm -rf data

.PHONY : all clean pristine

.PRECIOUS : data/github/% data/libraries/%
