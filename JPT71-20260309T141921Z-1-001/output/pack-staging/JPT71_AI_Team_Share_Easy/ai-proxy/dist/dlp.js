const DEFAULT_REDACT = "[REDACTED]";
const SEVERITY_ORDER = {
    none: 0,
    low: 1,
    medium: 2,
    high: 3,
    critical: 4,
};
const DEFAULT_POLICY = {
    sanitizeAtOrAbove: "medium",
    blockAtOrAbove: "high",
    includeEntropyRule: true,
};
const DEFAULT_RULES = [
    {
        id: "openai_sk",
        severity: "critical",
        pattern: /\bsk-[A-Za-z0-9_-]{12,}\b/g,
        description: "OpenAI style API key detected.",
    },
    {
        id: "github_pat",
        severity: "critical",
        pattern: /\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b/g,
        description: "GitHub personal access token detected.",
    },
    {
        id: "bearer_token",
        severity: "high",
        pattern: /\bBearer\s+[A-Za-z0-9._\-+=]{18,}\b/gi,
        description: "Bearer token detected.",
    },
    {
        id: "private_key",
        severity: "critical",
        pattern: /-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----/g,
        description: "Private key block detected.",
        redactWith: "[REDACTED_PRIVATE_KEY]",
    },
    {
        id: "password_assignment",
        severity: "high",
        pattern: /\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*["']?[^,\s"']{6,}/gi,
        description: "Credential assignment detected.",
    },
    {
        id: "email",
        severity: "medium",
        pattern: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi,
        description: "Email address detected.",
    },
    {
        id: "phone_number",
        severity: "medium",
        pattern: /\b(?:\+?\d[\d\-() ]{8,}\d)\b/g,
        description: "Phone number detected.",
    },
];
function shouldApplyThreshold(severity, threshold) {
    return SEVERITY_ORDER[severity] >= SEVERITY_ORDER[threshold];
}
function maxSeverity(left, right) {
    return SEVERITY_ORDER[left] >= SEVERITY_ORDER[right] ? left : right;
}
function maskPreview(value) {
    const trimmed = value.trim();
    if (trimmed.length <= 8) {
        return "***";
    }
    return `${trimmed.slice(0, 4)}...${trimmed.slice(-3)}`;
}
function escapeRegexLiteral(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
function shannonEntropy(value) {
    const frequencies = new Map();
    for (const char of value) {
        frequencies.set(char, (frequencies.get(char) ?? 0) + 1);
    }
    let entropy = 0;
    for (const count of frequencies.values()) {
        const probability = count / value.length;
        entropy -= probability * Math.log2(probability);
    }
    return entropy;
}
function detectHighEntropy(content) {
    const candidates = content.match(/[A-Za-z0-9+/_=-]{24,}/g) ?? [];
    const findings = [];
    for (const token of candidates) {
        const diversity = Number(/[A-Z]/.test(token)) +
            Number(/[a-z]/.test(token)) +
            Number(/\d/.test(token)) +
            Number(/[+/_=-]/.test(token));
        if (diversity < 3 || shannonEntropy(token) < 3.5) {
            continue;
        }
        findings.push({
            ruleId: "entropy_token",
            severity: "high",
            description: "High-entropy token-like string detected.",
            matchedTextPreview: maskPreview(token),
        });
    }
    return findings;
}
function scanByRules(content, rules) {
    const findings = [];
    for (const rule of rules) {
        const pattern = new RegExp(rule.pattern.source, rule.pattern.flags);
        const matches = content.match(pattern) ?? [];
        for (const match of matches) {
            findings.push({
                ruleId: rule.id,
                severity: rule.severity,
                description: rule.description,
                matchedTextPreview: maskPreview(match),
            });
        }
    }
    return findings;
}
function sanitizeContent(content, rules, policy) {
    let next = content;
    for (const rule of rules) {
        if (!shouldApplyThreshold(rule.severity, policy.sanitizeAtOrAbove)) {
            continue;
        }
        next = next.replace(rule.pattern, rule.redactWith ?? DEFAULT_REDACT);
    }
    if (!policy.includeEntropyRule) {
        return next;
    }
    const candidates = content.match(/[A-Za-z0-9+/_=-]{24,}/g) ?? [];
    for (const token of candidates) {
        if (shannonEntropy(token) < 3.5) {
            continue;
        }
        next = next.replace(new RegExp(escapeRegexLiteral(token), "g"), DEFAULT_REDACT);
    }
    return next;
}
export function scanMessagesForDlp(messages, opts) {
    const rules = opts?.rules?.length ? opts.rules : DEFAULT_RULES;
    const policy = {
        ...DEFAULT_POLICY,
        ...(opts?.policy ?? {}),
    };
    const findings = [];
    const messageScans = [];
    let highestSeverity = "none";
    for (const [index, message] of messages.entries()) {
        const content = String(message.content ?? "");
        const combinedFindings = [
            ...scanByRules(content, rules),
            ...(policy.includeEntropyRule ? detectHighEntropy(content) : []),
        ];
        for (const finding of combinedFindings) {
            findings.push(finding);
            highestSeverity = maxSeverity(highestSeverity, finding.severity);
        }
        messageScans.push({
            index,
            findings: combinedFindings,
            originalContent: content,
            sanitizedContent: sanitizeContent(content, rules, policy),
        });
    }
    let status = "allow";
    if (findings.some((finding) => shouldApplyThreshold(finding.severity, policy.blockAtOrAbove))) {
        status = "block";
    }
    else if (findings.some((finding) => shouldApplyThreshold(finding.severity, policy.sanitizeAtOrAbove))) {
        status = "sanitize";
    }
    return {
        status,
        highestSeverity,
        messageScans,
        findings,
    };
}
//# sourceMappingURL=dlp.js.map