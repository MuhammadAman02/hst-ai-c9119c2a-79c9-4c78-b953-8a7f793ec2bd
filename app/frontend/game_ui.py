"""Main game UI using NiceGUI"""
from nicegui import ui
import asyncio
import json
from typing import Dict, Any
from app.core.logging import app_logger

class GameUI:
    """Main game user interface"""
    
    def __init__(self):
        self.game_state = {
            'score': 0,
            'coins': 0,
            'distance': 0,
            'is_playing': False,
            'is_paused': False,
            'player_name': 'Anonymous'
        }
    
    async def create_game_page(self):
        """Create the main game page"""
        # Custom CSS for game styling
        ui.add_head_html('''
            <style>
                .game-container {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .game-canvas {
                    border: 3px solid #fff;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%);
                }
                .game-ui {
                    background: rgba(255,255,255,0.9);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
                .score-display {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    text-align: center;
                }
                .game-button {
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    border: none;
                    color: white;
                    padding: 15px 30px;
                    font-size: 18px;
                    border-radius: 25px;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                .game-button:hover {
                    transform: scale(1.05);
                }
                .controls-info {
                    background: rgba(255,255,255,0.8);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                }
            </style>
        ''')
        
        with ui.column().classes('game-container w-full'):
            # Game title
            ui.label('🚇 Subway Surfers').classes('text-4xl font-bold text-white text-center mb-4')
            
            with ui.row().classes('w-full justify-center'):
                # Game canvas and controls
                with ui.column().classes('items-center'):
                    # Player name input
                    with ui.card().classes('game-ui'):
                        ui.label('Enter Your Name:').classes('text-lg font-semibold')
                        name_input = ui.input('Player Name', value='Anonymous').classes('w-full')
                        name_input.on('change', lambda e: self.update_player_name(e.value))
                    
                    # Game canvas
                    canvas = ui.html('''
                        <canvas id="gameCanvas" width="800" height="600" class="game-canvas"></canvas>
                    ''')
                    
                    # Game controls
                    with ui.card().classes('game-ui'):
                        with ui.row().classes('justify-center gap-4'):
                            start_btn = ui.button('🎮 Start Game', on_click=self.start_game).classes('game-button')
                            pause_btn = ui.button('⏸️ Pause', on_click=self.pause_game).classes('game-button')
                            restart_btn = ui.button('🔄 Restart', on_click=self.restart_game).classes('game-button')
                    
                    # Controls info
                    with ui.card().classes('controls-info'):
                        ui.label('🎮 Controls:').classes('text-lg font-bold mb-2')
                        ui.label('← → Arrow Keys: Move Left/Right')
                        ui.label('↑ Arrow Key or Space: Jump')
                        ui.label('↓ Arrow Key: Slide')
                
                # Score panel
                with ui.card().classes('game-ui ml-4'):
                    ui.label('📊 Game Stats').classes('text-xl font-bold text-center mb-4')
                    
                    self.score_label = ui.label('Score: 0').classes('score-display')
                    self.coins_label = ui.label('Coins: 0').classes('score-display')
                    self.distance_label = ui.label('Distance: 0m').classes('score-display')
                    
                    ui.separator()
                    
                    # Navigation buttons
                    ui.button('🏆 Leaderboard', on_click=lambda: ui.navigate.to('/leaderboard')).classes('w-full mt-4')
        
        # Add the game JavaScript
        await self.add_game_script()
    
    async def create_leaderboard_page(self):
        """Create the leaderboard page"""
        with ui.column().classes('game-container w-full'):
            ui.label('🏆 Leaderboard').classes('text-4xl font-bold text-white text-center mb-4')
            
            with ui.card().classes('game-ui max-w-4xl mx-auto'):
                # Fetch and display high scores
                try:
                    import httpx
                    async with httpx.AsyncClient() as client:
                        response = await client.get('http://localhost:8080/api/game/high-scores')
                        if response.status_code == 200:
                            high_scores = response.json()
                            
                            if high_scores:
                                with ui.table().classes('w-full'):
                                    ui.table_row().classes('bg-gray-100'):
                                        ui.table_cell('Rank').classes('font-bold')
                                        ui.table_cell('Player').classes('font-bold')
                                        ui.table_cell('Score').classes('font-bold')
                                        ui.table_cell('Coins').classes('font-bold')
                                        ui.table_cell('Distance').classes('font-bold')
                                        ui.table_cell('Date').classes('font-bold')
                                    
                                    for i, score in enumerate(high_scores, 1):
                                        with ui.table_row():
                                            ui.table_cell(f"#{i}")
                                            ui.table_cell(score['player_name'])
                                            ui.table_cell(f"{score['score']:,}")
                                            ui.table_cell(f"{score['coins_collected']:,}")
                                            ui.table_cell(f"{score['distance']:.1f}m")
                                            ui.table_cell(score['created_at'][:10])
                            else:
                                ui.label('No high scores yet! Be the first to play!').classes('text-center text-lg')
                        else:
                            ui.label('Error loading leaderboard').classes('text-red-500 text-center')
                except Exception as e:
                    app_logger.error(f"Error loading leaderboard: {e}")
                    ui.label('Error loading leaderboard').classes('text-red-500 text-center')
                
                ui.button('🎮 Back to Game', on_click=lambda: ui.navigate.to('/')).classes('w-full mt-4 game-button')
    
    def update_player_name(self, name: str):
        """Update player name"""
        self.game_state['player_name'] = name or 'Anonymous'
    
    async def start_game(self):
        """Start the game"""
        self.game_state['is_playing'] = True
        self.game_state['is_paused'] = False
        await ui.run_javascript('startGame()')
    
    async def pause_game(self):
        """Pause/unpause the game"""
        self.game_state['is_paused'] = not self.game_state['is_paused']
        await ui.run_javascript(f'pauseGame({str(self.game_state["is_paused"]).lower()})')
    
    async def restart_game(self):
        """Restart the game"""
        self.game_state = {
            'score': 0,
            'coins': 0,
            'distance': 0,
            'is_playing': False,
            'is_paused': False,
            'player_name': self.game_state['player_name']
        }
        await ui.run_javascript('restartGame()')
        self.update_ui()
    
    def update_ui(self):
        """Update the UI with current game state"""
        if hasattr(self, 'score_label'):
            self.score_label.text = f"Score: {self.game_state['score']:,}"
            self.coins_label.text = f"Coins: {self.game_state['coins']:,}"
            self.distance_label.text = f"Distance: {self.game_state['distance']:.1f}m"
    
    async def add_game_script(self):
        """Add the game JavaScript code"""
        game_script = '''
        <script>
        // Game variables
        let canvas, ctx;
        let gameState = {
            isPlaying: false,
            isPaused: false,
            score: 0,
            coins: 0,
            distance: 0,
            speed: 5
        };
        
        let player = {
            x: 100,
            y: 400,
            width: 40,
            height: 60,
            velocityY: 0,
            isJumping: false,
            isSliding: false,
            lane: 1 // 0=left, 1=center, 2=right
        };
        
        let obstacles = [];
        let coins = [];
        let powerups = [];
        let keys = {};
        
        // Initialize game
        function initGame() {
            canvas = document.getElementById('gameCanvas');
            if (!canvas) return;
            
            ctx = canvas.getContext('2d');
            
            // Event listeners
            document.addEventListener('keydown', handleKeyDown);
            document.addEventListener('keyup', handleKeyUp);
            
            // Start game loop
            gameLoop();
        }
        
        function handleKeyDown(e) {
            keys[e.code] = true;
            
            if (!gameState.isPlaying || gameState.isPaused) return;
            
            switch(e.code) {
                case 'ArrowLeft':
                    if (player.lane > 0) {
                        player.lane--;
                        player.x = 100 + player.lane * 200;
                    }
                    break;
                case 'ArrowRight':
                    if (player.lane < 2) {
                        player.lane++;
                        player.x = 100 + player.lane * 200;
                    }
                    break;
                case 'ArrowUp':
                case 'Space':
                    if (!player.isJumping && !player.isSliding) {
                        player.isJumping = true;
                        player.velocityY = -15;
                    }
                    break;
                case 'ArrowDown':
                    if (!player.isJumping) {
                        player.isSliding = true;
                        setTimeout(() => player.isSliding = false, 500);
                    }
                    break;
            }
            e.preventDefault();
        }
        
        function handleKeyUp(e) {
            keys[e.code] = false;
        }
        
        function startGame() {
            gameState.isPlaying = true;
            gameState.isPaused = false;
            gameState.score = 0;
            gameState.coins = 0;
            gameState.distance = 0;
            gameState.speed = 5;
            
            // Reset player
            player.x = 300;
            player.y = 400;
            player.lane = 1;
            player.velocityY = 0;
            player.isJumping = false;
            player.isSliding = false;
            
            // Clear arrays
            obstacles = [];
            coins = [];
            powerups = [];
        }
        
        function pauseGame(paused) {
            gameState.isPaused = paused;
        }
        
        function restartGame() {
            startGame();
        }
        
        function gameLoop() {
            update();
            render();
            requestAnimationFrame(gameLoop);
        }
        
        function update() {
            if (!gameState.isPlaying || gameState.isPaused) return;
            
            // Update distance and score
            gameState.distance += gameState.speed * 0.1;
            gameState.score += Math.floor(gameState.speed);
            
            // Increase speed gradually
            gameState.speed += 0.001;
            
            // Update player physics
            if (player.isJumping) {
                player.velocityY += 0.8; // gravity
                player.y += player.velocityY;
                
                if (player.y >= 400) {
                    player.y = 400;
                    player.isJumping = false;
                    player.velocityY = 0;
                }
            }
            
            // Spawn obstacles
            if (Math.random() < 0.02) {
                obstacles.push({
                    x: canvas.width,
                    y: 420,
                    width: 40,
                    height: 80,
                    lane: Math.floor(Math.random() * 3)
                });
            }
            
            // Spawn coins
            if (Math.random() < 0.03) {
                coins.push({
                    x: canvas.width,
                    y: 350 + Math.random() * 100,
                    width: 20,
                    height: 20,
                    lane: Math.floor(Math.random() * 3)
                });
            }
            
            // Update obstacles
            obstacles = obstacles.filter(obstacle => {
                obstacle.x -= gameState.speed;
                return obstacle.x > -obstacle.width;
            });
            
            // Update coins
            coins = coins.filter(coin => {
                coin.x -= gameState.speed;
                return coin.x > -coin.width;
            });
            
            // Check collisions
            checkCollisions();
            
            // Update UI
            updateGameUI();
        }
        
        function checkCollisions() {
            // Check obstacle collisions
            obstacles.forEach(obstacle => {
                if (obstacle.lane === player.lane &&
                    player.x < obstacle.x + obstacle.width &&
                    player.x + player.width > obstacle.x &&
                    player.y < obstacle.y + obstacle.height &&
                    player.y + player.height > obstacle.y &&
                    !player.isSliding) {
                    gameOver();
                }
            });
            
            // Check coin collisions
            coins = coins.filter(coin => {
                if (coin.lane === player.lane &&
                    player.x < coin.x + coin.width &&
                    player.x + player.width > coin.x &&
                    player.y < coin.y + coin.height &&
                    player.y + player.height > coin.y) {
                    gameState.coins++;
                    gameState.score += 10;
                    return false;
                }
                return true;
            });
        }
        
        function gameOver() {
            gameState.isPlaying = false;
            
            // Save game session
            fetch('/api/game/session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    player_name: 'Anonymous',
                    score: gameState.score,
                    coins_collected: gameState.coins,
                    distance: gameState.distance,
                    duration: Date.now() / 1000
                })
            }).catch(console.error);
            
            alert(`Game Over!\\nScore: ${gameState.score}\\nCoins: ${gameState.coins}\\nDistance: ${gameState.distance.toFixed(1)}m`);
        }
        
        function render() {
            if (!ctx) return;
            
            // Clear canvas
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw ground
            ctx.fillStyle = '#90EE90';
            ctx.fillRect(0, 500, canvas.width, 100);
            
            // Draw lanes
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.setLineDash([10, 10]);
            for (let i = 1; i < 3; i++) {
                ctx.beginPath();
                ctx.moveTo(100 + i * 200, 0);
                ctx.lineTo(100 + i * 200, canvas.height);
                ctx.stroke();
            }
            ctx.setLineDash([]);
            
            // Draw player
            ctx.fillStyle = player.isSliding ? '#FF6B6B' : '#4ECDC4';
            let playerHeight = player.isSliding ? 30 : 60;
            let playerY = player.isSliding ? player.y + 30 : player.y;
            ctx.fillRect(player.x, playerY, player.width, playerHeight);
            
            // Draw obstacles
            ctx.fillStyle = '#FF4444';
            obstacles.forEach(obstacle => {
                let obstacleX = 100 + obstacle.lane * 200;
                ctx.fillRect(obstacleX, obstacle.y, obstacle.width, obstacle.height);
            });
            
            // Draw coins
            ctx.fillStyle = '#FFD700';
            coins.forEach(coin => {
                let coinX = 100 + coin.lane * 200 + 10;
                ctx.beginPath();
                ctx.arc(coinX + coin.width/2, coin.y + coin.height/2, coin.width/2, 0, Math.PI * 2);
                ctx.fill();
            });
            
            // Draw game info
            if (!gameState.isPlaying) {
                ctx.fillStyle = 'rgba(0,0,0,0.7)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#fff';
                ctx.font = '48px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('Subway Surfers', canvas.width/2, canvas.height/2 - 50);
                
                ctx.font = '24px Arial';
                ctx.fillText('Press Start Game to begin!', canvas.width/2, canvas.height/2 + 20);
                ctx.fillText('Use arrow keys to move and jump', canvas.width/2, canvas.height/2 + 60);
            }
            
            if (gameState.isPaused) {
                ctx.fillStyle = 'rgba(0,0,0,0.5)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#fff';
                ctx.font = '48px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('PAUSED', canvas.width/2, canvas.height/2);
            }
        }
        
        function updateGameUI() {
            // This would be called from Python to update the UI
            // For now, we'll just log the values
            if (gameState.isPlaying) {
                console.log(`Score: ${gameState.score}, Coins: ${gameState.coins}, Distance: ${gameState.distance.toFixed(1)}m`);
            }
        }
        
        // Initialize when DOM is loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initGame);
        } else {
            initGame();
        }
        </script>
        '''
        
        ui.add_head_html(game_script)