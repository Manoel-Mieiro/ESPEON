import { CONFIG } from "../config.js";
const lecturesEndpoint = "http://localhost:8183/lectures2";

export function fillTeacher() {
  chrome.storage.session.get("user", (result) => {
    const teacher = result.user;
    chrome.runtime.sendMessage({
      type: "console",
      message: `PROFESSOR resgatado: ${teacher}`,
    });

    document.getElementById("teacher").value = teacher;
  });
}

async function fetchSubjects() {
  try {
    const response = await fetch(`http://localhost:8183/${CONFIG.SUBJECTS_ENDPOINT}`);
    if (!response.ok) throw new Error("API may be unavaliable");
    return response;
  } catch (error) {
    chrome.runtime.sendMessage({
      type: "console",
      message: `[fetchSubjects] Falha ao extrair: ${error}`,
    });
  }
}

export async function fillSubjects(selector) {
  const response = await fetchSubjects();
  if (!response) return;

  const subjectList = await response.json();

  for (let s = 0; s < subjectList.length; s++) {
    const subject = subjectList[s]; 
    const opt = document.createElement("option");
    opt.value = subject.subject_id; 
    opt.innerHTML = formatSubjectName(subject.name); 
    selector.appendChild(opt);
  }
}

function formatSubjectName(name) {
  if (!name) return "";
  return name.replace(/_/g, " ").toUpperCase();
}


export function getFormData() {
  const subjectSelect = document.getElementById("subject");
  const teacherSelect = document.getElementById("teacher");

  const formData = {
    subject_id: subjectSelect.value,      // UUID do subject
    teacher_id: teacherSelect.value,      // UUID do teacher
    date_lecture: document.getElementById("date_lecture").value,
    period_start: document.getElementById("period_start").value,
    period_end: document.getElementById("period_end").value,
  };

  chrome.runtime.sendMessage({
    type: "console",
    message: `Form data collected: ${JSON.stringify(formData)}`,
  });

  return formData;
}

