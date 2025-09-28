chrome.storage.session.get(["state", "role"], (result) => {
  if (result.state === "logged") {
    if (result.role === "student") window.location.href = "popup.html";
    // else window.location.href = "lecture.html";
    else window.location.href = "teacher.html";
  } else {
    if (result.state === "register") {
      window.location.href = "register.html";
    } else {
      window.location.href = "form.html";
    }
  }
});
