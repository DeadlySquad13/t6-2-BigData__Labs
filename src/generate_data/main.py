import argparse
import time
from pathlib import Path

from tqdm import tqdm
import numpy as np
import pandas as pd
from faker import Faker


def generate_data(
    output_file: Path, number_of_rows: int, chunksize=100000, locale="ru_RU", seed=None
):
    """Generate a large CSV file with fake data using pandas and Faker.

    This function efficiently generates large datasets by processing data in chunks,
    making it memory-friendly for very large files.

    :param output_file: Path to output CSV file
    :type output_file: str
    :param num_rows: Total number of rows to generate
    :type num_rows: int
    :param chunksize: Number of rows to process at a time (default: 10000)
    :type chunksize: int
    :param locale: Locale for localized fake data (default: 'ru_RU')
    :type locale: str
    :param seed: Random seed for reproducibility (default: None)
    :type seed: int or None

    :returns: None
    :rtype: None

    Generated Data Fields:
        * id - Sequential identifier
        * name - Full name
        * email - Email address
        * age - Age

    Example:
        >>> generate_fake_data_with_pandas('output.csv', 1000000, chunksize=50000, locale='fr_FR')
        >>> # Generates 1 million rows of French data in 50k row chunks
    """

    if seed is not None:
        Faker.seed(seed)
        np.random.seed(seed)

    fake = Faker(locale)
    rng = np.random.default_rng()

    start_time = time.time()

    with tqdm(total=number_of_rows, desc="Generating data...") as pbar:
        for chunk in np.arange(np.ceil(number_of_rows / chunksize)):
            batch_size = min(number_of_rows, chunksize)

            messages = [fake.text(max_nb_chars=100) for _ in range(batch_size)]

            df = pd.DataFrame(
                {
                    "id": np.arange(chunk * batch_size, (chunk + 1) * batch_size, dtype=int),
                    "name": [fake.name() for _ in range(batch_size)],
                    "email": [fake.email() for _ in range(batch_size)],
                    "age": rng.integers(low=18, high=99, size=batch_size),
                    "message_length": [len(msg) for msg in messages],
                    "message": messages,
                }
            )

            # Write header only for first chunk
            header = chunk == 0
            df.to_csv(output_file, mode="a", header=header, index=False)

            pbar.update(batch_size)

    elapsed = time.time() - start_time
    print(f"\nGenerated {number_of_rows:,} rows in {elapsed:.2f} seconds")
    print(f"File saved to: {output_file}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate large CSV files with fake data"
    )
    # Positional args.
    parser.add_argument("output_file", type=str, help="Output CSV file path")

    # --key=value args.
    parser.add_argument(
        "-n",
        "--number_of_rows",
        type=int,
        default=1000000,
        help="Number of rows to generate (default: 1,000,000)",
    )
    parser.add_argument(
        "-c",
        "--chunksize",
        type=int,
        default=10000,
        help="Rows per chunk (default: 10,000)",
    )
    parser.add_argument(
        "-l",
        "--locale",
        type=str,
        default="ru_RU",
        help="Locale for fake data (e.g., en_US, fr_FR, de_DE)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    generate_data(
        output_file=args.output_file,
        number_of_rows=args.number_of_rows,
        chunksize=args.chunksize,
        locale=args.locale,
        seed=args.seed,
    )
