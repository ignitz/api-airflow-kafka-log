# Airflow Event Listener Kafka Forwarder API

## Overview

This project provides a FastAPI application designed to act as a bridge between Apache Airflow's Event Listener mechanism and Apache Kafka. It receives Airflow DAG Run and Task Instance event data via HTTP POST requests (JSON payload), processes them, serializes them using Avro, and forwards them to specified Kafka topics.

The application supports standard Kafka connections as well as secure connections to AWS Managed Streaming for Kafka (MSK) using IAM SASL authentication.

## Features

* Receives Airflow event data (DAG Runs, Task Instances) via a simple HTTP POST endpoint.
* Parses incoming JSON payloads.
* Serializes event data into Avro format using specified schemas.
* Publishes Avro messages to distinct Kafka topics for DAG Runs and Task Instances.
* Supports standard Kafka broker connections.
* Supports secure authentication with AWS MSK using IAM SASL (`aws-msk-iam-sasl-signer-python`).
* Configuration driven by environment variables (`.env` file).

## Prerequisites

* Python 3.11+
* Pip (Python package installer)
* Access to a Kafka cluster (Standard or AWS MSK).
* Corresponding Kafka topics created (`DAGRun` topic, `TaskInstance` topic).
* Avro schema files in `models` folder for DAGRun and TaskInstance events.
* An Airflow instance configured with an `EventListener` capable of sending POST requests.
* (If using AWS MSK) Configured AWS credentials accessible to the environment where the API runs (e.g., via IAM Role, environment variables, or AWS config file).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <project-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Linux/macOS
    source venv/bin/activate
    # On Windows
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run locally to develop**
    ```bash
    make local
    ```

## Configuration

Configuration is managed via environment variables. Create a `.env` file in the root directory of the project. You can use the `.env.example` as a template.

