# 🚇 Subway Surfers Game

A web-based endless runner game inspired by Subway Surfers, built with Python, NiceGUI, and FastAPI.

## ✨ Features

- **Endless Runner Gameplay**: Run automatically with smooth character movement
- **Intuitive Controls**: Use arrow keys to move left/right, jump, and slide
- **Obstacle Avoidance**: Dodge trains and barriers to keep running
- **Coin Collection**: Collect coins to increase your score
- **Score System**: Track your score, coins, and distance traveled
- **Leaderboard**: Compete with other players for high scores
- **Responsive Design**: Beautiful UI that works on different screen sizes
- **Real-time Statistics**: View game stats and performance metrics

## 🎮 How to Play

1. **Movement**: Use ← → arrow keys to move between lanes
2. **Jump**: Press ↑ arrow key or spacebar to jump over obstacles
3. **Slide**: Press ↓ arrow key to slide under barriers
4. **Collect Coins**: Run through gold coins to increase your score
5. **Avoid Obstacles**: Don't hit the red barriers or you'll crash!

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create data directory**:
   ```bash
   mkdir -p data logs
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

5. **Run the game**:
   ```bash
   python main.py
   ```

6. **Open your browser** and go to: `http://localhost:8080`

## 🎯 Game Controls

| Key | Action |
|-----|--------|
| ← → | Move left/right between lanes |
| ↑ or Space | Jump over obstacles |
| ↓ | Slide under barriers |

## 📊 Features Overview

### Game Mechanics
- **Automatic Running**: Character runs forward automatically
- **Lane System**: Three lanes to move between
- **Physics**: Realistic jumping and sliding mechanics
- **Progressive Difficulty**: Game speed increases over time
- **Collision Detection**: Accurate hit detection for obstacles and coins

### Scoring System
- **Distance Points**: Earn points for distance traveled
- **Coin Bonuses**: Extra points for collecting coins
- **High Score Tracking**: Automatic leaderboard updates
- **Statistics**: Track total games, coins, and distance

### Technical Features
- **Real-time Rendering**: Smooth 60fps gameplay using HTML5 Canvas
- **Database Integration**: SQLite database for persistent scores
- **RESTful API**: FastAPI backend for game data management
- **Responsive UI**: Modern web interface with NiceGUI
- **Error Handling**: Robust error handling and logging

## 🏗️ Project Structure

```
subway-surfers-game/
├── main.py                 # Application entry point
├── app/
│   ├── main.py            # NiceGUI page definitions
│   ├── core/              # Core application components
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── api/               # FastAPI endpoints
│   └── frontend/          # UI components
├── data/                  # Database files
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

The game can be configured through environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8080)
- `DEBUG`: Enable debug mode (default: false)
- `DATABASE_URL`: Database connection string
- `GAME_SPEED`: Initial game speed
- `SECRET_KEY`: Security key for sessions

## 📈 API Endpoints

- `GET /api/health` - Health check
- `POST /api/game/session` - Save game session
- `GET /api/game/high-scores` - Get leaderboard
- `GET /api/game/stats` - Get game statistics

## 🎨 Customization

### Game Settings
Modify game parameters in `app/core/config.py`:
- Spawn rates for obstacles and coins
- Game speed progression
- Player physics settings

### Visual Styling
Update CSS styles in `app/frontend/game_ui.py`:
- Color schemes
- UI layouts
- Animation effects

### Game Mechanics
Extend game logic in the JavaScript section:
- Add new obstacle types
- Implement power-ups
- Create special effects

## 🐛 Troubleshooting

### Common Issues

1. **Game won't start**: Check browser console for JavaScript errors
2. **Database errors**: Ensure `data/` directory exists and is writable
3. **Port conflicts**: Change the PORT in `.env` file
4. **Performance issues**: Close other browser tabs and applications

### Debug Mode

Enable debug mode by setting `DEBUG=true` in your `.env` file for detailed logging.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎉 Enjoy Playing!

Have fun playing Subway Surfers and try to beat the high score! 🏆

---

*Built with ❤️ using Python, NiceGUI, and FastAPI*