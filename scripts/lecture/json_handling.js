import api from "../api.js";
import { CONFIG } from "../config.js";

export async function formatLectureString(data) {
  const subjectDetails = await api.callAPI(
    "GET",
    `${CONFIG.API_BASE_URL}${CONFIG.SUBJECTS_ENDPOINT}/${data.subject_id}`
  );

  const teacherDetails = await api.callAPI(
    "GET",
    `${CONFIG.API_BASE_URL}${CONFIG.USERS_ENDPOINT}/${data.teacher_id}`
  );

  const subjectId = data.subject_id;
  const subject = subjectDetails.name;
  const teacher = teacherDetails.email;

  console.log(`SUBJECT: ${subject}`);
  console.log(`Teacher: ${teacher}`);

  return `[${subjectId}] ${subject}: ${teacher}`;
}
