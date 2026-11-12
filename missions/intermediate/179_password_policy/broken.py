# Mission 179 - Policy Enforcer
# Validate passwords against the company policy and list every violation.
import string


def check_password(password, username="", min_length=12):
    problems = []
    if len(password) <= min_length:
        problems.append("too_short")
    if not any(c.islower() for c in password):
        problems.append("no_lower")
    if not any(c.isupper() for c in password):
        problems.append("no_upper")
    if not any(c.isdigit() for c in password):
        problems.append("no_digit")
    if not any(not c.isalnum() for c in password):
        problems.append("no_symbol")
    if username and username in password:
        problems.append("contains_username")
    return problems


def is_valid(password, username="", min_length=12):
    return not check_password(password, username, min_length)


def explain(problems):
    messages = {
        "too_short": "use more characters",
        "no_lower": "add a lowercase letter",
        "no_upper": "add an uppercase letter",
        "no_digit": "add a digit",
        "no_symbol": "add a symbol such as ! or #",
        "contains_username": "do not include your username",
    }
    return "; ".join(messages[p] for p in problems) or "ok"
