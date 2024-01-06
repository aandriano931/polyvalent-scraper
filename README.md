# polyvalent-scraper
Polyvalent scraper to extract data, postprocess it and insert it in a MySQL database

Working fonctionnalities:
- Crawl bank website and extract specific account transactions data
- Add the possibility to insert transactions previous history in the database from a .csv file provided by the bank
- Insert transactions into a MySQL database
- Use a BERT LLM to guess the appropriate categories for the transactions without a category
- Various email notifications

Next steps:
- Add a crawler for another bank
- Extend the crawling to other type of data (energy consumption?)
- Improve logging & monitoring?
