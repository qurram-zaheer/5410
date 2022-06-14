import os
import uuid

from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, _apps

def create_app():
    app = Flask(__name__)

    cred = credentials.Certificate("key.json")
    if not _apps:
        initialize_app(cred)
    db = firestore.client()
    users_ref = db.collection('users')

    @app.route('/register', methods=["POST"])
    def register():
        
        if not all(k in request.json for k in ("name", "email", "password", "location")):
            return {"error": "Bad request"}, 500

        uid = uuid.uuid4().hex

        docs = users_ref.where("email", "==", request.json['email']).get()

        if len(docs) > 0:
            return {"error": "Email already exists, please login!"}

        returned_doc = users_ref.add(request.json)
        
        print(returned_doc[1].get().to_dict())

        return_user = returned_doc[1].get().to_dict()
        return_user["user_id"] = returned_doc[1].id
        return {"success": "Added user", "user": return_user}


    @app.route("/delete_test", methods=['POST'])
    def delete_test():
        id = users_ref.where("email", "==", "test@test.com").get()[0].id
        users_ref.document(id).delete()
        return "success"
    
    return app


if __name__ == '__main__':
    print("PORT: ", os.environ.get("PORT"))
    app = create_app()
    app.run(host='0.0.0.0', port=os.environ.get("PORT"))