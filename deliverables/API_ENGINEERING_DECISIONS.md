\# Engineering Rationale — Mohammad\_API



\## Overview

This repository was designed as an offline-capable AI service using FastAPI. The system combines OCR, local LLM capabilities, classical machine learning, retrieval, and RAG in a modular backend with a lightweight web interface.



\## Why FastAPI

FastAPI was selected because it provides:

\- high-performance API handling

\- built-in validation through Pydantic

\- automatic OpenAPI/Swagger documentation

\- clean modular routing



This made it a strong fit for building a well-structured AI API.



\## OCR Approach

OCR was implemented using Tesseract with OpenCV preprocessing.



\### Why this approach

\- fully offline

\- practical and lightweight

\- good enough for scanned documents and screenshots

\- supports multilingual scenarios



\### Preprocessing choices

The OCR pipeline includes configurable preprocessing such as:

\- grayscale

\- resize

\- denoise

\- deskew

\- thresholding



These were added because OCR quality depends heavily on image quality.



\## Local LLM Approach

The local LLM functionality was implemented using Ollama.



\### Why Ollama

\- very practical for local inference

\- easy model management

\- simple integration through HTTP

\- works well with small local models like llama3.2



This made it the best balance between usability and offline capability.



\## Additional AI Capabilities

Beyond OCR and local LLM chat, the API includes:

\- summarization

\- information extraction

\- classical ML prediction

\- retrieval

\- RAG question answering



This set was selected to make the system coherent as a document intelligence platform rather than a collection of unrelated endpoints.



\## ML Prediction Component

A small classical ML prediction model was included to satisfy the requirement for a trained prediction component.



\### Why this was included

\- demonstrates model training + inference integration

\- shows that the API supports both LLM and non-LLM AI

\- keeps the project technically diverse



\## Retrieval and RAG

The retrieval pipeline was designed to support document-based question answering.



\### Why retrieval was included

\- explicitly aligned with the assignment

\- demonstrates design thinking beyond simple LLM wrapping

\- creates a realistic document AI workflow



\### RAG architecture

The RAG flow is:

1\. upload document

2\. extract or load text

3\. chunk text

4\. build retrieval index

5\. retrieve relevant chunks

6\. pass context to local LLM

7\. generate grounded answer



\## API Structure

The API is organized by routers and services.



\### Why this structure

\- routers define public endpoints

\- services contain business logic

\- responsibilities stay separated

\- future features can be added cleanly



This improves maintainability and extensibility.



\## Frontend Design

A lightweight HTML/CSS/JavaScript frontend was added on top of FastAPI.



\### Why not a separate frontend framework

The goal was fast delivery, simplicity, and easy evaluation. A lightweight interface was enough to demonstrate the product clearly without adding unnecessary frontend complexity.



\## Dockerization

Docker was used to package the API and runtime dependencies.



\### Why Docker

\- reproducible setup

\- easier grading

\- simpler dependency handling

\- practical deployment packaging



\## Maintainability, Extensibility, and Usability

The system was designed to be:

\- easy to run

\- easy to review

\- easy to extend



Examples:

\- each capability has its own route/service

\- the UI is organized by feature

\- Docker supports repeatable setup



\## Tradeoffs Considered

\- local models were preferred over larger cloud models for offline capability

\- lightweight retrieval was preferred over a more complex vector DB for simplicity

\- the cloud demo may expose only a subset of the full offline functionality



\## Assumptions and Limitations

\- Ollama is available locally for full LLM functionality

\- the cloud version may run in limited mode

\- OCR quality depends on input quality

\- the RAG pipeline is lightweight and optimized for clarity over scale



\## Conclusion

The final design aims to demonstrate practical engineering judgment, not just endpoint count. The system is structured as a coherent offline document intelligence service with clear architecture and multiple AI capabilities.

