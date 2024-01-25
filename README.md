# polyvalent-scraper

_Experimental project to get familiar with python language_

Polyvalent scraper to extract data, postprocess it and insert it in a MySQL database.
Can also use machine learning to guess data categorization

### Working fonctionnalities:
- Crawl bank website and extract specific account transactions data
- Add the possibility to insert previous history of transactions in the database from a .csv file
- Insert transactions into a MySQL database
- Use a BERT LLM to guess the appropriate categories for the transactions without one
- Various email notifications

### Next steps:
- Add a crawler for another bank
- Extend the crawling to other type of data (energy consumption?)
- Improve logging & monitoring?
