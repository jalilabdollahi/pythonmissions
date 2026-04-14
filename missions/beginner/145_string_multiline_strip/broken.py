# Mission 145 - Strip Multiline Config Block
def clean_block(text):
    """Return list of stripped non-empty lines from text block."""
    return text.strip()

if __name__ == "__main__":
    block = """
    host=localhost
    port=5432
    db=myapp
    """
    print(clean_block(block))
