# Mission 051 - Multiprocessing Pool
# Fixed solution
import multiprocessing

def process_item(item):
    return item * item

def process_batch(items):
    with multiprocessing.Pool() as pool:
        results = pool.map(process_item, items)
    return results

def sum_squares(items):
    return sum(process_batch(items))
