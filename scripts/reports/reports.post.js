import api from "../api.js";
import { CONFIG } from "../config.js";
import { logger } from "../logger.js";

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("classes_container");
  const backBtn = document.getElementById("back");

  const ITEMS_PER_PAGE = 3;
  let currentPage = 1;
  let allLectures = [];
  let filteredLectures = [];

  if (backBtn) {
    backBtn.addEventListener("click", async () => {
      await chrome.storage.session.set({ currentPage: "reports_select.html" });
      window.location.href = "redirect.html";
    });
  }

  function renderLectures() {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const lecturesPage = filteredLectures.slice(start, end);

    if (lecturesPage.length === 0) {
      container.innerHTML = "<p>Nenhuma aula encontrada.</p>";
      return;
    }

    container.innerHTML = lecturesPage
      .map(
        (lecture) => `
      <div class="class_card">
        <span id="post-span-aula">Aula: ${lecture.lecture_id}</span>
        <button class="emit_btn" data-id="${lecture.lecture_id}">
          Emitir relatório
        </button>
      </div>
    `
      )
      .join("");

    document.querySelectorAll(".emit_btn").forEach((btn) =>
      btn.addEventListener("click", async (e) => {
        const lecture_id = e.target.dataset.id;

        const payload = {
          lecture_id,
          avg_cam_streaming_span: 22.0,
          avg_mic_streaming_span: 12.0,
        };

        try {
          const r = await api.callAPI(
            "POST",
            `${CONFIG.API_BASE_URL}/reports`,
            payload
          );

          console.log("Relatório criado:", r);
          logger.info("Retorno do backend:", r);

          const reportId = r?.report_id ?? r?._id ?? r?.id;

          if (!reportId) {
            alert("Relatório criado, mas ID não encontrado.");
            return;
          }

          const pdfUrl = `${CONFIG.API_BASE_URL}/reports/pdf/${reportId}`;

          const pdfRes = await fetch(pdfUrl);
          const blob = await pdfRes.blob();

          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          link.download = `relatorio_${reportId}.pdf`;
          link.click();

          URL.revokeObjectURL(link.href);

          alert("Relatório emitido e download iniciado!");
        } catch (err) {
          console.error("Erro ao emitir relatório:", err);
          alert("Erro ao emitir relatório");
        }
      })
    );
  }

  function renderPagination() {
    const totalPages = Math.ceil(filteredLectures.length / ITEMS_PER_PAGE);
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
        renderLectures();
        renderPagination();
      });
    });
  }

  try {
    allLectures = await api.callAPI("GET", `${CONFIG.API_BASE_URL}/lectures`);
    logger.info("Lectures retornadas do backend:", allLectures);

    filteredLectures = allLectures;

    renderLectures();
    renderPagination();
  } catch (error) {
    console.error("Erro ao carregar lectures:", error);
    container.innerHTML = '<p class="error">Erro ao carregar as aulas.</p>';
  }
});
