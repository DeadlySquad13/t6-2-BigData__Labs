# Big Data
## Apache Hadoop
Run:
```bash
make prepare-hadoop
make build-hadoop
make run-hadoop
```

Open admin panel in browser using `make open-hadoop-admin-panel`

> If you have problems opening site check if you have any Nginx settings
messing up you connection.

## Contributing
Created using Base with Docker Project bootstrap template
Has [Base template](https://github.com/dsOmega-bootstrap/Base.bootstrap) features and following:
- Simple Docker Makefile with QoL targets
- Docker .env for easier configurability of commands in aforementioned Makefile

### How to Use
See [.env.example](./.env.example). Copy it to `.env` and fill.

