export function handleView(content) {
  const copyCard = document.getElementById("lecture_title");
  const lectureCard = document.getElementById("form_lecture");
  const copyBtn = document.getElementById("copy");
  const homeBtn = document.getElementById("back")
  if (copyCard.style.display === "none") {
    lectureCard.style.display = "none";
    copyCard.style.display = "block";
    homeBtn.textContent = "MENU";
    chrome.storage.session.set({ lectureView: "copy" });
  } else if (lectureCard.style.display === "none") {
    lectureCard.style.display = "block";
    copyCard.style.display = "none";
    homeBtn.textContent = "VOLTAR"
    chrome.storage.session.remove("lectureView");
  }
}

export function triggerViewHandling(button) {
  button.addEventListener("click", () => {
    handleView();
  });
}

export function restoreView() {
  const copyCard = document.getElementById("lecture_title");
  const lectureCard = document.getElementById("form_lecture");
  const copyBtn = document.getElementById("copy");
  chrome.storage.session.get(["lectureView"], (result) => {
    if (result.lectureView === "copy") {
      chrome.runtime.sendMessage({
        type: "console",
        message: `lectureView: ${result.lectureView}`,
      });
      lectureCard.style.display = "none";
      copyCard.style.display = "block";
    } else {
      chrome.runtime.sendMessage({
        type: "console",
        message: `lectureView: none`,
      });
      copyCard.style.display = "none";
      lectureCard.style.display = "block";
    }
  });
}
