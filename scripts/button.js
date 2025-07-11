function updateButton(btn) {
  btn.id = isRecording ? "stop" : "start";
  btn.textContent = isRecording ? "PARAR" : "ENTRAR";
}

function makeLinkReadonly(input, lecture) {
  if (input) {
    input.setAttribute("readonly", true);
    input.value = lecture;
  }
}

async function handleMeetingInput(button, input) {
  const lecture = await chrome.storage.session.get(["lectureLink"]);
  if (lecture.lectureLink) {
      chrome.runtime.sendMessage({
        type: "console",
        message: `const lecutre = ${lecture.lectureLink}`,
      });
    button.id = "stop";
    button.textContent = "PARAR";
    makeLinkReadonly(input, lecture.lectureLink);
  } else {
    input.removeAttribute("readonly");
    input.value = "";
    button.id = "start";
    button.textContent = "ENTRAR";
  }
}

export default { handleMeetingInput };
