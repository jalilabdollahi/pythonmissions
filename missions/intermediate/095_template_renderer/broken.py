# Mission 095 - Jinja2 Template Renderer
# Fix the 2 bugs in this script.
try:
    from jinja2 import Environment, StrictUndefined
except ImportError:
    class StrictUndefined: pass
    class Environment:
        def __init__(self, **kw): pass
        def from_string(self, s):
            class T:
                def __init__(self, src): self.src = src
                def render(self, ctx):
                    import re
                    result = self.src
                    for k, v in ctx.items():
                        result = result.replace("{{" + k + "}}", str(v))
                    return result
            return T(s)

def render_template(template_str, context):
    env = Environment(undefined=StrictUndefined)
    tmpl = env.from_string(template_str)
    return tmpl.render(context)  # BUG 1: should be tmpl.render(**context)

def render_nginx_config(server_name, port=80, workers=4, extra=None):
    tmpl = "server {{ server_name }}:{{ port }} workers={{ workers }}"
    ctx = {"server_name": server_name, "port": port, "workers": workers}
    if extra:
        ctx.update(extra)
    return render_template(tmpl, ctx)
