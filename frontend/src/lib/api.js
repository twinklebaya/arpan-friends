const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options.body && !(options.body instanceof FormData)
        ? { "Content-Type": "application/json" }
        : {}),
      ...options.headers,
    },
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail || JSON.stringify(data);
    } catch {
      // ignore
    }
    throw new Error(`${res.status}: ${detail}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  getPersons: (status) => request(`/api/persons${status ? `?status=${status}` : ""}`),
  getPrimaryTargets: () => request("/api/persons/primary-targets"),
  getStats: () => request("/api/stats"),
  getGeneralFeed: () => request("/api/feed/general"),
  getTargetFeed: () => request("/api/feed/target"),
  submitTip: (formData) => request("/api/tips", { method: "POST", body: formData }),
  submitPerson: (payload) =>
    request("/api/persons/submit", { method: "POST", body: JSON.stringify(payload) }),

  // Admin (requires a bearer token from the caller)
  adminRequest: (path, token, options = {}) =>
    request(path, {
      ...options,
      headers: { ...options.headers, Authorization: `Bearer ${token}` },
    }),
};

export { BASE_URL };
