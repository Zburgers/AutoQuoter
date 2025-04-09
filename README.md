# AutoQuoter

A SaaS web application that automatically generates high-quality quote images for Instagram pages, creators, and motivational influencers.

## Features

- Generate beautiful quote images with just a few clicks
- Select from different quote themes (Motivation, Stoicism, Success, etc.)
- Custom backgrounds and fonts for different themes
- Enter your own custom quotes
- Download generated images for sharing

## Project Structure

```
autoquoter/
│
├── frontend/            # Frontend files (HTML, CSS, JS)
│   ├── index.html       # Main UI file
│   ├── style.css        # Styles
│   └── script.js        # Frontend JavaScript
│
├── backend/             # Flask backend
│   ├── main.py          # Flask app entrypoint
│   ├── quote_fetcher.py # Quote API integration
│   ├── image_creator.py # Image generation
│   └── utils.py         # Helper functions
│
├── templates/           # Optional HTML templates
│
├── assets/              # Static assets
│   ├── backgrounds/     # Background images
│   └── fonts/           # Custom fonts
│
└── static/              # Generated content
    └── generated/       # Saved quote images
```

## Setup Instructions

### Prerequisites

- Python 3.8+ with pip
- Modern web browser

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/autoquoter.git
cd autoquoter
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Setup assets (optional if not included in repository)
```bash
python backend/generate_backgrounds.py
python backend/setup_fonts.py
```

### Running the Application

1. Start the Flask server:
```bash
python backend/main.py
```

2. Open your browser and visit:
```
http://localhost:5000
```

## API Reference

### Generate Quote Image

**POST /api/generate**

Generates a quote image based on the specified theme.

Request Body:
```json
{
  "theme": "motivation",
  "customQuote": "Your custom quote text (optional)",
  "removeWatermark": false
}
```

Response: PNG image file

### Get User Quota

**GET /api/quota**

Returns information about the user's remaining quota.

Response:
```json
{
  "remaining": 5,
  "limit": 5,
  "isPremium": false
}
```

## Monetization Plan

| Tier     | Features                       | Price   |
|----------|--------------------------------|---------|
| Free     | 5 quotes/day, watermark        | $0      |
| Premium  | Unlimited quotes, no watermark | $5/mo   |
| Custom   | Brand quote packs + scheduler  | $9+/mo  |

## Future Enhancements

- User accounts and authentication
- Scheduler for auto-posting to social media
- More background and font options
- Video quote generation
- Admin panel for monitoring usage

## License

This project is licensed under the MIT License - see the LICENSE file for details.