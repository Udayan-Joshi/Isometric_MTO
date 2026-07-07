# Isometric MTO Extractor

A full-stack web application that automatically extracts a **Material Take-Off (MTO)** from a piping isometric drawing using **Google Gemini Vision** and presents the extracted engineering information in a structured, downloadable format.

The application allows users to upload a single isometric drawing (PNG, JPG, or PDF), processes it through an AI-powered extraction pipeline, validates the extracted information, displays the results in a clean interface, and supports CSV export.

---

# Project Overview

The objective of this project is to automate the generation of a Material Take-Off (MTO) from piping isometric drawings.

The application consists of:

* A **Next.js** frontend for uploading drawings and displaying results.
* A **FastAPI** backend for validation, AI inference, normalization, and CSV generation.
* A **Google Gemini Vision** pipeline for extracting engineering information.
* A normalization layer that converts AI output into a consistent application schema.

---

# Architecture

```text
                    +----------------------+
                    |    Next.js Frontend  |
                    +----------+-----------+
                               |
                         HTTP Requests
                               |
                               ▼
                    +----------------------+
                    |    FastAPI Backend   |
                    +----------+-----------+
                               |
                     File Validation Layer
                               |
                               ▼
                    Google Gemini Vision
                               |
                               ▼
                     Raw AI JSON Response
                               |
                               ▼
                    Response Normalizer
                               |
                               ▼
                    Pydantic Validation
                               |
                               ▼
                     Structured MTO JSON
                               |
               +---------------+---------------+
               |                               |
               ▼                               ▼
        Frontend Results                 CSV Export
```

---

# Project Structure

```text
Isometric_MTO/

├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── prompts/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── types/
│   └── package.json
│
├── samples/
├── screenshots/
└── README.md
```

---

# Features

## Frontend

* Upload PNG, JPG and PDF drawings
* Client-side validation
* Upload progress indicator
* Drawing preview
* Drawing metadata display
* Material Take-Off table
* Summary dashboard
* CSV download
* Responsive interface
* Loading and error states

## Backend

* FastAPI REST API
* Swagger documentation
* Server-side validation
* Google Gemini Vision integration
* AI response normalization
* Pydantic validation
* CSV generation
* Graceful fallback to mock extraction
* Health endpoint

---

# Technology Stack

| Component   | Technology                              |
| ----------- | --------------------------------------- |
| Frontend    | Next.js                                 |
| Language    | TypeScript                              |
| Styling     | Tailwind CSS                            |
| Backend     | FastAPI                                 |
| Language    | Python                                  |
| Validation  | Pydantic                                |
| AI Provider | Google Gemini Vision (gemini-2.5-flash) |
| Testing     | Pytest                                  |

---

# Setup Instructions

## Prerequisites

* Python 3.11+
* Node.js (LTS)
* npm

---

## Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:3000
```

---

# Environment Variables

Create a `.env` file inside the backend directory.

```text
GOOGLE_API_KEY=your_google_ai_studio_api_key
MODEL_NAME=gemini-2.5-flash
```

A sample configuration is provided in:

```text
backend/.env.example
```

---

# API Endpoints

| Method | Endpoint          | Description                     |
| ------ | ----------------- | ------------------------------- |
| GET    | `/api/health`     | Health check                    |
| POST   | `/api/extract`    | Upload drawing and generate MTO |
| GET    | `/api/export/csv` | Download MTO as CSV             |

---

# AI Pipeline

The extraction pipeline is designed to be modular and provider-independent.

```text
Upload Drawing
      │
      ▼
File Validation
      │
      ▼
Image / PDF Processing
      │
      ▼
Google Gemini Vision
      │
      ▼
Raw JSON Response
      │
      ▼
Response Normalization
      │
      ▼
Pydantic Validation
      │
      ▼
Structured MTO
      │
      ▼
Summary Generation
      │
      ▼
CSV Export
```

### Pipeline Stages

### 1. Validation

The backend validates:

* File type
* File size
* Upload integrity

before sending the drawing to the AI model.

### 2. AI Extraction

Google Gemini Vision analyzes the uploaded drawing and extracts:

* Drawing metadata
* Pipes
* Fittings
* Flanges
* Valves
* Gaskets
* Bolt sets
* Summary information

The prompt instructs Gemini to behave as a piping engineering expert and return structured JSON.

### 3. Response Normalization

LLM outputs may vary slightly in structure. A dedicated normalization layer converts Gemini's raw JSON into the application's standardized MTO schema.

Examples include:

* Mapping `type` → `category`
* Assigning item numbers
* Filling missing optional fields with defaults
* Standardizing engineering units
* Applying default confidence values when unavailable

This ensures a consistent internal representation regardless of minor variations in AI responses.

### 4. Validation

The normalized output is validated using Pydantic models before being returned to the frontend.

### 5. Graceful Fallback

If the Gemini API is unavailable, an API key is missing, or inference fails, the application automatically returns a schema-compliant mock MTO response. This ensures the application remains fully functional and satisfies the graceful degradation requirement.

---

# Prompt Strategy

The extraction prompt is designed to simulate the reasoning of an experienced piping engineer.

The prompt instructs Gemini to:

* Identify engineering metadata
* Detect piping components
* Recognize fittings and valves
* Estimate engineering quantities
* Return only JSON
* Avoid explanatory text
* Produce deterministic output using low temperature

The prompt is stored separately in:

```text
backend/app/prompts/extraction_prompt.txt
```

to keep business logic independent of application code.

---

# MTO Output Structure

Each response consists of three sections:

```text
Drawing Metadata

↓

Items[]

↓

Summary
```

## Drawing Metadata

* Drawing Number
* Revision
* Line Number
* NPS
* Material Class
* Service

## Items

Each extracted component contains:

* Item Number
* Category
* Description
* Size
* Schedule
* Material
* End Type
* Quantity
* Unit
* Length
* Confidence
* Remarks

## Summary

The backend generates a summary including:

* Total Pipe Length
* Fittings
* Flanges
* Valves
* Gaskets
* Bolt Sets
* Field Welds

---

# Assumptions

* One drawing is processed per upload.
* Supported formats are PNG, JPG, and PDF.
* The first page of a PDF is considered.
* Pipe lengths are reported in metres.
* In-memory storage is sufficient for this assessment.
* CSV export represents the latest processed extraction.

---

# Known Limitations

* Extraction accuracy depends on drawing quality and clarity.
* Dense or low-resolution drawings may reduce extraction accuracy.
* Hand-drawn drawings are not specifically optimized.
* Engineering quantities are generated by the Vision LLM and may require manual verification.
* Multi-page PDF processing is not currently implemented.

---

# Future Improvements

Given additional development time, the following enhancements would be implemented:

* Hybrid OCR + Vision pipeline
* Computer vision-based symbol detection
* Multi-page PDF processing
* Batch drawing uploads
* SQLite/PostgreSQL persistence
* User authentication
* Engineering rule validation
* Confidence visualization
* Excel export
* Support for multiple AI providers

---

# Testing

Backend tests are implemented using **Pytest**.

Included tests:

* Health endpoint
* Extraction endpoint

Run tests using:

```bash
pytest
```

---

# Sample Drawings

Sample drawings used during development are included in the `samples/` directory.

---

# Screenshots

The `screenshots/` directory contains example images of:

* Upload Page
* Results Page

---

# Notes

This project was developed as part of the Pathnovo Full-Stack AI Assessment.

The architecture emphasizes modularity by separating AI inference, normalization, validation, and presentation into independent layers. This design allows the AI provider or extraction strategy to be replaced without affecting the frontend or API contract.
