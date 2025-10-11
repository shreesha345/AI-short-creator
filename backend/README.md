# AI Short Creator - Backend

This is the backend system for AI Short Creator, an AI-powered tool that transforms long YouTube videos into engaging short clips with automatic face tracking and viral content detection.

## 🚀 Features

- **YouTube Video Download**: Automatically downloads videos with audio
- **AI-Powered Analysis**: Uses OpenAI GPT to identify viral segments
- **Automatic Subtitle Generation**: Extracts and generates accurate subtitles
- **Smart Face Detection**: MTCNN-based face tracking with smooth camera movement
- **Video Processing**: Cuts, crops, and combines clips into final short videos
- **Batch Processing**: Handles multiple clips efficiently with multiprocessing

## 📋 Prerequisites

### System Requirements

- **Python**: 3.12+ (required)
- **FFmpeg**: For video processing
- **Operating System**: macOS, Linux, or Windows
- **Memory**: At least 8GB RAM (16GB+ recommended for large videos)
- **Storage**: 2GB+ free space for temporary files

### External Dependencies

#### macOS
```bash
# Install FFmpeg
brew install ffmpeg

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Ubuntu/Debian
```bash
# Install FFmpeg
sudo apt update
sudo apt install ffmpeg

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
1. Download and install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add FFmpeg to your system PATH
3. Install uv: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd AI-short-creator
```

### 2. Install Python Dependencies
```bash
# Sync all dependencies using uv
uv sync

# Alternative: Install specific dependencies
uv add moviepy mtcnn numpy openai opencv-python pydub python-dotenv pytube tensorflow tqdm
```

### 3. Set Up Environment Variables
```bash
# Copy the example environment file
cp .copy.env .env

# Edit the .env file with your actual values
nano .env
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- `YOUTUBE_URL`: URL of the YouTube video you want to process

Optional environment variables:
- `OPENAI_MODEL`: OpenAI model to use (default: `gpt-3.5-turbo-16k`)
- `TEST_MODE`: Set to `true` to use mock data instead of OpenAI API

### 4. Verify Installation
```bash
# Run the system requirements check
uv run python backend/check_requirements.py
```

This will verify that:
- ✅ Python version is compatible
- ✅ All packages are installed correctly
- ✅ System commands (ffmpeg) are available
- ✅ Environment variables are set
- ✅ Directory structure is correct
- ✅ Basic functionality works

## 🎯 Usage

### Quick Start
```bash
# Run the complete pipeline
uv run python backend/main.py
```

### Step-by-Step Execution

You can also run individual components:

```bash
# 1. Download video and generate subtitles
uv run python backend/video/downloader.py

# 2. Analyze transcript for viral content
uv run python backend/transcript_analyzer.py

# 3. Cut video into clips
uv run python backend/video/cutter.py

# 4. Apply face detection and tracking
uv run python backend/face_detector.py

# 5. Combine clips into final video
uv run python backend/video/processor.py
```

### Development Mode

For development and testing:

```bash
# Use test mode (no OpenAI API calls)
export TEST_MODE=true
uv run python backend/main.py

# Run with verbose logging
export LOG_LEVEL=DEBUG
uv run python backend/main.py
```

## 📁 Project Structure

```
backend/
├── __init__.py                 # Package initialization
├── main.py                     # Main pipeline orchestrator
├── check_requirements.py       # System requirements checker
├── face_detector.py           # Face detection and tracking
├── transcript_analyzer.py     # AI-powered transcript analysis
└── video/
    ├── __init__.py            # Video package initialization
    ├── downloader.py          # YouTube video downloader
    ├── cutter.py              # Video clip extraction
    └── processor.py           # Final video assembly

data/                          # Data directory (auto-created)
├── input/                     # Input files
│   ├── raw_video/            # Downloaded video and audio
│   ├── main_part.json        # AI analysis results
│   └── mock_main_part.json   # Test data
└── output/                    # Generated content
    ├── clips/                # Individual video clips
    ├── final_clips/          # Processed clips with face tracking
    └── final_video/          # Final combined video
```

## ⚙️ Configuration

### Face Detection Parameters

Edit `face_detector.py` to customize face tracking:

```python
FACE_DETECTION_FREQUENCY = 7    # Detect face every N frames
RESIZE_RATIO = 0.25             # Downscale for faster detection
MOVEMENT_SPEED = 0.06           # Camera following speed
SMOOTHING_FACTOR = 0.3          # Movement smoothing
PREDICTION_WEIGHT = 0.5         # Face position prediction
```

### Video Processing Settings

Edit `video/cutter.py` and `video/processor.py` for video settings:

```python
# Output video codec and quality settings
codec="libx264"           # H.264 codec
audio_codec="aac"         # AAC audio codec
```

## 🔧 Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found
```bash
# Error: ffmpeg command not found
# Solution: Install FFmpeg for your system (see Prerequisites)
```

#### 2. OpenAI API Issues
```bash
# Error: OpenAI API key not set
# Solution: Set OPENAI_API_KEY in your .env file

# Error: OpenAI API rate limit
# Solution: Wait or upgrade your OpenAI plan
```

#### 3. Memory Issues
```bash
# Error: Out of memory during video processing
# Solution: Process smaller videos or increase system RAM
# Alternative: Reduce FACE_DETECTION_FREQUENCY or RESIZE_RATIO
```

#### 4. Python Version Issues
```bash
# Error: Python version too old
# Solution: Install Python 3.12+
# Check: python --version
```

#### 5. Package Installation Issues
```bash
# Error: Package installation failed
# Solution: Try installing individually
uv add moviepy
uv add opencv-python
uv add tensorflow
```

### Debug Mode

Enable detailed logging:

```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Run with debug output
uv run python backend/main.py
```

### Performance Optimization

For better performance:

1. **Use SSD storage** for faster I/O operations
2. **Increase CPU cores** - face detection uses all available cores
3. **GPU acceleration** - Install `tensorflow-gpu` if you have a compatible GPU
4. **Reduce video resolution** - Process 720p instead of 1080p videos

## 🧪 Testing

### Run System Tests
```bash
# Comprehensive system check
uv run python backend/check_requirements.py

# Test with mock data (no API calls)
TEST_MODE=true uv run python backend/main.py
```

### Create Mock Data

For testing without OpenAI API calls, create `data/input/mock_main_part.json`:

```json
[
  {
    "start_time": 10.0,
    "end_time": 65.0,
    "description": "Interesting discussion about AI",
    "duration": 55.0
  },
  {
    "start_time": 120.0,
    "end_time": 175.0,
    "description": "Viral moment with great insights",
    "duration": 55.0
  }
]
```

## 📚 Development

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make changes** and add tests
4. **Run the system check**: `uv run python backend/check_requirements.py`
5. **Test your changes**: `uv run python backend/main.py`
6. **Submit a pull request**

### Code Style

- Follow PEP 8 standards
- Add docstrings to all functions
- Include error handling and logging
- Use type hints where possible

### Dependencies Management

```bash
# Add new dependency
uv add package-name

# Remove dependency
uv remove package-name

# Update all dependencies
uv sync --upgrade

# Export requirements for other tools
uv export > requirements.txt
```

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Run the requirements checker**: `uv run python backend/check_requirements.py`
3. **Enable debug logging** to get more information
4. **Check that all environment variables are set correctly**
5. **Ensure your OpenAI API key has sufficient credits**

## 📝 License

[Add your license information here]

---

**Happy video creating! 🎬✨**
