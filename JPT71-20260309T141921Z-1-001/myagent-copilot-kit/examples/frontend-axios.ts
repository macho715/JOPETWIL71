import axios from "axios";

export async function callMyAgentWithAxios(params: {
  baseUrl: string;
  message: string;
  proxyToken?: string;
}) {
  const requestId = crypto.randomUUID();
  const headers: Record<string, string> = {
    "x-request-id": requestId,
    "x-ai-sensitivity": "internal",
  };
  if (params.proxyToken) {
    headers["x-ai-proxy-token"] = params.proxyToken;
  }

  const client = axios.create({
    baseURL: params.baseUrl.replace(/\/+$/, ""),
    timeout: 20_000,
  });

  const { data } = await client.post(
    "/api/ai/chat",
    {
      model: "github-copilot/gpt-5-mini",
      sensitivity: "internal",
      messages: [{ role: "user", content: params.message }],
    },
    { headers },
  );

  return data;
}
