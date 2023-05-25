# Installation Guide for Repo Reader

This document provides a step-by-step guide on how to install and set up Repo Reader. Follow the instructions below to get started.

## Prerequisites

Before we begin, ensure that you have Python 3.7 or above installed on your system. You can verify your Python version by running the following command in your terminal:

```bash
python --version
```

Or, if you're using Python 3 explicitly:

```bash
python3 --version
```

If you don't have Python installed or have an older version, visit the [official Python website](https://www.python.org/) to download and install the latest version.

Also, make sure that you have `virtualenv` installed on your system. If not, you can install it using pip:

```bash
pip install virtualenv
```

## Installation

Now, let's start the installation process for Repo Reader:

### Step 1: Create a Directory

First, create a new directory named `repos`:

```bash
mkdir repos
```

### Step 2: Set Up a Virtual Environment

Create a virtual environment in the `repos` directory:

```bash
virtualenv venv
```

Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On Unix or MacOS:

```bash
source venv/bin/activate
```

### Step 3: Install Requirements

Now, install the necessary requirements for Repo Reader:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Next, you need to set up your environment variables. You'll find a `.env.example` file in the root directory of Repo Reader. This file contains sample environment variables for the project.

Make a copy of this file and name it `.env`:

```bash
cp .env.example .env
```

Open the newly created `.env` file and replace the sample values with your actual data. Be careful not to share this file as it contains sensitive information.

### Step 5: Run the Application

Finally, you can start the application by running the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server and you can access the application by visiting the link shown in your terminal.

---

If you encounter any issues during the installation process, please refer to the FAQ.md or open a new issue on our GitHub page. Enjoy using Repo Reader!