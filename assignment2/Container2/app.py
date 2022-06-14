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


    @app.route('/login', methods=["POST"])
    def login():
        body = request.json
        
        if not all(k in request.json for k in ("email", "password")):
            return {"error": "Bad request"}, 500

        users_ref = db.collection("users")

        docs = users_ref.where("email", "==", request.json['email']).get()

        if len(docs) > 0:
            user = docs[0].to_dict()
            user_id = docs[0].id
            if user['password'] == request.json['password']:
                current_status = state_ref.document(user_id).get().to_dict()
                if current_status is None or current_status['status'] == "offline":
                    state_ref.document(user_id).set({"status": "online", "timestamp": datetime.timestamp(datetime.now())})
                return {"success": "Signed in successfully!", "user_id": user_id}
            else:
                return {"error": "Wrong username or password, please try again."}
        else:
            return {"error": "User not found, please register!"}
    
    return app

if __name__ == '__main__':
    print("PORT: ", os.environ.get("PORT"))
    app = create_app()
    app.run(host='0.0.0.0', port=os.environ.get("PORT"))