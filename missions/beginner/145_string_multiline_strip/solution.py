# Mission 145 - Solution
def clean_block(text):
    return [line.strip() for line in text.splitlines() if line.strip()]

if __name__ == "__main__":
    block = """
    host=localhost
    port=5432
    db=myapp
    """
    print(clean_block(block))
