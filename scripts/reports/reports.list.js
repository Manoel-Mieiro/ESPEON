import api from "../api.js";
import { getUser } from "../auth/user.js";
import { CONFIG } from "../config.js";
import { logout } from "../auth/logout.js";

document.addEventListener("DOMContentLoaded", async () => {
  await initReports();
  const exit = document.getElementById("exit");
  const back = document.getElementById("back");
  if (back) {
    back.addEventListener("click", async () => {
      await chrome.storage.session.remove("currentPage");
      window.location.href = "redirect.html";
    });
  }
  logout(exit);
});

const reportsContainer = document.querySelector(".form-container");
const ITEMS_PER_PAGE = 1;
let currentPage = 1;
let filteredReports = [];

async function initReports() {
  const teacherEmail = await getUser();
  console.log(`[REPORT] user retrieved: ${teacherEmail}`);
  await loadReports();
}

async function getReports() {
  const data = await api.callAPI("GET", `${CONFIG.API_BASE_URL}/reports`);
  return data || [];
}

export async function loadReports() {
  try {
    const reports = await getReports();
    filteredReports = reports;
    renderReports();
    renderPagination();
  } catch (err) {
    reportsContainer.innerHTML = `<p class="error">${err.message}</p>`;
    chrome.runtime.sendMessage({
      type: "console",
      message: `[loadReports] Erro: ${err.message}`,
    });
  }
}

function renderReports() {
  const start = (currentPage - 1) * ITEMS_PER_PAGE;
  const end = start + ITEMS_PER_PAGE;
  const reportsPage = filteredReports.slice(start, end);

  if (reportsPage.length === 0) {
    reportsContainer.innerHTML = "<p>Nenhum relatório encontrado.</p>";
    return;
  }

  reportsContainer.innerHTML = reportsPage
    .map(
      (r) => `
    <div class="report-card">
        <div class="report-card-title">
            <h3>Aula #${r.lecture_id}</h3>
            <a href="${CONFIG.API_BASE_URL}/reports/pdf/${
        r._id
      }" target="_blank">Baixar PDF</a>
        </div>
        <div class="report-card-content-container">
            <div class="report-card-content">
                <p>Disciplina: ${r.subject_id}</p>
                <p>Total de alunos: ${r.total_students}</p>
                <p>Tempo total assistido: ${Math.round(
                  r.total_time_watched
                )} min</p>
                <p>Data: ${r.issued_at} min</p>
            </div>
        </div>
    </div>
`
    )
    .join("");
}

function renderPagination() {
  const totalPages = Math.ceil(filteredReports.length / ITEMS_PER_PAGE);
  let paginationHtml = "";

  let startPage = Math.max(currentPage - 1, 1);
  let endPage = Math.min(startPage + 2, totalPages);

  if (endPage - startPage < 2) {
    startPage = Math.max(endPage - 2, 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    paginationHtml += `<button class="page-btn ${
      i === currentPage ? "active" : ""
    }" data-page="${i}">${i}</button>`;
  }

  const footer = document.getElementById("footer_reports");

  let pagContainer = document.getElementById("pagination");
  if (!pagContainer) {
    pagContainer = document.createElement("div");
    pagContainer.id = "pagination";
    pagContainer.classList.add("pagination-container");
    footer.prepend(pagContainer);
  }

  pagContainer.innerHTML = paginationHtml;

  document.querySelectorAll(".page-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      currentPage = parseInt(e.target.dataset.page);
      renderReports();
      renderPagination();
    });
  });
}
