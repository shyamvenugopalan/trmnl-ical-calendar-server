from flask import Flask, request, jsonify
import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta, timezone, date
import json
from dateutil.rrule import rrulestr
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Replace with your Apple public calendar iCal link and API key
ICAL_URL = '<your-ical-url>'
API_KEY = '<your-api-key>'

@app.route('/fetch-events', methods=['GET'])
def fetch_events():
    logging.info('Received request to fetch events')

    # Check for API key
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        logging.warning('Unauthorized access attempt')
        return jsonify({'error': 'Unauthorized'}), 401

    # Check for Content-Type header
    if request.headers.get('Content-Type') != 'application/json':
        logging.warning('Unsupported Media Type')
        return jsonify({'error': 'Unsupported Media Type'}), 415

    # Get the number of days to look ahead from query parameters, default to 7
    days = request.args.get('days', default=7, type=int)
    logging.info(f'Looking ahead {days} days')

    response = requests.get(ICAL_URL)
    if response.status_code != 200:
        logging.error('Failed to fetch calendar')
        return jsonify({'error': 'Failed to fetch calendar'}), 500

    cal = Calendar.from_ical(response.content)
    events = []
    now = datetime.now(timezone.utc)
    look_ahead_date = now + timedelta(days=days)
    
    for component in cal.walk():
        if component.name == "VEVENT":
            event_start = component.get('dtstart').dt
            event_end = component.get('dtend').dt
            if isinstance(event_start, date) and not isinstance(event_start, datetime):
                event_start = datetime.combine(event_start, datetime.min.time(), tzinfo=timezone.utc)
            if isinstance(event_end, date) and not isinstance(event_end, datetime):
                event_end = datetime.combine(event_end, datetime.min.time(), tzinfo=timezone.utc)
            if event_start.tzinfo is None:
                event_start = event_start.replace(tzinfo=timezone.utc)
            if event_end.tzinfo is None:
                event_end = event_end.replace(tzinfo=timezone.utc)
            
            if 'RRULE' in component:
                rule = component.get('RRULE').to_ical().decode()
                rrule = rrulestr(rule, dtstart=event_start)
                duration = event_end - event_start
                for dt in rrule.between(now, look_ahead_date):
                    event = {
                        'event': str(component.get('summary')),
                        'date': dt.strftime('%B %d'),
                        'time': f"{dt.strftime('%I:%M%p')} - {(dt + duration).strftime('%I:%M%p')}"
                    }
                    events.append(event)
            else:
                if now <= event_start <= look_ahead_date:
                    event = {
                        'event': str(component.get('summary')),
                        'date': event_start.strftime('%B %d'),
                        'time': f"{event_start.strftime('%I:%M%p')} - {event_end.strftime('%I:%M%p')}"
                    }
                    events.append(event)

    # Sort events by start date and time
    events.sort(key=lambda x: datetime.strptime(x['date'] + ' ' + x['time'].split(' - ')[0], '%B %d %I:%M%p'))

    response_data = {
        "text": "Family Calendar - {} days".format(days),
        "author": "Shyam Nair",
        "collection": events
    }

    logging.info('Successfully fetched and processed events')
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)