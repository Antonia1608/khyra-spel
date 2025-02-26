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
const historyModalElement = document.getElementById('history-modal');
let historyModal;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log("App initializing...");
    
    // Try to initialize Bootstrap components
    try {
        // First check if bootstrap is available
        if (typeof bootstrap !== 'undefined') {
            console.log("Bootstrap found, initializing modal");
            historyModal = new bootstrap.Modal(historyModalElement);
        } else {
            console.warn("Bootstrap not found, will use manual modal handling");
        }
    } catch (error) {
        console.error("Error initializing bootstrap components:", error);
    }
    
    // Load history from local storage if available
    loadHistory();
    
    // Generate a random game on initial load
    generateGame();
    
    // Event listeners
    generateButton.addEventListener('click', generateGame);
    historyButton.addEventListener('click', showHistory);
    
    // Add close functionality for the modal's close button
    const closeButtons = document.querySelectorAll('[data-bs-dismiss="modal"]');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            closeHistoryModal();
        });
    });
    
    // Add click outside functionality
    window.addEventListener('click', (event) => {
        if (event.target === historyModalElement) {
            closeHistoryModal();
        }
    });
    
    console.log("App initialization complete");
});

// Manual function to show modal
function showHistoryModal() {
    console.log("Showing history modal");
    try {
        if (historyModal) {
            // If bootstrap is available, use it
            historyModal.show();
        } else {
            // Manual fallback
            historyModalElement.classList.add('show');
            historyModalElement.style.display = 'block';
            document.body.classList.add('modal-open');
            
            // Add backdrop if it doesn't exist
            let backdrop = document.querySelector('.modal-backdrop');
            if (!backdrop) {
                backdrop = document.createElement('div');
                backdrop.className = 'modal-backdrop fade show';
                document.body.appendChild(backdrop);
            }
        }
    } catch (error) {
        console.error("Error showing modal:", error);
        alert("Er is een probleem met het tonen van de geschiedenis. Probeer de pagina te vernieuwen.");
    }
}

// Manual function to close modal
function closeHistoryModal() {
    console.log("Closing history modal");
    try {
        if (historyModal) {
            // If bootstrap is available, use it
            historyModal.hide();
        } else {
            // Manual fallback
            historyModalElement.classList.remove('show');
            historyModalElement.style.display = 'none';
            document.body.classList.remove('modal-open');
            
            // Remove backdrop
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
        }
    } catch (error) {
        console.error("Error closing modal:", error);
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
    console.log("Show history button clicked");
    
    // Clear previous history items
    historyList.innerHTML = '';
    
    // Get history from local storage
    const history = loadHistory();
    console.log("Loaded history:", history);
    
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
    showHistoryModal();
}