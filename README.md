# GCP Expert
A GCP Go-to Chatbot

# How to run?
## First Steps
1. Install Python and add to PATH
2. Using the change directory command navigate into this cloned repo main folder.
3. Create two folders in the root of the project: `chroma` and `data`
4. Create a virtual environment with: `python -m venv ./`
5. Activate the virtual environment (in the same terminal): `./Scripts/activate` command
6. Install the dependencies with `pip install -r requirements.txt`
7. Run the project with: python `./src/main.py`
8. Onto the next!

## Scraping
This is a one time process to scrape documents off of Google Docs (currently only for generative-ai) and put them in text files with respective route slugs (e.g /overview becomes overview.txt)
If your virtual environment is already running, simply run the command `python ./app/scraping/main.py` inside the root directory.
