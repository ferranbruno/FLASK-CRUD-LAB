from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage
events = [
    {
        "id": 1,
        "title": "Tech Conference 2026",
        "description": "Annual technology conference",
        "date": "2026-07-15",
        "location": "San Francisco, CA",
        "capacity": 500
    },
    {
        "id": 2,
        "title": "Music Festival",
        "description": "Summer music festival",
        "date": "2026-08-20",
        "location": "Austin, TX",
        "capacity": 1000
    }
]

next_id = 3

# Helper function
def find_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return event
    return None

# ============ GET / ============
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({
        "message": "Welcome to the Events API!"
    }), 200

# ============ GET /events ============
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events), 200

# ============ GET /events/<id> ============
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200

# ============ POST /events ============
@app.route('/events', methods=['POST'])
def create_event():
    global next_id
    
    data = request.get_json()
    
    # Check if data exists
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Check for required 'title' field
    if 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Create new event
    new_event = {
        "id": next_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "date": data.get('date', ''),
        "location": data.get('location', ''),
        "capacity": data.get('capacity', 0)
    }
    
    events.append(new_event)
    next_id += 1
    
    # Return 201 Created with the new event
    return jsonify(new_event), 201

# ============ PATCH /events/<id> ============
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    event = find_event(event_id)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update fields
    if 'title' in data:
        event['title'] = data['title']
    if 'description' in data:
        event['description'] = data['description']
    if 'date' in data:
        event['date'] = data['date']
    if 'location' in data:
        event['location'] = data['location']
    if 'capacity' in data:
        event['capacity'] = data['capacity']
    
    return jsonify(event), 200

# ============ DELETE /events/<id> ============
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = find_event(event_id)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    events.remove(event)
    return jsonify({"message": f"Event {event_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)