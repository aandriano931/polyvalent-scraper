# polyvalent-scraper
Polyvalent scraper to extract data, postprocess it and insert it in a MySQL database

Working fonctionnalities:
- Crawl bank website and extract transactions data
- Insert transactions into a MySQL database
- Use a BERT LLM to guess the appropriate categories for the inserted transactions
- Update the transactions without a category with the guessed categories
- Email notification in case of failure

Next steps:
- Add a crawler for another bank
- Extend the crawling to other type of data (energy consumption?)
- Improve logging monitoring?
- Improve email notification (send LLM guessed categories for review)
