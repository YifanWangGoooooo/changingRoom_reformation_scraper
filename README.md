## Reformation Scraper for Changing Room

### What is it?

This scraper is a web app using Selenium to fetch all the product information on https://www.reformation.com. It can fetch and display each product's url, name, category, price, description, color, size and their avalibility, image urls. Now it is set to crawl products under a specific category such as clothing or shoes with 4 times of scrolling for testing but the logic behind it is complete. It is also connected to a AWS RDS database.

### Main Features
1. **Scraping**<br>
Run the scraping commands below to easily start the product fetching.
-  % python manage.py scrape_data 'https://www.thereformation.com/clothing'
    
2. **Overview of all the Products Fetched**<br>
-   % python manage.py runserver 
-   http://127.0.0.1:8000/

### Contributors
- Yifan Wang
