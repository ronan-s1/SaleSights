# Project Plan

<details><summary><h2>Services and Technologies<h2></summary>

### Add Sales

When a sale is a made it should be added to the database.

A sale can be added:
- Manually (from a dropdown of products)
- Through scanning salesight [barcode](#generate-barcodes--qr-codes)
- Importing a correctly formatted CSV file

<hr>

### Add Expenses

When an expense is a made it should be added to the database.

Ann expense can be added a sale:
- Manually (from a dropdown of [products](#add-products))
- Uploading a correctly formatted CSV file

<hr>

### Add Products

Ability to add a list of products manually or through uploading a correctly formatted CSV file.

There should be fields for:
- Product ID
- Product name
- Price
- Category

maybe more?

<hr>

### Generate Barcodes / QR codes

- Ability to Generate a Barcode / QR code.
- These codes would be placed on products. 
- These products would be scanned when adding a sale.

<hr>

### Generate Reciepts

After a sale has been made and added to the database, a reciept should be generated.

<hr>

### Analytics

Ability to view daily, weekly, monthly quarterly insights on business sales and expenses through charts.

<hr>

### Generate Invoices

Ability to create an invoice with business logo.

<hr>

### Generate Reports

Generate reports on past sales and expenses. Maybe intergrate a summary explaining the report using AI.

<hr>

### Export Data

Ability to export data in to a CSV or Excel file for external reporting and analysis.

<hr>

### NLP Data Querying

Allow users to query their businesses data using natural language, for example: "What product has been sold the most in the last month?"

A chatbot like interface can be created for this.

<hr>

### Sentiment Analysis on Reviews

Scrape data from google reviews and analyse the reviews using AI similar to [this project](https://github.com/ronan-s1/Django-Sentiment-Analysis-Application) I made.

<hr>

### Implement PyGWalker

PyGWalker is Python Library for Exploratory Data Analysis with Visualization. It can simplify data analysis and data visualization workflow, by turning a pandas dataframe (and polars dataframe) into a Tableau-style User Interface for visual exploration.

You can easily incorporate PyGwalker into a Streamlit application; check out [this](https://docs.kanaries.net/pygwalker/use-pygwalker-with-streamlit) resource for more information.

<hr>

### SaleSight API

Allow users to intergreate SaleSights service's with other programs and software via an API

## Possible Tools, Technolgies and Frameworks

Here are some proposed tools I am planning to use.

### Streamlit

Streamlit is an open-source framework that for custom web app development. It's great for building intuitive interfaces and developing data driven applications as it keep users informed with dynamic data that refreshes in real-time.

It has good support for intergrating plotly graphs which would be great for dynamic and interactive sales and expense charts. It also good for displaying pandas dataframes.

Streamlit can seamlessly integrate with popular computer vision libraries and frameworks, such as OpenCV, Dlib, TensorFlow etc which could be used for scanning the [QR / Barcodes](#generate-barcodes--qr-codes)

Streamlit has intergation with mongodb using the [streamlit secrets manager](https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb).

The book "Web Application Development with Streamlit
Develop and Deploy Secure and Scalable Web Applications to the Cloud Using a Pure Python Framework" discusses more above in more detail.

<hr>

### Langchain

LangChain is an open source framework to aid the development of applications leveraging the power of Large Language Models.

LangChain DataFrame Agent is a tool that allows interaction with a pandas DataFrame, optimised for question answering. This agent can be used to query your data using natural language.

![langchain df agent flow](https://blog.streamlit.io/content/images/2023/07/langchain-5-scheme.JPG.jpg)

There are other LLM libraries such as [LlamaIndex](https://www.llamaindex.ai/) which I am also considering using.

<hr>

### Plotly

Plotly's Python graphing library makes interactive, publication-quality graphs. [Plotly website](https://plotly.com/python/).

<hr>

### Pandas

Pandas is a fast, powerful, flexible and easy to use open source data analysis library, also works well with Plotly. [Pandas website](https://pandas.pydata.org/).

<hr>

### BERT

BERT(Bidirectional Encoder Representations from Transformers) can perform sentiment analysis on [reviews](#sentiment-analysis-on-reviews).

<hr>

### Docker

Docker can be used for containerising the app and deploying it (maybe).

## Interim and Final Report

For the write up part of the FYP I will be using [Overleaf](https://www.overleaf.com/) which is an online LaTeX editor.

</details>


<details><summary><h2>Choosing all services and tech stack<h2></summary>

### Core Services
- Add Sale
  - Ability to scan barcode to add to a sale transaction
- Add Expense
- Add Product
  - Associate a barcode with a product (optional)
  - **fields:**
  - Product ID
  - Product name
  - Price
  - Category
  - Barcode
- Display analytics
- Generate receipts
- Export data

### Other Services
- Generate reports
- NLP Querying

### Services to implement if I have time
- PyGWalker
- Sentiment Analysis
- SaleSight API

## Technolgies

### Frontend Technologies
- Streamlit
- Streamlit Components

<img src="https://images.ctfassets.net/23aumh6u8s0i/2vWy8CrwyDEsApwk5wHzge/2962bedb072ac7cd952b4ce134d5e132/05_capabilities-zero-app.png" width="550">

### Backend Technologies
- Langchain (for report analysis)
- LlamaIndex (for NLP querying)
- Pandas
- Plotly
- OpenCV

### Database
- MongoDB

</details>
