function upvoteProject(projectId) {
    fetch(`/project/${projectId}/upvote/`, {
        method: 'POST',  
        headers: {
            'Content-Type': 'application/json',  
            'X-CSRFToken': getCookie('csrftoken'), 
        },
    })
    .then(response => {
        console.log('Response Status:', response.status);  
        
        if (!response.ok) {
            throw new Error('Failed to upvote. HTTP Status: ' + response.status);
        }

        return response.json(); 
    })
    .then(data => {
        console.log('Server Response:', data);  

        const upvoteCountElement = document.getElementById(`upvote-count-${projectId}`);
        const upvoteIconElement = document.getElementById(`upvote-icon-${projectId}`);
        
        upvoteCountElement.textContent = data.upvotes;

        if (data.status === 'added') {
            upvoteIconElement.classList.add('filled');
            upvoteIconElement.style.color = 'green';  
        } else if (data.status === 'removed') {
            upvoteIconElement.classList.remove('filled');
            upvoteIconElement.style.color = '';  
        }

    })
    .catch(error => {
        console.error('Error upvoting:', error);
        alert('Upvote failed: ' + error.message);  
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function refreshTranscriptionStatus(jobName, file_id) {
    fetch(`/refresh-transcription/${jobName}/${file_id}`)
        .then(response => response.json())
        .then(data => {
            const transcriptionDiv = document.getElementById('transcription-text');
            if (data.status === "completed") {
                transcriptionDiv.innerHTML = `<p>${data.transcription}</p>`;
            } else if (data.status === "Transcribing...") {
                transcriptionDiv.innerHTML = `<p>Transcription in progress. Come back in a few minutes.</p>`;
            } else {
                transcriptionDiv.innerHTML = `<p>Transcription failed.</p>`;
            }
        })
        .catch(error => console.error('Error fetching transcription status:', error));
}
