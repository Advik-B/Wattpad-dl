from wattpad import Wattpad
from wattpad.modals import Story
import tempfile
from html5tagger import Document, E
wattpad = Wattpad(use_cache=True)

s = Story.from_id(125486510, wattpad)


# print(f"""
# Title: {s.title}
# Author: {s.author}
# Description: {s.description}
# Tags: {s.tags}
# """)

doc = Document(
    E.TitleText_(s.title),
)

doc.Div_(E.h1(s.title), E.img(src=s.cover, alt="Story Cover"))
doc.p(f"By {s.author.name}")
doc.p(s.description)
doc.p("Tags: ", ", ".join(s.tags))

# End the document
with open("story.html", "w") as f:
    f.write(str(doc))
