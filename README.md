# Crypto Tracker

A Django-based cryptocurrency tracking application that displays real-time information about various cryptocurrencies, including their prices, market caps, and 24-hour price changes.

## Features

- Real-time cryptocurrency data display
- Price change percentage with color indicators (green for positive, red for negative)
- Market cap information
- Clean and responsive UI
- Docker support for easy deployment

## Quick Start with Docker Compose

The application requires PostgreSQL and Redis services, so the easiest way to run it is using Docker Compose:

1. Clone the repository:
```bash
git clone https://github.com/Gus-Fuentes/crypto-tracker.git
cd crypto-tracker
```

2. Start all services:
```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`.

3. Create an admin user (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

## Manual Installation (Without Docker)

If you prefer to run the application without Docker, you'll need to have PostgreSQL and Redis installed locally:

1. Clone the repository:
```bash
git clone https://github.com/Gus-Fuentes/crypto-tracker.git
cd crypto-tracker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your PostgreSQL database and update settings.py with your database credentials

5. Start Redis locally (installation depends on your OS)

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`.

## Environment Variables

- `DEBUG`: Enable/disable debug mode (default: True)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `POSTGRES_DB`: PostgreSQL database name (default: postgres)
- `POSTGRES_USER`: PostgreSQL username (default: postgres)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: postgres)
- `REDIS_URL`: Redis connection URL (default: redis://redis:6379/1)

## Common Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart the web application
docker-compose restart web

# Run database migrations
docker-compose exec web python manage.py migrate
```

## Troubleshooting

If the market data isn't showing:
1. Make sure all services are running:
```bash
docker-compose ps
```

2. Check the logs for errors:
```bash
docker-compose logs
```

3. Restart the services:
```bash
docker-compose restart
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
