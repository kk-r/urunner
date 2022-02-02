# URunner Application

## Requirements :pushpin:
- Docker :whale:
- docker-compose :whale:
- Python 3.6+ :snake:

### Local Development

1. Create .env files `cp .env.example .env`
2. `docker-compose -f docker-compose.yml build`
3. `docker-compose -f docker-compose.yml up -d`
3. `docker exec -it users-app-api bash prestart.sh` ``
3. `docker exec -it users-app-api python mysqlseed.py`
5. That's just all, api server is listen at http://localhost:8030/docs now

You will see the automatic interactive API documentation (provided by Swagger UI):
![Swagger UI](screenshots/ui.png)

## Testing  :rotating_light:

```python
    pytest -vvs src/tests/
```