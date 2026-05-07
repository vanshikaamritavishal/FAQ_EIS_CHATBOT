async function askQuestion() {

    const question = document.getElementById("question").value;

    const answerDiv = document.getElementById("answer");

    answerDiv.innerHTML = "Thinking...";

    try {

        const response = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        answerDiv.innerHTML = data.answer;

    } catch (error) {

        console.error(error);

        answerDiv.innerHTML = "Error connecting to backend.";

    }
}