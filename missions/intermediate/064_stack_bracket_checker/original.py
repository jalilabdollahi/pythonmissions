# Mission 064 - Stack Bracket Checker
# Fix the 2 bugs in this script.

PAIRS = {")": "(", "]": "[", "}": "{"}

def check_brackets(s):
    stack = []
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack:
                return False
            top = stack.pop()
            if top != PAIRS[char]:
                return False
    return True  # BUG 1: should check stack is empty (unmatched opens)

def count_unmatched(s):
    stack = []
    count = 0
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if stack:
                stack.pop()
            else:
                count += 1
    count += stack  # BUG 2: should be count += len(stack)
    return count
