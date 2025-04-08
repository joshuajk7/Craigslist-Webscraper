# CRAIGSLIST-WEBSCRAPER

Discover Your Perfect Vehicle, Efficiently Unlocked

Built with Python and modern web scraping technologies

## Table of Contents

- [Overview](#overview)
- [Why Craiglist-Webscraper?](#why-craiglist-webscraper)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

## Overview

Craigslist-Webscraper is a powerful tool designed for developers seeking to streamline the extraction of car listings from Craigslist.

### Why Craiglist-Webscraper?

This project simplifies the process of finding your ideal vehicle by enabling precise searches and enhancing user experience. The core features include:

- **Extraction and Filtering**: Easily extract car listings based on make, model, price range, and location.
- **Microservice for Suggested Vehicles:** Get tailored recommendations to refine your search and save time.
- **Export to Excel:** Effectively analyze and manipulate your data with convenient Excel exports.
- **Real-time Filter Suggestions:** Enjoy dynamic suggestions that adapt to your search criteria for improved efficiency.
- **User-friendly Format:** Navigate and sort listings with ease, making your search experience seamless.

## Getting Started

### Prerequisites

This project requires the following dependencies:

- Python 3.x
- Pip (Python package manager)

### Installation

To build Craiglist-Webscraper from source and install dependencies:

1. Clone the repository:
```bash
git clone https://github.com/joinup07/craigslist-webscraper
```

2. Navigate to the project directory:
```bash
cd craigslist-webscraper 
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

### Usage
Run the main Script:
```bash
python main.py
```

### Using virtual environment (recommended):
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

### Testing
Craigslist-webscraper uses pytest test framework. Run the test suite with:
```bash
pytest tests/
```
