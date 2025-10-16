export async function getUser() {
    const result = await chrome.storage.session.get("user");
    return result.user || null;
}

export function getUsernameAlias(email) {
    return email ? email.split("@")[0] : "Dummy";
}