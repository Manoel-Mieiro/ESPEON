import api from "../api.js";
import { CONFIG } from "../config.js";
import { apiLogger, logger } from "../logger.js";

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("classes_container");

  const backBtn = document.getElementById("back");

  if (backBtn) {
    backBtn.addEventListener("click", async () => {
      await chrome.storage.session.set({ currentPage: "reports_select.html" });
      window.location.href = "redirect.html";
    });
  }

  const lectures = await api.callAPI("GET", `${CONFIG.API_BASE_URL}/lectures`);

  logger.info("Lectures retornadas do backend:", lectures);

  lectures.forEach((lecture) => {
    const div = document.createElement("div");
    div.classList.add("class_card");

    div.innerHTML = `
      <span>Aula: ${lecture.date_lecture}</span>
      <span>Horário: ${lecture.period_start} - ${lecture.period_end}</span>

      <button class="emit_btn" data-id="${lecture.lecture_id}">
        Emitir relatório
      </button>
    `;

    container.appendChild(div);
  });

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
        apiLogger.info("🔍 Retorno do backend:", r);

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
});
