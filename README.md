# langchain-agent

A versatile and customizable language model assistant using OpenAI.

## Demo

<p align="center">
<img src="agent.gif" alt="demo" width="70%">

<p align="center">


## Description

This project is a Python-based implementation that utilizes OpenAI's GPT model to create a helpful assistant capable of answering various questions, extracting information from web pages, and performing several other tasks. The assistant is easily extensible with new tools and features, allowing developers to tailor the functionality to specific use cases.

## Installation

### Prerequisites

* Python 3.6 or higher
* virtualenv

### Setup

1. Clone the repository:

```bash
git clone https://github.com/theodo-group/langchain-agent.git
```

2. Navigate to the project directory:

```bash
cd langchain-agent
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your virtual environment is active:

```bash
source venv/bin/activate
```

2. Run the `app.py` script:

```bash
python app.py
```

The assistant will process the queries provided in the `app.py` file and print the results.

To use the assistant with custom queries, modify the `app.py` file or create a new script that imports and initializes the `Assistant` class.

## Extending the Assistant

To add new tools or features to the assistant, create a new `Tool` instance and add it to the `tools` list in the `tools.py` file. Make sure to provide a unique name, a function that implements the tool's functionality, and a description.

You can also create new prompt templates and output parsers by extending the base classes provided by the `langchain` library.


## Acknowledgments

* OpenAI for creating the GPT language model
* The `langchain` library for providing a convenient way to interact with language models