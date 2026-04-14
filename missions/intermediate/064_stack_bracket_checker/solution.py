# Mission 064 - Stack Bracket Checker
# Fixed solution

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
    return len(stack) == 0

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
    count += len(stack)
    return count
