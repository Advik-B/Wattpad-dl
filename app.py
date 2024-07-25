from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from wattpad import Wattpad, Story, Part, PublishedPart
from modes.wattpad_mode import WattpadMode
import wattpad.errors
import tempfile
import json
import os
import re

app = Flask(__name__, template_folder="html")
api = Api(app, prefix="/api")
wattpad_story_regex = re.compile(r"https://www.wattpad.com/story/(\d+)-(.+)")
wattpad_part_regex = re.compile(r"https://www.wattpad.com/(\d+)-(.+)")

# Create a Wattpad engine
if os.environ.get("PROD") == "true":
    engine = Wattpad(use_cache=True, cache_dir=tempfile.gettempdir())
else:
    engine = Wattpad(use_cache=False)


class WattpadStory(Resource):
    def get(self, url: str):
        # Check if the url is a story url
        current_mode = None
        story_match = wattpad_story_regex.match(url)
        part_match = wattpad_part_regex.match(url)
        id = None
        if story_match:
            current_mode = WattpadMode.STORY
            id = story_match.group(1)
        elif part_match:
            current_mode = WattpadMode.PART
            id = part_match.group(1)
        else:
            return jsonify({"error": "Invalid URL"}), 400

        if current_mode == WattpadMode.STORY:
            story = Story.from_id(id, engine)
        else:
            story = Story.from_partid(id, engine)

        return jsonify(story)



api.add_resource(WattpadStory, "/story/<int:story_id>")

# Story url
# https://www.wattpad.com/story/336166598-wounded-love-%E2%9C%85%EF%B8%8F

# Part url
# https://www.wattpad.com/1322118318-wounded-love-%E2%9C%85%EF%B8%8F-aesthetics

# Notice that the story url is always /story/<story_id>-<story_name>
# The part url is always /<part_id>-<part_name>

@app.route("/")
def index():
    return render_template("index.j2")
