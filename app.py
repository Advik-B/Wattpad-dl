from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from wattpad import Wattpad, Story, Part, PublishedPart
import wattpad.errors
import tempfile
import json
import os

app = Flask(__name__, template_folder="html")
api = Api(app, prefix="/api")

# Create a Wattpad engine
if os.environ.get("PROD") == "true":
    engine = Wattpad(use_cache=True, cache_dir=tempfile.gettempdir())
else:
    engine = Wattpad(use_cache=False)

class WattpadStory(Resource):
    def get(self, story_id):
        try:
            story = Story.from_id(story_id, engine)
            return jsonify(story)

        except wattpad.errors.APIerror as e:
            str_e = str(e).replace("'", "\"")
            error = json.loads(str_e)
            match error["error_code"]:
                case 1017:  # Not found
                    return error, 404
                # Default case
                case _:
                    return error, 500


api.add_resource(WattpadStory, "/story/<int:story_id>")

@app.route("/")
def index():
    return render_template("index.j2")
