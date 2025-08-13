// static/script.js
document.querySelector("#replayButton").addEventListener("click", function() {
    fetch("/replay", {
        method: "POST",
    })
    // Update board
    const cells = document.querySelectorAll("#board td");
    for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
            cells[r * 3 + c].textContent = "";
        }
    }

});

document.querySelectorAll("#board td").forEach(cell => {
    cell.addEventListener("click", () => {
        const row = cell.dataset.row;
        const col = cell.dataset.col;

        fetch("/play", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ row: parseInt(row), col: parseInt(col) })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            // Update board
            const cells = document.querySelectorAll("#board td");
            for (let r = 0; r < 3; r++) {
                for (let c = 0; c < 3; c++) {
                    cells[r * 3 + c].textContent = data.grid[r][c];
                }
            }
            // Show winner if game over
            if (data.winner !== null) {
                setTimeout(() => alert(
                    data.winner === 1 ? "AI wins!" :
                    data.winner === -1 ? "You win!" :
                    "Draw!"
                ), 100);
            }
        });
    });
});
