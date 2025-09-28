import { formatLectureString } from "./json_handling.js";

function generateTitle(lecture) {
  var title = lecture;
  return JSON.stringify(title);
}

export async function fillWithTitle(lecture, field) {
  field.textContent = await formatLectureString(lecture);
}
