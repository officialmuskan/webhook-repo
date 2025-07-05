from flask import Blueprint, json, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix="/webhook")


@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    # print(data)
    event_type = request.headers.get('X-GitHub-Event')
    print(event_type)
    timestamp = datetime.utcnow().isoformat()

    try:
        if event_type == 'push':
            event = {
                "type": "push",
                "author": data['pusher']['name'],
                "to_branch": data['ref'].split('/')[-1],
                "timestamp": timestamp
            }
            print(event)

        elif event_type == 'pull_request':
            pr_action = data['action']
            print(pr_action)
            if pr_action == "reopened" or pr_action == "opened":
                event = {
                    "type": "pull_request",
                    "author": data['sender']['login'],
                    "from_branch": data['pull_request']['head']['ref'],
                    "to_branch": data['pull_request']['base']['ref'],
                    "timestamp": timestamp

                }
                print(event)
            elif pr_action == "closed" and data['pull_request']['merged']:
                event = {
                    "type": "merge",
                    "author": data['sender']['login'],
                    "from_branch": data['pull_request']['head']['ref'],
                    "to_branch": data['pull_request']['base']['ref'],
                    "timestamp": timestamp
                }
                print(event)
            else:
                return '', 204
        else:
            return '', 204

        mongo.db.events.insert_one(event)
        return jsonify({"msg": "Event saved"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@webhook.route('/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find({}, {"_id": 0}))
    return jsonify(events)


@webhook.route('/')
def index():
    print("hello")
    return render_template('index.html')
