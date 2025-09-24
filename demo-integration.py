#!/usr/bin/env python3
"""
Demo script showing how to generate math files and prepare for web SDK integration.
This demonstrates the complete flow from Math SDK to Web SDK.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_game_simulation(game_name: str) -> bool:
    """Run a game simulation and generate math files."""
    game_path = Path(f'games/{game_name}')
    run_file = game_path / 'run.py'
    
    if not run_file.exists():
        print(f"❌ Game '{game_name}' not found at {game_path}")
        return False
    
    print(f"🎰 Running simulation for {game_name}...")
    
    try:
        # Change to game directory and run the simulation
        original_cwd = os.getcwd()
        os.chdir(game_path)
        
        result = subprocess.run([sys.executable, 'run.py'], 
                              capture_output=True, text=True, timeout=60)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print(f"✅ Simulation completed successfully for {game_name}")
            return True
        else:
            print(f"❌ Simulation failed for {game_name}")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Simulation timed out for {game_name}")
        return False
    except Exception as e:
        print(f"❌ Error running simulation: {e}")
        return False

def check_generated_files(game_name: str) -> bool:
    """Check if the required files were generated."""
    library_path = Path(f'games/{game_name}/library')
    publish_path = library_path / 'publish_files'
    
    required_files = [
        'index.json',
        # Either compressed or uncompressed books
        # Either compressed or uncompressed lookup tables
    ]
    
    if not publish_path.exists():
        print(f"❌ Publish directory not found: {publish_path}")
        return False
    
    # Check for books files (either compressed or uncompressed)
    books_files = list(publish_path.glob('books_*.jsonl*'))
    lookup_files = list(publish_path.glob('lookUpTable*.csv'))
    index_file = publish_path / 'index.json'
    
    if not books_files:
        print(f"❌ No books files found in {publish_path}")
        return False
        
    if not lookup_files:
        print(f"❌ No lookup table files found in {publish_path}")
        return False
        
    if not index_file.exists():
        print(f"❌ index.json not found in {publish_path}")
        return False
    
    print(f"✅ Generated files found:")
    for file in books_files + lookup_files + [index_file]:
        file_size = file.stat().st_size
        print(f"   📄 {file.name} ({file_size:,} bytes)")
    
    return True

def show_web_sdk_integration_info():
    """Show information about how to integrate with the Web SDK."""
    print("\n🌐 Web SDK Integration:")
    print("1. Deploy the generated files to your RGS server:")
    print("   - Upload files from games/{game}/library/publish_files/")
    print("   - Configure RGS to serve these files")
    
    print("\n2. Use the Web SDK in your frontend:")
    print("   - Import: import { GameController } from '@stake-engine/web-sdk'")
    print("   - Initialize with RGS URL and session ID")
    print("   - Use GameController.placeBet() and endRound() methods")
    
    print("\n3. Run the simple game example:")
    print("   cd web-sdk/examples/simple-game")
    print("   npm install && npm run dev")
    print("   Open with URL parameters: ?rgs_url=your-server&sessionID=test")

def main():
    """Main demo function."""
    print("🚀 Stake Engine Math SDK to Web SDK Integration Demo")
    print("=" * 60)
    
    # List available games
    games_dir = Path('games')
    if not games_dir.exists():
        print("❌ Games directory not found")
        return
    
    available_games = [d.name for d in games_dir.iterdir() 
                      if d.is_dir() and (d / 'run.py').exists()]
    
    if not available_games:
        print("❌ No games with run.py found")
        return
    
    print(f"📋 Available games: {', '.join(available_games)}")
    
    # Default to fifty_fifty if available, otherwise first game
    demo_game = 'fifty_fifty' if 'fifty_fifty' in available_games else available_games[0]
    print(f"🎯 Using '{demo_game}' for demo")
    
    # Run simulation
    if not run_game_simulation(demo_game):
        return
    
    # Check generated files
    if not check_generated_files(demo_game):
        return
    
    # Show integration info
    show_web_sdk_integration_info()
    
    print("\n✅ Demo completed successfully!")
    print("🔗 Your math files are ready for RGS deployment")
    print("🎮 Your web frontend can use the Web SDK for integration")

if __name__ == '__main__':
    main()