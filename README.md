# scrapy-test

Sample web application for scraping data from news articles on theguardian.com.au

## Install
    
    pip install -r requirements.txt
    pip install -r dev-requirements.txt  # optional for testing
    pip install -e .  # optional for testing
    
## Usage
    
- ### Crawl 

        ./run crawl [OPTIONS]
        
    Crawl theguardian.com.au and extract the news articles from the list of articles 
        
- ### Search

        ./run search [OPTIONS] [QUERY]
        
    Search the database for articles with the search `QUERY`
    
## Testing

    # see install section for testing install requirements
    python setup.py test
    
## Help

    ./run --help
    ./run crawl --help
    ./run search --help