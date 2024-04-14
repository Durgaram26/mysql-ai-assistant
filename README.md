# Chat with MySQL AI Assistant

This project implements a Streamlit-based application that allows users to interact with a MySQL database using natural language queries. The application features an AI assistant capable of interpreting user queries, generating corresponding SQL queries, executing them on the database, and presenting the results back to the user in a conversational format.

https://github.com/saha-trideep/Chat-With-SQL-Database/assets/115859105/fc1b39e9-d28f-43ad-be78-57b3c2982333

## Table of Contents

- [Introduction](#introduction)
- [Dataset](#dataset)
- [Features](#features)
- [Usage](#usage)
- [Installation](#installation)

## Introduction

As a data analyst or enthusiast, accessing and analyzing data from databases can often be cumbersome, especially when dealing with SQL queries. The Chat with MySQL AI Assistant simplifies this process by allowing users to interact with the database using natural language, abstracting away the complexities of SQL querying.


## Dataset

The dataset used in this project was obtained from Kaggle. It is available at [Jobs and salaries in data field 2024](https://www.kaggle.com/datasets/murilozangari/jobs-and-salaries-in-data-field-2024).

The dataset provides information about jobs in the data field, including details such as work year, experience level, employment type, job title, salary, salary currency, employee residence, work setting, company location, company size, and job category.


## Features

- **Interactive Chat Interface**: Users can converse with the AI assistant through a chat interface, asking questions or requesting information about the data stored in the MySQL database.
  
- **Natural Language Processing (NLP)**: The AI assistant utilizes NLP techniques to interpret user queries and translate them into SQL queries that the database can understand.

- **SQL Query Generation**: Based on the user's input, the AI assistant generates SQL queries tailored to retrieve the desired information from the database.

- **Real-time Interaction**: Users can see immediate responses to their queries, facilitating seamless interaction and exploration of the database content.

## Usage

1. **Connecting to MySQL Database**: Users provide the necessary database connection details such as host, user, port, database name, and password through the Streamlit sidebar. Upon clicking the "Connect" button, the application establishes a connection to the MySQL database.

2. **Chat Interface**: Once connected, users can interact with the AI assistant through the chat interface. They can ask questions or input queries related to the data stored in the database using natural language.

3. **Query Execution**: The AI assistant interprets the user's queries, generates corresponding SQL queries, and executes them on the MySQL database. The results are then presented back to the user in a conversational format.

## Installation

To install and run the Chat with MySQL AI Assistant locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/chat-with-mysql.git

2. Navigate to the project directory:
   ```bash
   cd chat-with-mysql
   
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Run the Streamlit application:
   ```bash
   streamlit run original.py
   ```




