# Myntra Scraper and Enhancer Project

## Overview

This project scrapes product data from Myntra, enhances the scraped data using OpenAI API, and saves it to JSON files. You can easily run the scraper and enhancer using a single script (`./setup_and_run.sh`), which handles all the necessary setup and execution.

## How to Run the Scripts

### Prerequisites
Before running the scripts, make sure you have the following:

1. **Python 3.8 or higher** installed.
2. **OpenAI API Key** (you will be prompted to enter it during the setup).
3. **Input URLs** input the urls of the products you want to scrape in the `input/urls.py` *in the next line below the previous one*

### Steps to Run:

1. open the project to your local machine.
   ```bash
        git clone git@github.com:sgnhyperion/Product_Data_Enhancer.git
        cd ProductScraper_Consuma
    ```
3. Inside the ProductScraper_Consuma folder, run the following command in terminal to execute the setup script:

    ```bash
        ./setup_and_run.sh
    ```

4. The script will:
    - Create a virtual environment (if not already created).
    - Install all the necessary dependencies.
    - Prompt you to enter your OpenAI API key.

5. The script will scrape product data from Myntra and enhance the data using OpenAI API. The enhanced data will be saved in `output/enhanced_data.json`, and the raw scraped data will be saved in `output/scraped_data.json`.

6. If you want to change your OpenAI API key later, run the following command in your terminal:

    ```bash
    export OPENAI_API_KEY=Your_API_KEY
    ```

7. To deactivate the virtual environment after running the script, use the following command in the terminal:

    ```bash
        deactivate
    ```

## Dependencies

The following dependencies are used in the project:

- `beautifulsoup4`: Used for scraping HTML content from the Myntra website.
- `requests`: Used for sending HTTP requests to fetch webpage content.
- `lxml`: Used by BeautifulSoup to parse HTML content.
- `openai`: Used to interact with OpenAI's GPT model for data enhancement.

These dependencies are automatically installed when you run the setup script.

## Workflow of the Code

1. **Scraping Data**:
   - The scraper fetches product URLs from Myntra.
   - It uses `requests.Session()` to handle requests and maintain session cookies.
   - BeautifulSoup is used to parse the HTML and extract product details like name, price, and rating and description.
   - The scraped data is saved in a JSON format.

2. **Enhancing Data**:
   - After scraping, the product details are enhanced using OpenAI's GPT model.
   - The model categorizes products, infers their pricing segment, and generates a catchy tagline for each.
   - The enhanced data is saved in a separate JSON file.

3. **Parallelization**:
   - To speed up the scraping process, multiple product URLs are scraped concurrently using `ThreadPoolExecutor`.
   - A random delay (`time.sleep(random.uniform(1, 3))`) is used between requests to avoid getting blocked by Myntra.



### Files Explanation

1. **scraper/scraper.py**: Contains the logic for scraping Myntra product pages and storing the data.
2. **input/input.py**: Contains the list of URLs to scrape (to be entered manually).
3. **output**: Stores the output files:
   - `scraped_data.json`: Contains raw scraped data.
   - `enhanced_data.json`: Contains enhanced data after processing with OpenAI API.
4. **requirements.txt**: A text file listing the Python dependencies used in the project.
5. **setup_and_run.sh**: A shell script that sets up the environment and runs the project.

## Conclusion

This project scrapes product data from Myntra and enhances it using OpenAI. You can easily set it up, run the scripts, and get enriched product data in a simple and structured format.

If you encounter any issues, please refer to the README file for troubleshooting, or feel free to ask for support.
