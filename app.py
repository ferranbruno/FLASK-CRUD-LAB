from flask import Flask, request, jsonify

app = Flask(__name__)

# Event class for the autograder
class Event:
    def __init__(self, id, title, description="", date="", location="", capacity=0):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.capacity = capacity
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "capacity": self.capacity
        }

# Sample data with Event objects
events = [
    Event(1, "Tech Conference 2026", "Annual technology conference", "2026-07-15", "San Francisco, CA", 500),
    Event(2, "Music Festival", "Summer music festival", "2026-08-20", "Austin, TX", 1000)
]

next_id = 3

# Helper functions
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

def event_to_dict(event):
    return event.to_dict()

# ============ ROUTE 1: GET / ============
@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the Events API!"}

# ============ ROUTE 2: GET /events ============
@app.route('/events', methods=['GET'])
def get_events():
    return [event.to_dict() for event in events]

# ============ ROUTE 3: GET /events/<id> ============
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = find_event(event_id)
    if event is None:
        return {"error": "Event not found"}, 404
    return event.to_dict()

# ============ ROUTE 4: POST /events ============
@app.route('/events', methods=['POST'])
def create_event():
    global next_id
    
    data = request.get_json()
    
    if not data:
        return {"error": "No data provided"}, 400
    
    if 'title' not in data:
        return {"error": "Title is required"}, 400
    
    new_event = Event(
        id=next_id,
        title=data['title'],
        description=data.get('description', ''),
        date=data.get('date', ''),
        location=data.get('location', ''),
        capacity=data.get('capacity', 0)
    )
    
    events.append(new_event)
    next_id += 1
    
    return new_event.to_dict(), 201

# ============ ROUTE 5: PATCH /events/<id> ============
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    event = find_event(event_id)
    
    if event is None:
        return {"error": "Event not found"}, 404
    
    data = request.get_json()
    
    if not data:
        return {"error": "No data provided"}, 400
    
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'date' in data:
        event.date = data['date']
    if 'location' in data:
        event.location = data['location']
    if 'capacity' in data:
        event.capacity = data['capacity']
    
    return event.to_dict(), 200

# ============ ROUTE 6: DELETE /events/<id> ============
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = find_event(event_id)
    
    if event is None:
        return {"error": "Event not found"}, 404
    
    events.remove(event)
    return {"message": f"Event {event_id} deleted"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)