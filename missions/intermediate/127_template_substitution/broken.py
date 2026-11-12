# Mission 127 - Missing Placeholders
# Render $name / ${name} templates and report which variables were missing.
from string import Template


def find_placeholders(text):
    names = set()
    for match in Template.pattern.finditer(text):
        name = match.group("named")
        if name:
            names.add(name)
    return sorted(names)


def render(text, values):
    missing = sorted(n for n in find_placeholders(text) if not values.get(n))
    rendered = Template(text).substitute(values)
    return rendered, missing


def render_all(templates, values):
    """Render several templates; report the union of missing names."""
    outputs = {}
    all_missing = set()
    for name, text in templates.items():
        outputs[name], missing = render(text, values)
        all_missing.update(missing)
    return outputs, sorted(all_missing)
