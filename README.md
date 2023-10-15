# SaleSights

## Services List

### Add Sales

When a sale is a made it should be added to the database.

A sale can be added:
- Manually (from a dropdown of products)
- Through scanning salesight [barcode](#generate-barcodes)
- Importing a correctly formatted CSV file

### Add Expenses

When an expense is a made it should be added to the database.

Ann expense can be added a sale:
- Manually (from a dropdown of [products](#add-products))
- Uploading a correctly formatted CSV file

### Add Products

Ability to add a list of products manually or through uploading a correctly formatted CSV file.

There should be fields for:
- Product ID
- Product name
- Price
- Category

maybe more?

### Generate Barcodes / QR codes

- Ability to Generate a Barcode / QR code.
- These codes would be placed on products. 
- These products would be scanned when adding a sale.

### Generate Reciepts

After a sale has been made and added to the database, a reciept should be generated.

### Analytics

Ability to view daily, weekly, monthly quarterly insights on business sales and expenses through charts.

### Generate Invoices

Ability to create an invoice with business logo.

### Generate Reports

Generate reports on past sales and expenses.

### Export Data

Ability to export data in to a CSV or Excel file for external reporting and analysis.

### NLP Data Querying

Allow users to query their businesses data using natural language, for example: "What product has been sold the most in the last month?"

A chatbot like interface can be created for this.

### Sentiment Analysis on Reviews

Scrape data from google reviews and analyse the reviews using AI similar to [this project](https://github.com/ronan-s1/Django-Sentiment-Analysis-Application) I made.

## Possible Tools, Technolgies and Frameworks

### Streamlit

Streamlit is an open-source framework that for custom web app development. It's great for building intuitive interfaces and developing data driven applications as it keep users informed with dynamic data that refreshes in real-time.

It has good support for intergrating plotly graphs which would be great for dynamic and interactive sales and expense charts. It also good for displaying pandas dataframes.

Streamlit can seamlessly integrate with popular computer vision libraries and frameworks, such as OpenCV, Dlib, TensorFlow etc which could be used for scanning the [QR / Barcodes](#generate-barcodes--qr-codes)

Streamlit has intergation with mongodb using the [streamlit secrets manager](https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb).

The book "Web Application Development with Streamlit
Develop and Deploy Secure and Scalable Web Applications to the Cloud Using a Pure Python Framework" discusses more above reasons in more detail.


### Langchain

LangChain is an open source framework to aid the development of applications leveraging the power of Large Language Models. It can be used for chatbots, text summarization, data generation, question answering, and more. LangChain's strength lies in its wide array of integrations and capabilities. 

LangChain DataFrame Agent is a tool in LangChain that allows interaction with a pandas DataFrame, optimized for question answering. This agent can be used to query your data using natural language.

!(diagram)[https://blog.streamlit.io/content/images/2023/07/langchain-5-scheme.JPG.jpg]