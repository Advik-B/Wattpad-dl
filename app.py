from sanic import Sanic
from sanic.request import Request

app = Sanic(__name__)
app.config.TEMPLATES_AUTO_RELOAD = True
# app.config.TEMPLATING_PATH_TO_TEMPLATES = "."


@app.route("/")
@app.ext.template("story.html")
async def index(request: Request):
    return {}

