const status = document.getElementById("status");

function startRecognition() {
  if (!("webkitSpeechRecognition" in window)) {
    status.innerText = "❌ Not supported";
    return;
  }

  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onstart = () => (status.innerText = "🎙️ Listening...");
  recognition.onerror = () => (status.innerText = "❌ Error");
  recognition.onend = () => (status.innerText = "✅ Done");

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    window.parent.postMessage(
      {
        isStreamlitMessage: true,
        type: "streamlit:setComponentValue",
        value: transcript,
      },
      "*"
    );
    status.innerText = "✅ Sent: " + transcript;
  };

  recognition.start();
}

window.addEventListener("load", function () {
  const Streamlit = window.streamlitComponent;
  if (Streamlit) Streamlit.setComponentReady();
});
