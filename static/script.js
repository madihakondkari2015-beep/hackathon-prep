async function sendMessage() {

    const message = document.getElementById("message").value;

    document.getElementById("tool").innerText = "Thinking...";
    document.getElementById("response").innerText = "Agent is analyzing request...";

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    document.getElementById("tool").innerText = data.tool_used;
    document.getElementById("response").innerText = data.response;
}