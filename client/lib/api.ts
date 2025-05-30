const API_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * Fetches data from the API.
 *
 * @param {RequestInit} [options={}] - The options for the fetch request.
 * @returns {Promise<any>} - A promise that resolves to the JSON response from the API.
 * @throws {Error} - Throws an error if the response is not ok.
 */
export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  // TODO: add /api/v1 to endpoints in server
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  if (!response.ok) {
    let errorBody = {};
    try {
      errorBody = await response.json();
    } catch (e: any) {
      // ignore parse error
    }
    const error = new Error(
      `API error: ${response.status} ${response.statusText} at ${endpoint}`
    );
    error.status = response.status;

    error.body = errorBody;
    throw error;
  }

  return response.json();
}
