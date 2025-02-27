# Code Curer

Welcome to Code Curer! This project aims to provide tools and resources for improving code quality and curing common coding issues. Whether you're a beginner or an experienced developer, Code Curer offers solutions to enhance your coding practices.

A project designed for TransfiNITTe '24, NIT Tiruchirappalli's Annual Hackathon. This website blends traditional algorithmic vulnerability scanning along with LLMs to search code for vulnerabilities and errors, across any language. Powered by DeepSeek Coder and Snyk.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/harishsenthilkumar06/Code-curer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Code-curer
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Flask server:
   ```bash
   python Server.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000/`.
3. Use the interface to explore the tools and resources available.
4. Follow the guides and use the tools to improve your code quality.

### Routes
- **`/`**: The index page.
- **`/choice`**: Page to select the type of input (source code or Git repository).
- **`/source`**: Page to input and analyze source code.
- **`/gitpage`**: Page to provide a Git repository URL for cloning and analysis.

## Contributing
Contributions are welcome! Feel free to fork this repository, submit issues, or create pull requests.
