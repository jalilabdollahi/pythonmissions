# Mission 063 - Solution
def tags_to_list(s):
    return [t.strip() for t in s.split(",")]

if __name__ == "__main__":
    print(tags_to_list("web,api,db"))
