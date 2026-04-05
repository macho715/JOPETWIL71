export type ProxyMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

export async function callMyAgentWithFetch(params: {
  baseUrl: string;
  model?: string;
  sensitivity?: "public" | "internal" | "confidential" | "secret";
  proxyToken?: string;
  messages: ProxyMessage[];
}) {
  const requestId = crypto.randomUUID();
  const headers: Record<string, string> = {
    "content-type": "application/json",
    "x-request-id": requestId,
    "x-ai-sensitivity": params.sensitivity ?? "internal",
  };
  if (params.proxyToken) {
    headers["x-ai-proxy-token"] = params.proxyToken;
  }

  const response = await fetch(`${params.baseUrl.replace(/\/+$/, "")}/api/ai/chat`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      model: params.model ?? "github-copilot/gpt-5-mini",
      sensitivity: params.sensitivity ?? "internal",
      messages: params.messages,
    }),
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail =
      typeof payload?.detail === "string" ? payload.detail : `HTTP ${response.status}`;
    throw new Error(`AI proxy error: ${detail}`);
  }
  return payload;
}
