Create a migration
`docker-compose exec web alembic revision --autogenerate -m "create text_summary table"`

Run migrations
`docker-compose exec web alembic upgrade head`

Run tests
`docker compose exec web python -m pytest -p no:warnings`

Insert dummy data

curl -X POST http://localhost:8004/summaries/ \
  -H "Content-Type: application/json" \
  -d '{"url": "http://testdriven.io"}'
{"url":"http://testdriven.io","id":2}%  


normal run
`docker compose exec web python -m pytest`

# disable warnings
`docker compose exec web python -m pytest -p no:warnings`

# run only the last failed tests
`docker compose exec web python -m pytest --lf`

# run only the tests with names that match the string expression
`docker compose exec web python -m pytest -k "summary and not test_read_summary"`

# stop the test session after the first failure
`docker compose exec web python -m pytest -x`

# enter PDB after first failure then end the test session
`docker compose exec web python -m pytest -x --pdb`

# stop the test run after two failures
`docker compose exec web python -m pytest --maxfail=2`

# show local variables in tracebacks
`docker compose exec web python -m pytest -l`

# list the 2 slowest tests
`docker compose exec web python -m pytest --durations=2`

# with coverage
`docker compose exec web python -m pytest --cov="."`

# coverage html report
`docker compose exec web python -m pytest --cov="." --cov-report html`

![Continuous Integration and Delivery](https://github.com/Rikstam/fastapi-sqlalchemy-base/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)