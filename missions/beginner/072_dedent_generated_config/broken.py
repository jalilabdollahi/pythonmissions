# Mission 072 - Indented Config Template
# Renders nginx-style config blocks from embedded templates.
import textwrap


def render_vhost(domain, port):
    template = f"""
    server {{
        listen {port};
        server_name {domain};
    }}
    """
    return template.strip() + "\n"


def render_upstream(name, servers):
    lines = "\n".join("        server %s;" % s for s in servers)
    template = f"""
    upstream {name} {{
{lines}
    }}
    """
    return template.strip() + "\n"


def render_all(sites):
    return "\n".join(render_vhost(domain, port) for domain, port in sites)


if __name__ == "__main__":
    print(render_vhost("shop.example", 8080))
