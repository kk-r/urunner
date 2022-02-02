# URunner Application
Sample application

## Requirements :pushpin:
- Docker
- docker-compose
- Python 3.6+ 

### Local Development

1. Clone this repo 
2  Create .env files `cp .env.example .env`
3. `docker-compose -f docker-compose.yml build`
4. `docker-compose -f docker-compose.yml up -d`
5. `docker exec -it users-app-api bash prestart.sh` `To run migration script`
6. `docker exec -it users-app-api python mysqlseed.py` `To seed test data into database`
7.  Api server is listen at http://localhost:8030/docs now.