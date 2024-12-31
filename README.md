# HelpMateAI - Simplifying Insurance Information Retrieval


## Project Overview

HelpMateAI is a cutting-edge application designed to simplify the retrieval of information from voluminous insurance-related documents. By leveraging advanced Natural Language Processing (NLP) techniques and state-of-the-art Large Language Models (LLMs), HelpMateAI enables users to extract precise answers from extensive document collections with ease. The tool eliminates the need to manually search through hundreds of pages, providing accurate results along with citations (document name and page number) for further reference.

## Problem Statement

Insurance companies and clients often struggle with accessing specific details from extensive documentation. Traditional methods of information retrieval require:

Manually scanning through hundreds of pages in a single document.
Cross-referencing between multiple documents to find related information.
Spending a significant amount of time locating critical details.
These challenges lead to inefficiencies, wasted time, and increased user frustration, particularly when swift decision-making or detailed understanding is required.

Current Challenges:

- Navigating documents with more than 100+ pages.
- Lack of a centralized system for precise, contextual answers.
- Inability to provide quick and accurate citations for follow-up reading.
- Absence of conversational context or memory in querying tools, limiting a seamless user experience.


## Key Objectives

- `Ease of Information Retrieval`
- `Citation for Transparency`
- `Efficiency Through AI`
- `User Experience`
- `Accuracy and Relevance`
- `Scalability for Future Enhancements`

## Features

- Effortless Query Resolution: Retrieve answers to user queries from a plethora of documents in no time.

- Citations for Reference: Provides document names and page numbers for further reading.

- Streamlined Search: Eliminates the need to manually scan through large PDFs with hundreds of pages.

## Technology Stack

HelpMateAI is built using the following technologies:

-  `Python`: Core programming language.

- `Closed and Open Source LLMs`: For processing natural language queries.

- `PDFPlumber`: For extracting text from PDF documents.

- `ChromaDB`: Vector database for managing embeddings and performing similarity searches.

- `Grok API`: For contextual processing.

- `OpenAI APIs`: For leveraging advanced language models.

- `pandas`: For data manipulation and processing.

- `Other Python Libraries`: Supporting tools and utilities for implementation.

## System Architecture

### Step 1: Build the Vector Store

- Use an embedding model to convert document chunks into vector representations and store them in the vector database.

## Step 2: Cache, Search, and Rerank
- Process user queries:

    - First, search in the cache for a quick response.

    - If the query is not found in the cache, search the main vector database.

- Retrieve top-k closest document chunks and rerank them using Cross Encoders for semantic accuracy.

## Step 3: Generative Search

- Combine the query, prompt, and top 3 reranked document chunks.

- Use a Large Language Model (LLM) to generate the final response.

![b77d0c75-c07b-44e1-90ed-366bd3138808-generation](https://github.com/user-attachments/assets/06078dcd-45f4-4d1b-a8a3-a8a0962993ef)


## User Interaction

Users can interact with HelpMateAI through a web-based UI. Simply enter a query related to your insurance document, and the system will provide an accurate response along with relevant citations.

## Limitations

- Does not store user chat history.

- No memory for consecutive chats.

## Feature Scope

- `Chat History Storage`: Retain user interactions for better context in follow-up queries.

- `User-Level Sessions`: Personalized experiences with session-based interactions.

- `Enhanced Memory`: Provide memory to the LLM for more coherent multi-turn conversations.


## Acknowledgements
- This Project is a part of my assignment for Post Graduate Diploma Degree in AI & ML at IIIT-Bangalore

## ✍️ Author
Developed by [Upendra Kumar]. For queries, reach out at [upendra.kumar48762@gmail.com].
