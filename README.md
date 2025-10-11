
# AI-short-creator ✨

Edit:
I just want to say that I have started working on this project to Improve it so I would really appreciate if someone could help me with this project and if can't give time then atleast sponsor it (to talk to me you can DM me in discord username: shr33shc

AI-short-creator is an AI-powered tool that turns long videos into short clips. It works best for videos with multiple speakers and topics, such as interviews and documentaries. Clipster finds the most engaging parts of the video, adds captions and transitions, and makes the clips ready for social media.
<div align='center'>
  <img src="https://th.bing.com/th/id/OIG.DXZZsyt9aBRpjM2P6F5U?pid=ImgGn" alt="drawing" style="width:400px;"/>
</div>

# Result
https://private-user-images.githubusercontent.com/71629361/287322097-13fffb50-11e3-4c10-b52c-92897bd253ee.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDE0NDc3MjIsIm5iZiI6MTcwMTQ0NzQyMiwicGF0aCI6Ii83MTYyOTM2MS8yODczMjIwOTctMTNmZmZiNTAtMTFlMy00YzEwLWI1MmMtOTI4OTdiZDI1M2VlLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMDElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjAxVDE2MTcwMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTM1MmNlMzgwNGNjZjk1NGU5ZWIwZTdhNzUyZmRkOGY4YWFiNTU1ZTk1NmQ3MWY2YTYyMjViM2U1YThkNzVmM2YmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Y2FbJwnW-rzLkssM9MB9b4JVLHrFlo11N2OoLf73MFM

## Installation

### 🐳 Docker Installation (Recommended)

The easiest way to run AI-short-creator is using Docker. This method handles all dependencies automatically.

**Prerequisites:**
- Docker Desktop installed ([Download here](https://docker.com/products/docker-desktop))
- 4GB+ RAM available for Docker

**Quick Start:**
```bash
# Clone the repository
git clone <your-repo-url>
cd AI-short-creator

# Setup environment (for production mode)
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and YOUTUBE_URL

# Run with the simple script
./run.sh -t -d    # Test mode (uses mock data)
# OR
./run.sh -d       # Production mode (requires API keys)
```

**Simple Commands:**
```bash
./run.sh -t       # Test mode with mock data
./run.sh          # Production mode  
./run.sh -d       # Run in background
./run.sh -b       # Force rebuild
./run.sh -l       # Show logs
./run.sh -s       # Stop services
./run.sh -h       # Show help
```

**Direct Docker Commands:**
```bash
# Test mode (no API keys needed)
TEST_MODE=true docker-compose up --build

# Production mode
docker-compose up --build

# Background mode
docker-compose up -d --build

# Stop services
docker-compose down
```

**Access URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### 💻 Local Installation

For development without Docker:

Step 1: Install frontend packages
```bash
cd frontend
npm install
```

Step 2: Install Python packages
```bash
cd ..
# Using uv (recommended)
pip install uv
uv sync

# OR using pip
pip install -r requirements.txt
```

Step 3: Setup environment variables
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
OPENAI_API_KEY='Your openAI key'
YOUTUBE_URL='https://youtube.com/watch?v=your-video-id'
```

Step 4: Run system requirements check
```bash
uv run python backend/check_requirements.py
```

Step 5: Run the application
```bash
# Run complete pipeline
uv run python backend/main.py

# OR run in test mode
TEST_MODE=true uv run python backend/main.py
```

    
## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.

