document.getElementById('textForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    const textInput = document.getElementById('textInput').value;
    const maxLength = document.getElementById('maxLength').value;
    const seed = document.getElementById('seed').value;

    const time_start = Date.now();

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
        const time_end = (Date.now() - time_start);
        document.getElementById('responseTime').innerHTML = returnReadableTime(time_end);
        document.getElementById('generatorTime').innerHTML = returnReadableTime(data.response_time * 1000);
        text = new String(data.generated_text)
        document.getElementById('tokensPerSecond').innerHTML = (Math.round(text.split(" ").length / data.response_time * 100) / 100) + " tokens/s";
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function returnReadableTime(time){
    let time_in_ms = time;
    let time_in_s = Math.floor(time / 1000);
    let time_in_m = Math.floor(time_in_s / 60);
    time_in_s = Math.floor(time_in_s - (60 * time_in_m));
    time_in_ms = Math.floor(time_in_ms - (time_in_s * 1000) - (time_in_m * 60000));
    return time_in_m + "m " + time_in_s + "s " + time_in_ms + "ms";
}
