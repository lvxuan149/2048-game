const gameBoard = document.getElementById('game-board');
const scoreDisplay = document.getElementById('score');
let board = [];
let score = 0;

function initGame() {
    board = Array(4).fill().map(() => Array(4).fill(0));
    score = 0;
    addNewTile();
    addNewTile();
    updateBoard();
}

function addNewTile() {
    const emptyTiles = [];
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (board[i][j] === 0) {
                emptyTiles.push({i, j});
            }
        }
    }
    if (emptyTiles.length > 0) {
        const {i, j} = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
        board[i][j] = Math.random() < 0.9 ? 2 : 4;
    }
}

function updateBoard() {
    gameBoard.innerHTML = '';
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            const tile = document.createElement('div');
            tile.className = `tile ${board[i][j] ? 'tile-' + board[i][j] : ''}`;
            tile.textContent = board[i][j] || '';
            gameBoard.appendChild(tile);
        }
    }
    scoreDisplay.textContent = score;
}

function move(direction) {
    let moved = false;
    const newBoard = JSON.parse(JSON.stringify(board));

    function merge(row) {
        const newRow = row.filter(val => val !== 0);
        for (let i = 0; i < newRow.length - 1; i++) {
            if (newRow[i] === newRow[i + 1]) {
                newRow[i] *= 2;
                score += newRow[i];
                newRow.splice(i + 1, 1);
            }
        }
        while (newRow.length < 4) {
            newRow.push(0);
        }
        return newRow;
    }

    if (direction === 'ArrowUp' || direction === 'ArrowDown') {
        for (let j = 0; j < 4; j++) {
            let column = [board[0][j], board[1][j], board[2][j], board[3][j]];
            if (direction === 'ArrowDown') column.reverse();
            column = merge(column);
            if (direction === 'ArrowDown') column.reverse();
            for (let i = 0; i < 4; i++) {
                if (newBoard[i][j] !== column[i]) {
                    moved = true;
                    newBoard[i][j] = column[i];
                }
            }
        }
    } else {
        for (let i = 0; i < 4; i++) {
            let row = board[i].slice();
            if (direction === 'ArrowRight') row.reverse();
            row = merge(row);
            if (direction === 'ArrowRight') row.reverse();
            if (!row.every((val, index) => val === newBoard[i][index])) {
                moved = true;
                newBoard[i] = row;
            }
        }
    }

    if (moved) {
        board = newBoard;
        addNewTile();
        updateBoard();
    }

    if (isGameOver()) {
        alert('Game Over! Your score: ' + score);
    }
}

function isGameOver() {
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (board[i][j] === 0) return false;
            if (i < 3 && board[i][j] === board[i + 1][j]) return false;
            if (j < 3 && board[i][j] === board[i][j + 1]) return false;
        }
    }
    return true;
}

let isDragging = false;
let startX, startY;
let minSwipeDistance = 50; // 最小滑动距离

function startDrag(e) {
    isDragging = true;
    startX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
    startY = e.type.includes('mouse') ? e.clientY : e.touches[0].clientY;
}

function drag(e) {
    if (!isDragging) return;
    
    let endX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
    let endY = e.type.includes('mouse') ? e.clientY : e.touches[0].clientY;
    
    let dx = endX - startX;
    let dy = endY - startY;
    
    if (Math.abs(dx) > minSwipeDistance || Math.abs(dy) > minSwipeDistance) {
        if (Math.abs(dx) > Math.abs(dy)) {
            move(dx > 0 ? 'ArrowRight' : 'ArrowLeft');
        } else {
            move(dy > 0 ? 'ArrowDown' : 'ArrowUp');
        }
        isDragging = false; // 移动后结束拖拽
    }
}

function endDrag() {
    isDragging = false;
}

// 移除之前的键盘事件监听器
document.removeEventListener('keydown', keydownHandler);

// 添加新的键盘事件监听器
function keydownHandler(event) {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        event.preventDefault();
        move(event.key);
    }
}
document.addEventListener('keydown', keydownHandler);

// 添加鼠标事件监听器
gameBoard.addEventListener('mousedown', startDrag);
gameBoard.addEventListener('mousemove', drag);
gameBoard.addEventListener('mouseup', endDrag);
gameBoard.addEventListener('mouseleave', endDrag);

// 添加触摸事件支持
gameBoard.addEventListener('touchstart', startDrag);
gameBoard.addEventListener('touchmove', (e) => {
    e.preventDefault(); // 防止页面滚动
    drag(e);
});
gameBoard.addEventListener('touchend', endDrag);

initGame();