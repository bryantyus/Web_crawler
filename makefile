PY=python3.6
STYLE=astyle
OPT=python

demo:
	@$(PY) web_crawler.py

.PHONY:clean
clean:
	rm *.jpg
