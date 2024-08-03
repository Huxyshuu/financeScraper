# FinanceScraper
A python app for getting useful information from yahoo finance

## Setup Instructions
Run these commands in order inside a terminal to get the app set up properly
1. Clone the repository:
   ```
   git clone https://github.com/Huxyshuu/financeScraper
   ```
2. Create a virtual environment for python to install the requirements and run the commands below
   ``` 
   cd yourproject

   python -m venv venv     # creates a virtual environment

   venv\Scripts\activate   # activates the virtual environment

   pip install -r requirements.txt
   ```
3. Run the app or create an executable file (.exe) to run. Make sure you have virtual environment activated
   ```
   python app.py                         #to run the app

   pyinstaller financeScraper.spec       #to create an executable file (.exe)
   ```
4. The app should open a browser window upon starting and you'll be greeted with a rather dull page at first.
5. Typing in a valid stock ticker will bring up useful information about the stock such as the **current price**, **forward P/E**, etc. *(might sometimes throw a HTTP 401 error, which is usually fixed by restarting the app)*

![Image of the page](https://i.imgur.com/GtFJGTV.png)

## Tech
- Flask to build a web interface for the app
- yfinance to indirectly get the data from yahoo finance api 
