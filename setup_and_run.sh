#!/bin/bash

# Step 1: Set up Python virtual environment (if not already created)
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Step 2: Activate the virtual environment
source .venv/bin/activate
echo "Virtual environment activated."

Step 3: Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# step 4: Input the API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Please input your OpenAI API key:"
    read OPENAI_API_KEY
    export OPENAI_API_KEY=$OPENAI_API_KEY
fi

# Step 4: Run the scraper
echo "Running the scraper to fetch product data..."
python3 scraper/scraper.py

# Step 5: Run the enhancer to process the scraped data
echo "Enhancing product data using OpenAI API..."
python3 main.py

# # # Step 6: Deactivate the virtual environment
# # deactivate

echo "Setup and execution completed successfully."
