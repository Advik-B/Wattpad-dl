from sanic import Sanic
from sanic.request import Request
from sanic_ext import render
from sanic.response import json, html, text, file, redirect
from wattpad import Wattpad
from wattpad.modals import Story, User
from wattpad.errors import APIerror
import json

app = Sanic(__name__)
app.config.TEMPLATES_AUTO_RELOAD = True
# app.config.TEMPLATING_PATH_TO_TEMPLATES = "."

wattpad = Wattpad()

@app.route("/")
@app.ext.template("index.html.j2")
async def index(request: Request):
    return await render("index.html.j2", context={})

@app.route("/story/<story_id:int>")
@app.ext.template("story.html.j2")
async def story(request: Request, story_id: int):
    try:
        story = Story.from_id(story_id, wattpad)
    except APIerror as e:
        # Render story.error.html.j2 instead
        return {
            "err": True,
            "error": json.loads(str(e).replace('\'', '"')),
            "story_id": story_id
        }
    return {"story": story, "err":False}
