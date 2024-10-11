from sanic import Sanic
from sanic.request import Request
from sanic.response import json, html, text, file, redirect
from wattpad import Wattpad
from wattpad.modals import Story, User

app = Sanic(__name__)
app.config.TEMPLATES_AUTO_RELOAD = True
# app.config.TEMPLATING_PATH_TO_TEMPLATES = "."


@app.route("/")
@app.ext.template("index.html.j2")
async def index(request: Request):
    if request.args.get("story"):
        story = await Story.from_id(request.args.get("story"))
        return {"story": story}
    
    return text("No story provided in query string")
