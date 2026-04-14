# Mission 148 - Solution
def assert_success(status_code):
    assert status_code < 400, f"Expected success, got {status_code}"

if __name__ == "__main__":
    try:
        assert_success(500)
        print("No error for 500?!")
    except AssertionError as e:
        print(f"Caught: {e}")
    assert_success(200)
    print("200 passed")
