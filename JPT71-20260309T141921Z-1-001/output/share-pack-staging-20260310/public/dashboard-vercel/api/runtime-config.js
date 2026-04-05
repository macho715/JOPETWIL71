module.exports = (_req, res) => {
  const endpoint = String(process.env.JPT71_AI_ENDPOINT || "").trim();
  const proxyToken = String(process.env.JPT71_AI_PROXY_TOKEN || "").trim();

  res.setHeader("Content-Type", "application/javascript; charset=utf-8");
  res.setHeader("Cache-Control", "no-store, max-age=0, must-revalidate");
  res.status(200).send(
    [
      "(function () {",
      `  window.__JPT71_AI_ENDPOINT__ = ${JSON.stringify(endpoint)};`,
      `  window.__JPT71_AI_PROXY_TOKEN__ = ${JSON.stringify(proxyToken)};`,
      "})();",
      ""
    ].join("\n")
  );
};
