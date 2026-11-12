# Mission 142 - Exposition Writer
# Render metrics in the Prometheus text exposition format.


def escape_label_value(text):
    text = str(text)
    return text.replace('"', '\\"')


def format_labels(labels):
    if not labels:
        return ""
    pairs = [f'{key}="{escape_label_value(value)}"' for key, value in labels.items()]
    return "{" + ",".join(pairs) + "}"


def format_value(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def render_metrics(metrics):
    lines = []
    for metric in metrics:
        lines.append(f"# HELP {metric['name']} {metric['help']}")
        lines.append(f"# TYPE {metric['name']} {metric['type']}")
        for labels, value in metric["samples"]:
            lines.append(f"{metric['name']}{format_labels(labels)} {format_value(value)}")
    return "\n".join(lines)
