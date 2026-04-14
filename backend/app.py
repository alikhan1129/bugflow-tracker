from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from backend.models import db, Bug
from backend.services import bug_service
from backend.schemas import BugCreate, BugUpdate

import os
load_dotenv()
print(f"DEBUG: GEMINI_API_KEY present: {bool(os.getenv('GEMINI_API_KEY'))}")

def create_app():
    # Configure Flask to serve the React production build
    dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
    app = Flask(__name__, static_folder=dist_path, static_url_path='/')
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bugflow.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    CORS(app)

    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')
    
    @app.route('/api/bugs', methods=['POST'])
    def create_bug():
        try:
            data = BugCreate(**request.json)
            bug = bug_service.create_bug(data)
            return jsonify(bug.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/bugs', methods=['GET'])
    def get_bugs():
        bugs = bug_service.get_all_bugs()
        return jsonify([b.to_dict() for b in bugs])

    @app.route('/api/bugs/<int:bug_id>', methods=['PATCH'])
    def update_bug(bug_id):
        try:
            data = BugUpdate(**request.json)
            bug = bug_service.update_bug(bug_id, data)
            return jsonify(bug.to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return app.send_static_file('index.html')

    with app.app_context():
        # Ensure database and tables exist
        db.create_all()
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
