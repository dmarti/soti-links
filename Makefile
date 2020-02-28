all : data/github/gdpr data/github/ccpa

data/github/% :
	./curl-github.sh $@

data/libraries/% :
	./curl-libraries.sh $@

clean : 
	true

pristine : clean
	rm -rf data

.PHONY : all clean pristine

