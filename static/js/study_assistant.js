/**
 * UI Controls Engine Layer for DSACOE Study Assistant Workspace
 */

const outputViewport = document.getElementById("outputViewport");
const statusAlert = document.getElementById("statusAlert");
const ytUrlInput = document.getElementById("ytUrlInput");
const aiChatInput = document.getElementById("aiChatInput");

function triggerInput(id) {
    document.getElementById(id).click();
}

function displayStatus(msg, type = "success") {
    statusAlert.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show small py-2 animate-fade-in" role="alert">
            <i class="fa-solid fa-circle-info me-1"></i> ${msg}
            <button type="button" class="btn-close py-2 shadow-none" data-bs-dismiss="alert"></button>
        </div>
    `;
}
function clearOutput() {
    outputViewport.innerHTML = `
        <div class="empty-state-card text-center my-auto animate-fade-in">
            <i class="fa-solid fa-brain-circuit display-1 text-info opacity-50 mb-3 d-block"></i>
            <h5 class="text-white">Workspace Cleared</h5>
            <p class="text-light-muted mx-auto max-w-400">
                Load new media pipelines or ask questions via input tool.
            </p>
        </div>
    `;
}

function renderLoading(prompt) {
    outputViewport.innerHTML = `
        <div class="text-center my-auto p-4 animate-fade-in">
            <div class="spinner-border text-info mb-3" style="width: 3rem; height: 3rem;" role="status"></div>
            <h6 class="text-white fw-medium">${prompt}</h6>
            <p class="text-light-muted small">AI is parsing and structures data elements...</p>
        </div>
    `;
}

function handleFileSelect(input, type) {
    if (!input.files || input.files.length === 0) return;
    const file = input.files[0];
    
    const formData = new FormData();
    formData.append("file", file);

    displayStatus(`Processing file upload: ${file.name}...`, "info");
    
    fetch("/upload-notes", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
    console.log(data);
    if(data.success){
        displayStatus(data.message, "success");
    }
    else{
        displayStatus(data.message,"danger");
    }

})
    .catch(() => displayStatus("Error connection status during document data ingest.", "danger"));
}

function processYoutubeLink() {
    const url = ytUrlInput.value.trim();
    if(!url) {
        displayStatus("Please enter a valid video link string first.", "warning");
        return;
    }

    displayStatus("Analyzing media URL structures...", "info");

    fetch("/upload-notes", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `youtube_url=${encodeURIComponent(url)}`
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            displayStatus("Successfully added reference link context rules.", "success");
            ytUrlInput.value = "";
        } else {
            displayStatus(data.message, "danger");
        }
    });
}

function generateSummary() {
    renderLoading("Compiling structural reference notes...");
    
    fetch("/generate-summary", { method: "POST" })
    .then(res => res.json())
    .then(data => {
        outputViewport.innerHTML = `
            <div class="output-card-response animate-fade-in">
                ${formatTextResponse(data.summary)}
            </div>
        `;
    });
}

function generateFlashcards() {

    renderLoading("Generating Flashcards...");

    fetch("/generate-flashcards", {

        method: "POST"

    })

    .then(res => res.json())

    .then(data => {

        try {

            let json = data.raw_json
                .replace(/```json/g,"")
                .replace(/```/g,"")
                .trim();

            const cards = JSON.parse(json);

            let html = '<div class="flashcard-deck">';

            cards.forEach(card=>{

                html+=`

                <div class="study-flashcard"
                onclick="flipCard(this,
                '${btoa(card.front)}',
                '${btoa(card.back)}')">

                ${card.front}

                </div>

                `;

            });

            html+="</div>";

            outputViewport.innerHTML=html;

        }

        catch(err){

            outputViewport.innerHTML=

            formatTextResponse(data.raw_json);

        }

    });

}

function flipCard(element, frontBase64, backBase64) {
    const frontText = atob(frontBase64);
    const backText = atob(backBase64);
    
    if (element.classList.contains("flipped")) {
        element.innerHTML = `<span>${frontText}</span>`;
        element.classList.remove("flipped");
        element.style.borderLeftColor = "#00d2ff";
    } else {
        element.innerHTML = `<span class="text-muted small">💡 Answer:</span><br><strong>${backText}</strong>`;
        element.classList.add("flipped");
        element.style.borderLeftColor = "#2ec4b6";
    }
}

function generateQuiz(){

    renderLoading("Generating Quiz...");

    fetch("/generate-quiz",{

        method:"POST"

    })

    .then(res=>res.json())

    .then(data=>{

        try{

            let json=data.raw_json
            .replace(/```json/g,"")
            .replace(/```/g,"")
            .trim();

            const quiz=JSON.parse(json);

            let html="<div class='output-card-response'>";

            html+="<h3>📝 AI Quiz</h3><br>";

            quiz.forEach((q,index)=>{

                html+=`

                <div class="quiz-question-block">

                <h5>${index+1}. ${q.question}</h5>

                `;

                q.options.forEach(opt=>{

                    html+=`

                    <button

                    class="quiz-option-btn"

                    onclick="checkQuizAnswer(this,

                    '${opt.replace(/'/g,"\\'")}',

                    '${q.answer.replace(/'/g,"\\'")}')">

                    ${opt}

                    </button>

                    `;

                });

                html+="</div>";

            });

            html+="</div>";

            outputViewport.innerHTML=html;

        }

        catch{

            outputViewport.innerHTML=

            formatTextResponse(data.raw_json);

        }

    });

}

function checkQuizAnswer(btn, selection, correct) {
    const container = btn.parentElement;
    const allButtons = container.querySelectorAll('.quiz-option-btn');
    
    allButtons.forEach(b => b.disabled = true);
    
    if (selection === correct) {
        btn.style.background = "#d4edda";
        btn.style.borderColor = "#28a745";
        btn.innerHTML += "  <i class='fa-solid fa-circle-check text-success ms-2'></i>";
    } else {
        btn.style.background = "#f8d7da";
        btn.style.borderColor = "#dc3545";
        btn.innerHTML += "  <i class='fa-solid fa-circle-xmark text-danger ms-2'></i>";
    }
}

function submitWorkspaceChat() {
    const text = aiChatInput.value.trim();
    if(!text) return;

    // Directly evaluate local parsing response patterns inside view window
    const userBlock = document.createElement("div");
    userBlock.className = "p-3 mb-2 bg-dark-trans border border-secondary border-opacity-25 rounded text-white small ms-auto text-end my-2 max-w-400 animate-fade-in";
    userBlock.innerText = text;
    outputViewport.appendChild(userBlock);
    
    aiChatInput.value = "";
    outputViewport.scrollTop = outputViewport.scrollHeight;

    setTimeout(() => {
        const botBlock = document.createElement("div");
        botBlock.className = "output-card-response my-2 me-auto max-w-400 animate-fade-in";
        botBlock.innerHTML = `🤖 <b>Study Copilot:</b> I am indexing your question about <i>"${text}"</i>. Please run explicit generation actions above to build detailed components on this topic.`;
        outputViewport.appendChild(botBlock);
        outputViewport.scrollTop = outputViewport.scrollHeight;
    }, 600);
}
function formatTextResponse(text) {
    if (!text) return "";

    return text
        .replace(/\*\*(.*?)\*\*/g, "<h5>$1</h5>")
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>")
        .replace(/^- (.*)$/gm, "• $1");
}