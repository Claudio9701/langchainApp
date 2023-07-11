# LangchainApp - A Django Application for Data Interpretation

LangchainApp is an application built with Django and utilizes the power of ChatGPT to provide a basic interpretation of user uploaded data. This project allows users to upload a CSV file, which is then interpreted by the ChatGPT API. The interpretation provides an overview of the data, its nature, value ranges, data types and suggests potential directions for further analysis.

## Features

- User Authentication: Users can sign in with their own credentials.
- Data Upload: Users can upload data in CSV format.
- Data Interpretation: Uploaded data is interpreted with the help of ChatGPT API and an initial summary is provided.
- Web Interface: The project includes a user-friendly web interface for user interaction.

## Installation

Before running this project, you need to have Python and Django installed in your environment.

1. Clone this repository: `git clone https://github.com/username/LangchainApp.git`
2. Navigate to the project directory: `cd LangchainApp`
3. Create a virtual environment: `python3 -m venv .env`
4. Activate the virtual environment: `source .env/bin/activate` (For Windows, use: `.env\Scripts\activate`)
5. Install the requirements: `pip install -r requirements.txt`
6. Apply the migrations: `python manage.py migrate`
7. Run the Django server: `python manage.py runserver`

## Usage

1. Register a new user.
2. Log in with the newly created user credentials.
3. From the dashboard, navigate to the "Upload CSV" section.
4. Choose the CSV file you want to analyze and click on "Upload".
5. The application will provide an interpretation of the data in the uploaded CSV.

## Tests

To run the tests for this application, use the following command: `python manage.py test`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

## License

This project is licensed under the terms of the MIT license. 
