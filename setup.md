# Project Setup Guide

Welcome to the project! This guide will help you set up the application on your local machine for development and testing purposes.


## Setup Instructions

Follow these steps to get your development environment up and running:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/AthenaFoss/Shallu.W3K.git
cd Shallu.W3K
```

### 2. Create a Virtual Environment

To avoid conflicts with other projects and dependencies, it's best to create a virtual environment:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment using the following commands based on your operating system:

- **Windows**:

  ```bash
  .\.venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```bash
  source .venv/bin/activate
  ```

### 4. Run the Setup Script

Install the necessary dependencies and set up the project by running the setup script:

```bash
python setup.py
```

### 5. Start the Development Server

Finally, start the development server to run the application:

```bash
uvicorn api-server:app --reload
```

## Additional Information

### Directory Structure

Here’s a brief overview of the project’s directory structure:

```
Shallu.W3K/
│
├── api-server.py          # Main API server script
├── setup.py               # Setup script
├── requirements_base.txt  # Base requirements file
├── .venv/                 # Virtual environment directory
├── data.csv               # CSV file containing data
├── support-ticket.py      # Support ticket handling script
├── query_pipelines/
│   └── default/
│       └── entrypoint.py  # Default query pipeline entrypoint
├── databases/
│   ├── master/
│   │   └── master.db      # Master SQLite database
│   ├── default_pipeline_vdb/  # Default pipeline vector database
│   └── support-ticket/
│       └── support-ticket.db  # Support ticket SQLite database
└── .env                   # Environment variables file
```

### Deactivating the Virtual Environment

After you are done with development, you can deactivate the virtual environment with:

```bash
deactivate
```

### Troubleshooting

If you encounter any issues during setup, please check the following:

- Ensure Python and pip are correctly installed and accessible from your command line.
- Verify that you have activated the virtual environment before running the setup script.

If the problem persists, feel free to open an issue in the repository or reach out to the maintainers for support.


