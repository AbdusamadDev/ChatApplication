// Check if MediaRecorder is available
if (!window.MediaRecorder) {
    alert('MediaRecorder not supported on this browser. Please use Firefox or Chrome.');
}

// Request permissions to record audio
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        mediaRecorder.start();

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener('stop', () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
        });

        // Stop recording after 3 seconds
        setTimeout(() => {
            mediaRecorder.stop();
        }, 3000);
    })
    .catch(error => console.error('MediaDevices.getUserMedia error:', error));
