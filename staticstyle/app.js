function updateStatus() {
    fetch("/api/status")
        .then(res => res.json())
        .then(data => {
            document.getElementById("bot-status").innerText = data.running ? "Rodando" : "Parado";
            document.getElementById("last-run").innerText = data.last_run || "-";
            document.getElementById("total-runs").innerText = data.total_runs;
            document.getElementById("errors").innerText = data.errors;
            document.getElementById("current-action").innerText = data.current_action;
        })
        .catch(err => console.error("Erro ao atualizar status:", err));
}

setInterval(updateStatus, 5000);
window.onload = updateStatus;
