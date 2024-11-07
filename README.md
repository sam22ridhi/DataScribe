# DataScribe
Here's a comprehensive GitHub README for your "DataScribe" project, covering all necessary aspects like setup, usage, and features.

---

# DataScribe

## Project Description
**DataScribe** is an AI-powered data retrieval tool that extracts targeted information from the web for entities listed in user-uploaded datasets. Users can upload a CSV or connect a Google Sheet, specify a search query template, and let DataScribe find and parse relevant information using a Language Model (LLM). With a simple, user-friendly interface, DataScribe is ideal for anyone needing to collect structured information about multiple entities efficiently.

## Key Features
- **Data Upload**: Upload a CSV file or connect a Google Sheet for easy data integration.
- **Dynamic Query Input**: Define custom search queries with placeholders (e.g., `{company}`) to specify the type of information needed for each entity.
- **Automated Web Search**: Leverages web search APIs (e.g., SerpAPI) to find specific information for each entity.
- **LLM Data Parsing**: Uses an LLM (e.g., OpenAI’s GPT API or Groq) to interpret and extract data based on user-defined prompts.
- **Structured Output and Download**: Displays extracted data in a table format with options to download as CSV or update a Google Sheet.
- **Optional Advanced Features**: Supports complex queries, error handling, and API rate limit management for enhanced performance.

---

## Table of Contents
- [Project Description](#project-description)
- [Key Features](#key-features)
- [Project Setup](#project-setup)
- [Usage Guide](#usage-guide)
- [API Keys and Environment Variables](#api-keys-and-environment-variables)
- [Optional Features](#optional-features)
- [Demo Video](#demo-video)
- [FAQ](#faq)

---

## Project Setup

### Requirements
- Python 3.8 or above
- [Streamlit](https://streamlit.io/) or [Flask](https://flask.palletsprojects.com/) for the UI
- [Pandas](https://pandas.pydata.org/) for data handling
- Google Sheets API for Google Sheets integration
- [SerpAPI](https://serpapi.com/) or [ScraperAPI](https://www.scraperapi.com/) for web search functionality
- [OpenAI API](https://beta.openai.com/docs/) or [Groq](https://groq.com/) for LLM

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/DataScribe.git
   cd DataScribe
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**  
   In the root directory, create a `.env` file with your API keys and other configurations (details below).

### API Keys and Environment Variables

To ensure secure access to APIs, place your API keys in the `.env` file as follows:
```plaintext
SERPAPI_KEY=your_serpapi_key
OPENAI_KEY=your_openai_key
GOOGLE_SHEETS_API_KEY=your_google_sheets_api_key
```

For additional security, never hard-code API keys directly in the code.

---

## Usage Guide

### 1. Start the Application
- Run the application:
  ```bash
  streamlit run app.py
  ```
- Or, if using Flask:
  ```bash
  python app.py
  ```

### 2. Upload Data
- **CSV Upload**: Click "Browse" to upload a CSV file, or connect to Google Sheets using your Google Sheets API key.
- **Data Preview**: Once uploaded, preview your data and select the primary column (e.g., `company`).

### 3. Define Your Search Query
- Enter a search query in the input box using placeholders (e.g., “Find the email for {company}”). DataScribe will replace placeholders with each entity in your dataset.

### 4. Retrieve Data
- DataScribe will perform automated web searches for each entity and retrieve relevant results.
- After processing, an LLM will parse these results to extract the requested information.

### 5. View and Download Results
- Review the extracted data in the table.
- Download the results as a CSV file or save them to your connected Google Sheet.

---

## Optional Features
If you've implemented any extra features (such as batch processing, advanced query templates, or error handling), describe them here.

---

## Demo Video
Watch a walkthrough of the project here: [Loom Video](https://loom.com/share/your-video-link)

---

## FAQ

1. **Can I use a different search API?**
   Yes! You can use any search or scraping API, like ScraperAPI or an API from a major search engine if compatible with your project requirements.

2. **What if the LLM fails to extract the needed information?**
   DataScribe includes fallback logic, such as retries, and will notify the user if certain data points are unavailable.

3. **How should I handle large datasets?**
   DataScribe is optimized to handle datasets by implementing batch processing to avoid timeouts and API rate limits.

4. **Can I contribute or request features?**
   Yes! We welcome contributions and feedback. Feel free to submit a pull request or raise an issue.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

