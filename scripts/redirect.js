chrome.storage.session.get(["state", "role", "currentPage"], (result) => {
  const { state, role, currentPage } = result;

  if (state === "logged") {
    if (role === "student") {
      window.location.href = "popup.html";
    } else if (role === "educator") {
      if (currentPage) {
        window.location.href = currentPage;
      } else {
        window.location.href = "teacher.html";
      }
    }
  } else if (state === "register") {
    window.location.href = "register.html";
  } else {
    window.location.href = "form.html";
  }
});
