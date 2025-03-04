# Terminal Calendar Plugin

This project is a Flask-based web service that fetches events from an Apple public calendar iCal link, filters the events for a specified number of days, and returns the events in a JSON format. The JSON response is formatted to be consumed by TRMNL plugin.

## Features

- Fetch events from an Apple public calendar iCal link.
- Filter events for a specified number of days.
- Return events in a JSON format.
- Support for recurring events.
- Basic authentication using an API key.

## Requirements

- Python 3.9+
- Flask
- requests
- icalendar
- python-dateutil

## Installation

1. Clone the repository:

    ```sh
    git clone <>
    cd trmnl-calendar-plugin
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Replace the `ICAL_URL` and `API_KEY` in [main.py](http://_vscodecontentref_/1) with your Apple public calendar iCal link and your desired API key.

## Usage

1. Run the Flask server:

    ```sh
    python main.py
    ```

2. Make a GET request to fetch events:

    ```sh
    curl -X GET "http://127.0.0.1:5000/fetch-events?days=7" \
         -H "Content-Type: application/json" \
         -H "X-API-KEY: your_api_key_here"
    ```

## API

### GET /fetch-events

Fetch events from the Apple public calendar.

#### Query Parameters

- `days` (optional): The number of days to look ahead. Default is 7.

#### Headers

- `Content-Type`: Must be `application/json`.
- `X-API-KEY`: Your API key for authentication.

#### Response

- `200 OK`: Returns a JSON object with the events.
- `401 Unauthorized`: Invalid API key.
- `415 Unsupported Media Type`: Invalid `Content-Type` header.
- `500 Internal Server Error`: Failed to fetch calendar.

#### Example Response

```json
{
  "text": "Family Calendar - 7 days",
  "author": "shyam",
  "collection": [
    {
      "event": "summary 1",
      "date": "March 05",
      "time": "10:30AM - 11:00AM"
    },
    {
      "event": "summary 2",
      "date": "March 06",
      "time": "01:00PM - 02:00PM"
    }
  ]
}