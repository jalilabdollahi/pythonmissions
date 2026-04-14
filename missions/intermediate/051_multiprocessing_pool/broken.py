# Mission 051 - Multiprocessing Pool
# Fix the 2 bugs in this script.
import multiprocessing

def process_item(item):
    return item * item

def process_batch(items):
    with multiprocessing.Pool() as pool:
        results = pool.apply(process_item, items)  # BUG 1: should be pool.map()
    return results

def sum_squares(items):
    return sum(process_batch(items))  # BUG 2: process_batch returns int from apply, not list
