# Mission 149 - Generate the Alert Email
from string import Template

def render_alert(template_str, values):
    """Fill in Template placeholders with values dict."""
    return Template(template_str).substitute(values)

if __name__ == "__main__":
    tmpl = "Alert: @level on @host - @message"
    vals = {"level": "CRITICAL", "host": "web-01", "message": "disk full"}
    print(render_alert(tmpl, vals))
