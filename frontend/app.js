document.getElementById('textForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    const textInput = document.getElementById('textInput').value;
    const maxLength = document.getElementById('maxLength').value;
    const seed = document.getElementById('seed').value;

    // Prepare the data to be sent
    const data = {
        text: textInput,
        max_length: parseInt(maxLength, 10),
        seed: parseInt(seed, 10)
    };

    fetch('http://localhost:8000/generate/', {
        method: 'POST',
        headers: {
            'accept': 'application/json', 
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        // Display the generated text
        document.getElementById('generatedText').textContent = data.generated_text;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});