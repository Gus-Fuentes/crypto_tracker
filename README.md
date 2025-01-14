# Crypto Tracker

A Django-based cryptocurrency tracking application that displays real-time information about various cryptocurrencies, including their prices, market caps, and 24-hour price changes.

## Features

- Real-time cryptocurrency data display
- Price change percentage with color indicators (green for positive, red for negative)
- Market cap information
- Clean and responsive UI

## Prerequisites

- Python 3.8+
- Django
- requests library

## Installation

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
