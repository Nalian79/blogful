from mistune import markdown
from blog import app

app.jinja_env.filters['display_markdown'] = markdown

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)
