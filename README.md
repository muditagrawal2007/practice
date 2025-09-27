# Clothes Shops in Satna

This project is designed to fetch and display the top clothing shops near Satna, Madhya Pradesh using the Serper API. It provides a simple interface to retrieve shop names, descriptions, and other relevant information.

## Project Structure

```
clothes-shops-satna
├── src
│   ├── main.py        # Main entry point of the application
│   └── utils.py       # Utility functions for API calls and data handling
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd clothes-shops-satna
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in your terminal:

```
python src/main.py
```

This will initiate the process of fetching the top clothing shops near Satna, Madhya Pradesh, and display the results in the console.

## API Key

The Serper API key is already configured in the code:
```python
api_key = "5abce63108fa0916d4a9fd2b68635d875c0ddfa5"
```

## Features

- Real-time data fetching from Serper API
- Detailed shop information including:
  - Shop names
  - Descriptions
  - Locations
  - Ratings (where available)
  - Links to more information
- Error handling for API requests and data processing
- Formatted output for easy reading

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.