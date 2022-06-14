import os
from datetime import datetime

from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, _apps


def create_app():
    app = Flask(__name__)
    cred = credentials.Certificate("key.json")
    if not _apps:
        initialize_app(cred)
    db = firestore.client()
    users_ref = db.collection('users')
    state_ref = db.collection("state")



    @app.route('/sessions', methods=["GET"])
    def get_sessions():
        user_id = request.args.get("user_id")

        sessions = state_ref.where("status", "==", "online").stream()

        sessions_arr = []

        for session in sessions:
            s_id = session.id
            s_dict = session.to_dict()
            
            to_append = {}
            if user_id is not None and s_id == user_id:
                to_append['user'] = "You"
            else:
                user = users_ref.document(s_id).get().to_dict()
                to_append['user'] = user['name']
            
            to_append["timestamp"] = s_dict['timestamp']

            sessions_arr.append(to_append)

        return {"success": "Get sessions", "data": sessions_arr}

    @app.route("/logout", methods=["POST"])
    def logout():
        try:
            user_id = request.json['user_id']
            
            current_status = state_ref.document(user_id).get().to_dict()
            print("Current stats: ", current_status)
            if current_status['status'] == "online":
                state_ref.document(user_id).set({"status": "offline", "timestamp": datetime.timestamp(datetime.now())})
            
            return {"success": "Logged out!"}
        except KeyError as e:
            return {"error": "No user id provided"}, 500
        
    return app

if __name__ == '__main__':
    app = create_app
    app.run(host='0.0.0.0', port=os.environ.get("PORT"))