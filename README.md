# NBA Data Analytics Dashboard

An interactive Streamlit dashboard for exploring NBA player data. The app cleans the source data by filling missing college values, removing players without a positive salary, and converting player heights from feet and inches to total inches.

## Features

- Filter players by team, position, and age.
- View the average salary, youngest player, and average age for the selected players.
- Browse the filtered player data in a table.
- Compare average salaries by team and average weight by position.
- View the five highest-paid players.
- Explore the relationship between player height and salary by position.
- Inspect the height and salary correlation matrix.
- View players under 30 earning more than $5 million and export the results to a CSV file.

## Installation

Install the project dependencies from the project directory:

```bash
pip install -r requirements.txt
```

## Running the App

From the project directory, start the dashboard with:

```bash
streamlit run nba_dashboard.py
```

The dashboard uses the NBA CSV dataset and displays the results in your browser.
