# Mission 025 - Solution

def copy_allowlist(original):
    result = original.copy()
    return result

if __name__ == "__main__":
    prod_list = ["10.0.0.1", "10.0.0.2"]
    staging = copy_allowlist(prod_list)
    staging.append("10.0.0.99")
    print("prod:", prod_list)
    print("staging:", staging)
