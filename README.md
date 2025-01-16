# Crypto Tracker

A Django-based cryptocurrency tracking application that displays real-time information about various cryptocurrencies, including their prices, market caps, and 24-hour price changes.

## Features

- Real-time cryptocurrency data display
- Price change percentage with color indicators (green for positive, red for negative)
- Market cap information
- Clean and responsive UI
- Docker support for easy deployment

## Running with Docker

### Option 1: Pull from Docker Hub (Recommended)

The easiest way to run the application is to pull it directly from Docker Hub:

```bash
docker run -p 8000:8000 gusfuentes/crypto-tracker:latest
```

The application will be available at `http://localhost:8000`.

You can also specify a custom port by overriding the CMD:

```bash
docker run -p 3000:3000 gusfuentes/crypto-tracker:latest 0.0.0.0:3000
```

### Option 2: Build Locally

1. Clone the repository:
```bash
git clone https://github.com/Gus-Fuentes/crypto-tracker.git
cd crypto-tracker
```

2. Build the Docker image:
```bash
docker build -t crypto-tracker .
```

3. Run the container:
```bash
docker run -p 8000:8000 crypto-tracker
```

Or with a custom port:
```bash
docker run -p 3000:3000 crypto-tracker 0.0.0.0:3000
```

## Manual Installation (Without Docker)

If you prefer to run the application without Docker:

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

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`.

## Environment Variables

- `PORT`: Default port for the container (default: 8000)
- `DEBUG`: Enable/disable debug mode (default: True)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Usage

Visit `http://localhost:8000` in your web browser to view the cryptocurrency tracker.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
