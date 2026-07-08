// Timer duration in minutes
const TIMER_DURATION_MINUTES = 30;

// Total time in seconds
let totalSeconds = TIMER_DURATION_MINUTES * 60;

// Get the timer display element
const timerElement = document.getElementById("timer");

// Get the exam form
const examForm = document.getElementById("examForm");

/**
 * Format seconds into MM:SS string.
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");
}

/**
 * Update the timer display.
 */
function updateTimerDisplay() {
    timerElement.textContent = formatTime(totalSeconds);
}

/**
 * Auto-submit the exam form.
 */
function autoSubmit() {
    if (examForm) {
        examForm.submit();
    }
}

/**
 * Handle timer tick each second.
 */
function tick() {
    if (totalSeconds <= 0) {
        autoSubmit();
        return;
    }

    totalSeconds--;
    updateTimerDisplay();
}

// Initialize timer display
updateTimerDisplay();

// Start the countdown interval
setInterval(tick, 1000);

// Warn before leaving the page during an active exam
window.addEventListener("beforeunload", function (e) {
    if (totalSeconds > 0) {
        e.preventDefault();
        e.returnValue = "Your exam is in progress. Are you sure you want to leave?";
    }
});
