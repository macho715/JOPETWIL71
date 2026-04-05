function safeErrorDetail(value) {
    return value.length <= 320 ? value : `${value.slice(0, 317)}...`;
}
export function buildOperationalLog(params) {
    const now = Date.now();
    return {
        schema: "openclaw.copilot.proxy.log.v1",
        timestamp: new Date(now).toISOString(),
        requestId: params.requestId,
        stage: params.stage,
        outcome: params.outcome,
        route: params.route,
        httpStatus: params.httpStatus,
        latencyMs: Math.max(0, now - params.startedAtMs),
        model: params.model,
        sensitivity: params.sensitivity,
        reason: params.reason,
        provider: params.provider,
        endpoint: params.endpoint,
        dlpStatus: params.dlpStatus ?? "unknown",
        dlpHighestSeverity: params.dlpHighestSeverity ?? "unknown",
        dlpFindingCount: params.dlpFindingCount ?? 0,
        sanitized: params.sanitized ?? false,
        usage: params.usage,
        errorCode: params.errorCode,
        errorDetail: params.errorDetail ? safeErrorDetail(params.errorDetail) : undefined,
    };
}
export function toOperationalUsage(response) {
    return response.usage;
}
//# sourceMappingURL=ops-log.js.map