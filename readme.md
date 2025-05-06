Create a migration
`docker-compose exec web alembic revision --autogenerate -m "create text_summary table"`

Run migrations
`docker-compose exec web alembic upgrade head`

Run tests
`docker compose exec web python -m pytest -p no:warnings`

Insert dummy data
```
curl -X POST http://localhost:8004/summaries/ \
  -H "Content-Type: application/json" \
  -d '{"url": "http://testdriven.io"}'
{"url":"http://testdriven.io","id":2}%  
```