<!-- toc -->

# Big Data
## 1. MapReduce Concept using built-in methods.
### Generating Big Data
Run `generate-data` script, for example:
```py
# Generate 1 million rows in ./data/test.csv
pixi run generate-data ./data/test.csv --number_of_rows 10000000

# Generate array of test files in ./data directory with rows specified in
# array `rows`:
rows=( 100 1000 10000 100000 1000000 2000000 3000000 4000000 5000000 )
for i in "${rows[@]}"; do pixi run generate-data ./data/"test-$i.csv" --number_of_rows "$i"; done
```

To see full list of options use help:
```py
pixi run generate-data --help
```

### Get Statistics
```bash
pixi run thread-pool-executer ./data/test-1000000.csv
# Or
pixi run thread-pool-executer ./data/test-1000000.csv --top_n 10 --chunsize 10000
```

To see full list of options use help:
```py
pixi run thread-pool-executer --help
```

## 2. Apache Hadoop
Uses Docker paired with .env and .env.dev extensively for configuration.
Check [.env.example](./.env.example) and
[.env.dev.example](./.env.dev.example).

Run:
```bash
# Or `make run-hadoop` to see logs in real-time.
make start-hadoop # Will run detached.
```

Open admin panel in browser using `make open-hadoop-admin-panel` or
connect in terminal: `make connect`.

Both `run-hadoop` and `start-hadoop` will create a volume connecting:
- [data folder on host](./data) and `/home/hduser/data` in container.
- [scripts folder on host](./scripts) and `/home/hduser/scripts` in container.

> If you have problems opening site check if you have any Nginx settings
messing up you connection.

> [!warning] Not suitable as is for production environment.
> See `$HADOOP_HOME/etc/hadoop/hdfs-site.xml` (or in admin panel go to Utilities/Configuration):
> dfs.permissions
>   false

Execute Map & Reduce using `execute-hadoop-map-reduce`. It will iterate through
all the "data/test-*.csv" using hdfs map&reduce mechanism to count words. It
will count time elapsed for each dataset. Check [script](./scripts/hadoop-map-reduce.sh)
and [mapper](./scripts/mapper.py) & [reducer](./scripts/reducer.py) implementations for more details.

## 3. Apache Spark
Everything the same as in [2. Apache Hadoop](<README#2. Apache Hadoop>) if not stated otherwise, just change "hadoop"
to "spark". Also uses .env and .env.dev, check their respective example files.
For more precise configuration check out [Spark's .env example](./Apache__Spark/.env.example).

For example, to get started run:
```bash
# Or `make run-spark` to see logs in real-time.
make start-spark # Will run detached.
```

Both `run-spark` and `start-spark` will create a volume connecting:
- [data folder on host](./data) and `/opt/spark/data` in container.
- [scripts folder on host](./scripts) and `/opt/spark/scripts` in container.

Just as Hadoop uses `execute-spark-map-reduce` target. Check [script](./scripts/spark-map-reduce.sh)
and [Python implementation](./scripts/spark-map-reduce.py) for more details.

## Contributing
Created using Base with Docker Project bootstrap template
Has [Base template](https://github.com/dsOmega-bootstrap/Base.bootstrap) features and following:
- Simple Docker Makefile with QoL targets
- Docker .env for easier configurability of commands in aforementioned Makefile

### How to Use
See [.env.example](./.env.example). Copy it to `.env` and fill.

## Contributing
See guidelines in [Contributing](./CONTRIBUTING.md). This projects also
has Docker support, see ["Running in Docker"
section in Contributing](./CONTRIBUTING.md#running-in-docker).
