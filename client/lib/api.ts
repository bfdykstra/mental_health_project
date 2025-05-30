const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface ApiError extends Error {
  status?: number;
  body?: any;
}

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
    const error: ApiError = new Error(
      `API error: ${response.status} ${response.statusText} at ${endpoint}`
    );
    error.status = response.status;
    error.body = errorBody;
    throw error;
  }

  return response.json();
}

/**
 * Stream data from the API using Server-Sent Events
 *
 * @param endpoint - The API endpoint to stream from
 * @param requestData - The data to send in the POST request
 * @param onEvent - Callback for each event received
 * @param onError - Callback for errors
 * @param onComplete - Callback when stream completes
 */
export function streamApi(
  endpoint: string,
  requestData: any,
  onEvent: (eventData: any) => void,
  onError: (error: Error) => void,
  onComplete: () => void
): () => void {
  // Create a URL with query params for GET requests or use POST
  const url = `${API_URL}${endpoint}`;

  // For streaming, we need to send the request data first
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      function readStream(): Promise<void> {
        return reader!.read().then(({ done, value }) => {
          if (done) {
            onComplete();
            return;
          }

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.slice(6));
                onEvent(data);
              } catch (e) {
                console.warn("Failed to parse SSE data:", line);
              }
            }
          }

          return readStream();
        });
      }

      return readStream();
    })
    .catch(onError);

  // Return cleanup function
  return () => {
    // For fetch streams, we can't easily cancel, but we can ignore events
    // In a production app, you might want to use AbortController
  };
}
