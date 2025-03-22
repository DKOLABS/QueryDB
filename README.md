# QueryDB

QueryDB is a project designed to manage and display search queries using a web-based interface. It allows users to filter and search through various predefined queries stored in YAML files.

## Project Structure
```
QueryDB/
├── .gitignore
├── bin/
│   ├── build.py
├── build/
│   └── output.html
├── README.md
├── searches/
├── templates/
│   ├── card.html
│   ├── footer.html
│   ├── header.html
│   ├── script.js
│   └── style.css
```

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DKOLABS/QueryDB.git
    cd QueryDB
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\Activate.ps1`
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. Populate searches as yaml files in the `searches` folder.

2. To build the HTML output, run the `build.py` script:
    ```sh
    python bin/build.py
    ```

3. Open the generated `output.html` file in your web browser to view the search queries.
