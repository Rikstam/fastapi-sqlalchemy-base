Create a migration
`docker-compose exec web alembic revision --autogenerate -m "create text_summary table"`

Run migrations
`docker-compose exec web alembic upgrade head`