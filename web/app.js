// DOM Elements
const generateButton = document.getElementById('generate-button');
const gameName = document.getElementById('game-name');
const gameDescription = document.getElementById('game-description');
const gameInfo = document.getElementById('game-info');
const difficultySelect = document.getElementById('difficulty-select');
const durationSelect = document.getElementById('duration-select');
const typeSelect = document.getElementById('type-select');
const historyButton = document.getElementById('history-button');
const historyList = document.getElementById('history-list');
let historyModal;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Bootstrap components
    initializeBootstrapComponents();
    
    // Load history from local storage if available
    loadHistory();
    
    // Generate a random game on initial load
    generateGame();
    
    // Event listeners
    generateButton.addEventListener('click', generateGame);
    historyButton.addEventListener('click', showHistory);
});

// Initialize Bootstrap components 
function initializeBootstrapComponents() {
    try {
        // Initialize the modal
        const modalElement = document.getElementById('history-modal');
        if (modalElement) {
            historyModal = new bootstrap.Modal(modalElement);
        } else {
            console.error('History modal element not found');
        }
    } catch (error) {
        console.error('Error initializing Bootstrap components:', error);
    }
}

// Generate a random game based on filters
function generateGame() {
    // Get selected filter values
    const difficulty = difficultySelect.value;
    const maxDuration = durationSelect.value;
    const type = typeSelect.value;
    
    // Filter games
    let filteredGames = DOG_GAMES.slice(); // Create a copy of the games array
    
    if (difficulty !== 'Alle') {
        filteredGames = filteredGames.filter(game => game.difficulty === difficulty);
    }
    
    if (maxDuration !== 'Alle') {
        filteredGames = filteredGames.filter(game => {
            // Extract the first number from the duration string (e.g., "5-10 minuten" -> 5)
            const gameDuration = parseInt(game.duration.split('-')[0]);
            return gameDuration <= parseInt(maxDuration);
        });
    }
    
    if (type !== 'Alle') {
        filteredGames = filteredGames.filter(game => game.type === type);
    }
    
    // If no games match the criteria
    if (filteredGames.length === 0) {
        gameName.textContent = '🤔 Geen spelletjes gevonden met deze criteria!';
        gameDescription.textContent = '';
        gameInfo.textContent = '';
        return;
    }
    
    // Select a random game from filtered list
    const randomIndex = Math.floor(Math.random() * filteredGames.length);
    const selectedGame = filteredGames[randomIndex];
    
    // Update the UI
    gameName.textContent = `🎯 ${selectedGame.name}`;
    gameDescription.textContent = `📝 ${selectedGame.description}`;
    gameInfo.textContent = `
⏱️ Duur: ${selectedGame.duration}
📊 Moeilijkheid: ${selectedGame.difficulty}
🎮 Type: ${selectedGame.type}
    `;
    
    // Save to history
    saveGameToHistory(selectedGame);
    
    // Add animation effect
    addAnimationEffect();
}

// Add a subtle animation effect when generating a new game
function addAnimationEffect() {
    const gameSection = document.getElementById('game-section');
    gameSection.style.opacity = '0';
    
    setTimeout(() => {
        gameSection.style.opacity = '1';
        gameSection.style.transition = 'opacity 0.5s ease-in';
    }, 100);
}

// Save the played game to history in local storage
function saveGameToHistory(game) {
    let history = [];
    
    // Try to load existing history
    const storedHistory = localStorage.getItem('gameHistory');
    if (storedHistory) {
        try {
            history = JSON.parse(storedHistory);
        } catch (error) {
            console.error('Error parsing stored history:', error);
            // If parsing fails, start with an empty history
            history = [];
        }
    }
    
    // Add the new game to history
    const gameEntry = {
        name: game.name,
        type: game.type,
        difficulty: game.difficulty,
        playedAt: new Date().toLocaleString('nl-NL')
    };
    
    history.push(gameEntry);
    
    // Save back to local storage
    try {
        localStorage.setItem('gameHistory', JSON.stringify(history));
    } catch (error) {
        console.error('Error saving history to local storage:', error);
    }
}

// Load history from local storage
function loadHistory() {
    try {
        const storedHistory = localStorage.getItem('gameHistory');
        if (!storedHistory) {
            return [];
        }
        
        return JSON.parse(storedHistory);
    } catch (error) {
        console.error('Error loading history from local storage:', error);
        return [];
    }
}

// Show the history modal with all played games
function showHistory() {
    // Ensure modal is initialized
    if (!historyModal) {
        try {
            initializeBootstrapComponents();
        } catch (error) {
            console.error('Error re-initializing modal:', error);
        }
    }
    
    // Clear previous history items
    historyList.innerHTML = '';
    
    // Get history from local storage
    const history = loadHistory();
    
    if (!history || history.length === 0) {
        historyList.innerHTML = '<p class="text-center py-3">Nog geen spelletjes gespeeld</p>';
    } else {
        // Add history items in reverse order (newest first)
        history.slice().reverse().forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            const gameNameSpan = document.createElement('span');
            gameNameSpan.className = 'history-game';
            gameNameSpan.textContent = `${item.name} (${item.type})`;
            
            const dateSpan = document.createElement('span');
            dateSpan.className = 'history-date';
            dateSpan.textContent = item.playedAt;
            
            historyItem.appendChild(gameNameSpan);
            historyItem.appendChild(dateSpan);
            
            historyList.appendChild(historyItem);
        });
    }
    
    // Show the modal
    try {
        if (historyModal) {
            historyModal.show();
        } else {
            // Fallback if modal object isn't available
            const modalElement = document.getElementById('history-modal');
            if (modalElement) {
                const bsModal = new bootstrap.Modal(modalElement);
                bsModal.show();
            } else {
                console.error('Cannot find history modal element');
            }
        }
    } catch (error) {
        console.error('Error showing history modal:', error);
        alert('Er is een probleem met het weergeven van de geschiedenis. Probeer de pagina te vernieuwen.');
    }
}