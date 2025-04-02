import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import threading


def map_function(chunk):
    """Map function to count messages per sender in a data chunk."""
    local_counts = defaultdict(int)
    for sender in chunk['name']:
        local_counts[sender] += 1

    return local_counts


def reduce_function(results):
    """Reduce function to combine counts from all chunks."""
    final_counts = defaultdict(int)
    for count_dict in results:
        for sender, count in count_dict.items():
            final_counts[sender] += count

    return final_counts


def find_most_active_users(input_file, top_n=10, chunksize=10000):
    """Find the most active users (by message count) using map-reduce pattern.

    :param input_file: Path to input CSV file with message data
    :type input_file: str
    :param top_n: Number of top users to return (default: 10)
    :type top_n: int
    :param chunksize: Number of rows to process at a time (default: 10000)
    :type chunksize: int

    :returns: List of tuples (email, count) sorted by count descending
    :rtype: list
    """
    print(f"\nFinding {top_n} most active users from {input_file}")

    start_time = time.time()

    # Shared list for map results
    map_results = []
    lock = threading.Lock()

    def process_chunk(chunk):
        """Process a single chunk and store results thread-safely."""
        result = map_function(chunk)
        with lock:
            map_results.append(result)

    # Read data in chunks and process with ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        for chunk in tqdm(
            pd.read_csv(input_file, chunksize=chunksize),
            desc="Processing chunks"
        ):
            executor.submit(process_chunk, chunk)

    # Reduce phase
    final_counts = reduce_function(map_results)

    # Get top N most active users
    top_users = sorted(
        final_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    elapsed = time.time() - start_time
    print(f"\nFound {top_n} most active users in {elapsed:.2f} seconds")

    return top_users


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Execute map reduce using ThreadPoolExecutor"
    )
    # Positional args.
    parser.add_argument("input_file", type=str, help="Input CSV file path")

    # --key=value args.
    parser.add_argument(
        "-c",
        "--chunksize",
        type=int,
        default=10000,
        help="Rows per chunk (default: 10,000)",
    )
    parser.add_argument(
        "-t",
        "--top_n",
        type=int,
        default=10,
        help="Number of top users to return (default: 10)",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    # Analyze message data (if generated)
    message_file = args.input_file.replace('.csv', '_messages.csv')
    try:
        top_users = find_most_active_users(
            args.input_file,
            top_n=args.top_n,
            chunksize=args.chunksize
        )
        print("\nMost active users (by message count):")
        for i, (user, count) in enumerate(top_users, 1):
            print(f"{i}. {user}: {count} messages")
    except FileNotFoundError:
        print("\nNo message data found for analysis")
