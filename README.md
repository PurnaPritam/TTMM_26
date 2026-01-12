# Ten Minute Million (TTMM) - E-Cell IIT Bombay

## Overview

Ten Minute Million is a flagship startup pitching competition organized by the Entrepreneurship Cell (E-Cell) of IIT Bombay. This platform provides a digital solution for managing the competition, allowing startups to register, submit pitches, and enabling investors to bid on promising ventures.

## About Ten Minute Million

Ten Minute Million is a unique platform where startups get just **10 minutes** to pitch their ideas and secure funding from a panel of investors and venture capitalists. The event is part of E-Cell IIT Bombay's initiative to foster entrepreneurship and connect innovative startups with potential investors.

## What can you do here?

**If you're a startup founder:**
- Register your startup with detailed information
- Upload pitch decks and business plans
- Track which investors are interested
- See real-time bids during your pitch session
- Get notifications about investor activity

**If you're an investor:**
- Browse all registered startups
- Filter companies by industry, stage, or funding needs
- Place bids during live pitching sessions
- Access comprehensive startup details and metrics
- Track your bidding history

## What we built it with

We've used a modern, reliable tech stack:

**Backend:**
- Django for handling all server-side logic
- Django REST Framework for building the API
- SQLite for the database (can scale to PostgreSQL if needed)

**Frontend:**
- Angular for building the user interface
- TypeScript for type-safe code
- Modern component-based architecture

## How the code is organized

```
TTMM_26/
├── ttmm_26_backend/       # All the server-side code
│   ├── ttmm_26/           # Core app (models, views, API)
│   ├── manage.py          # Django's command-line tool
│   └── db.sqlite3         # Database
└── ttmm_26_frontend/      # All the Angular frontend code
```

## Getting it running locally

**Setting up the backend:**

1. Go to the backend folder:
   ```bash
   cd ttmm_26_backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

**Setting up the frontend:**

1. Go to the frontend folder:
   ```bash
   cd ttmm_26_frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   ng serve
   ```

## How the API works

The backend provides these main endpoints:

- `POST /api/startups/` - Register a new startup
- `GET /api/startups/` - Get all registered startups
- `GET /api/startups/{id}/` - Get details for a specific startup
- `POST /api/bids/` - Place a bid on a startup
- `GET /api/bids/` - View all bids

## About E-Cell IIT Bombay

E-Cell IIT Bombay is one of India's most prominent entrepreneurship cells. Through flagship events like Ten Minute Million and E-Summit, along with year-round workshops and mentorship programs, they've built an ecosystem that has nurtured hundreds of startups and connected countless entrepreneurs with investors, mentors, and resources.

## Want to contribute?

Found a bug or have an idea to improve this platform? Feel free to open a pull request or create an issue!

## Get in touch

For anything related to the Ten Minute Million competition:
- Website: [E-Cell IIT Bombay](https://www.ecell.in/)
- Email: contact@ecell.in

---

*Built for the Ten Minute Million competition by E-Cell IIT Bombay*
