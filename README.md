# Getting started

Simple news data scraping tool for web development project.

## Create virtual environment with  [pipenv](https://pypi.org/project/pipenv)

```
pipenv install

pipenv shell
```

## or [virtualenv](https://pypi.org/project/virtualenv)

# Run command

From root directory, run command

```
scrapy runspider ./spider/zingnews_spider.py --set=FEED_EXPORT_ENCODING=utf-8 -O ./data/raw-data.json
```
