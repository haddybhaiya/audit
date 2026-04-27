const API_BASE_URL = "https://auditt.up.railway.app";
const DEFAULT_PREDICT_URL = `${API_BASE_URL}/mock/`;

const elements = {
  csvFile: document.getElementById("csvFile"),
  prediction: document.getElementById("prediction"),
  protected: document.getElementById("protected"),
  predictUrl: document.getElementById("predictUrl"),
  allowLocalPredictUrl: document.getElementById("allowLocalPredictUrl"),
  runAuditBtn: document.getElementById("runAuditBtn"),
  btnText: document.getElementById("btnText"),
  btnSpinner: document.getElementById("btnSpinner"),
  errorMessage: document.getElementById("errorMessage"),
  statusMessage: document.getElementById("statusMessage"),
  severityCards: document.getElementById("severityCards"),
  metricsPanel: document.getElementById("metricsPanel"),
  summaryText: document.getElementById("summaryText"),
  llmText: document.getElementById("llmText")
};

initializeDefaults();
elements.runAuditBtn.addEventListener("click", runAuditFlow);

function initializeDefaults() {
  if (!elements.predictUrl.value.trim()) {
    elements.predictUrl.value = DEFAULT_PREDICT_URL;
  }
  renderSeverityCards({ critical: 0, high: 0, low: 0 });
}

async function runAuditFlow() {
  hideMessage(elements.errorMessage);
  showMessage(elements.statusMessage, "Uploading file...");

  const file = elements.csvFile.files && elements.csvFile.files[0];
  const prediction = elements.prediction.value.trim();
  const protectedColumn = elements.protected.value.trim();

  if (!file) {
    showError("Please select a CSV file before running the audit.");
    return;
  }

  if (!prediction || !protectedColumn) {
    showError("Prediction and protected column fields are required.");
    return;
  }

  setLoading(true);

  try {
    const uploadedFilename = await uploadCsv(file);

    showMessage(elements.statusMessage, "Generating report...");

    const reportResponse = await fetch(`${API_BASE_URL}/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: uploadedFilename,
        prediction,
        protected: protectedColumn,
        predict_url: elements.predictUrl.value.trim(),
        allow_local_predict_url: Boolean(elements.allowLocalPredictUrl.checked)
      })
    });

    if (!reportResponse.ok) {
      throw new Error(await extractError(reportResponse, "Report request failed."));
    }

    const reportData = await reportResponse.json();
    renderReport(reportData);
    showMessage(elements.statusMessage, "Audit completed successfully.");
  } catch (error) {
    showError(error.message || "Something went wrong while running the audit.");
  } finally {
    setLoading(false);
  }
}

async function uploadCsv(file) {
  const payload = new FormData();
  payload.append("file", file);

  const uploadResponse = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: payload
  });

  if (!uploadResponse.ok) {
    throw new Error(await extractError(uploadResponse, "Upload failed."));
  }

  const uploadData = await uploadResponse.json();
  const uploadedFilename =
    uploadData.filename ||
    uploadData.stored_filename ||
    uploadData.file ||
    (uploadData.data && uploadData.data.filename);

  if (!uploadedFilename) {
    throw new Error("Upload succeeded but no filename was returned by the server.");
  }

  return uploadedFilename;
}

function renderReport(data) {
  const severityCounts = parseSeverity(data);
  renderSeverityCards(severityCounts);

  const metrics = parseMetrics(data);
  renderMetrics(metrics);

  elements.summaryText.textContent = formatTextBlock(
    firstDefined([
      data.summary,
      data.report_summary,
      data.result && data.result.summary,
      data.message
    ]),
    "No summary available."
  );

  elements.llmText.textContent = formatTextBlock(
    firstDefined([
      data.llm_explanation,
      data.explanation,
      data.analysis,
      data.result && data.result.llm_explanation
    ]),
    "No LLM explanation available."
  );
}

function parseSeverity(data) {
  const source =
    data.severity_counts ||
    data.severity ||
    data.risk_levels ||
    (data.result && data.result.severity_counts) ||
    {};

  if (source && typeof source === "object" && !Array.isArray(source)) {
    if (
      Object.prototype.hasOwnProperty.call(source, "critical") ||
      Object.prototype.hasOwnProperty.call(source, "high") ||
      Object.prototype.hasOwnProperty.call(source, "low")
    ) {
      return {
        critical: toCount(source.critical),
        high: toCount(source.high),
        low: toCount(source.low)
      };
    }

    const counts = { critical: 0, high: 0, low: 0 };
    Object.values(source).forEach((value) => {
      const level = String(value).toLowerCase();
      if (Object.prototype.hasOwnProperty.call(counts, level)) {
        counts[level] += 1;
      }
    });
    return counts;
  }

  return { critical: 0, high: 0, low: 0 };
}

function parseMetrics(data) {
  const source =
    data.metrics ||
    data.fairness_metrics ||
    (data.result && data.result.metrics) ||
    {};

  if (!source || typeof source !== "object" || Array.isArray(source)) {
    return {};
  }

  return source;
}

function renderSeverityCards(counts) {
  const levels = ["critical", "high", "low"];
  elements.severityCards.innerHTML = levels
    .map((level) => {
      const count = toCount(counts[level]);
      return `
        <div class="severity-card severity-${level}">
          <div class="label">${level}</div>
          <div class="value">${count}</div>
        </div>
      `;
    })
    .join("");
}

function renderMetrics(metrics) {
  const entries = Object.entries(metrics);

  if (!entries.length) {
    elements.metricsPanel.textContent = "No metrics available.";
    elements.metricsPanel.classList.add("muted");
    return;
  }

  elements.metricsPanel.classList.remove("muted");
  elements.metricsPanel.innerHTML = entries
    .map(([key, value]) => {
      const formattedKey = String(key).replace(/_/g, " ");
      const formattedValue = formatMetricValue(value);
      return `
        <div class="metric-row">
          <span class="metric-key">${escapeHtml(formattedKey)}</span>
          <span class="metric-value">${escapeHtml(formattedValue)}</span>
        </div>
      `;
    })
    .join("");
}

function setLoading(isLoading) {
  elements.runAuditBtn.disabled = isLoading;
  elements.btnSpinner.classList.toggle("hidden", !isLoading);
  elements.btnText.textContent = isLoading ? "Running..." : "Upload & Run Audit";
}

function showError(message) {
  hideMessage(elements.statusMessage);
  showMessage(elements.errorMessage, message);
}

function showMessage(target, message) {
  target.textContent = message;
  target.classList.remove("hidden");
}

function hideMessage(target) {
  target.textContent = "";
  target.classList.add("hidden");
}

function toCount(value) {
  if (Array.isArray(value)) {
    return value.length;
  }
  const number = Number(value);
  return Number.isFinite(number) ? number : 0;
}

function formatMetricValue(value) {
  if (value === null || value === undefined) {
    return "N/A";
  }
  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toFixed(4);
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

async function extractError(response, fallback) {
  try {
    const body = await response.json();
    return body.detail || body.message || JSON.stringify(body) || fallback;
  } catch (_) {
    return fallback;
  }
}

function firstDefined(values) {
  return values.find(
    (value) =>
      value !== null &&
      value !== undefined &&
      (typeof value !== "string" || value.trim().length > 0)
  );
}

function formatTextBlock(value, fallback) {
  if (value === null || value === undefined) {
    return fallback;
  }
  if (typeof value === "string") {
    return value.trim() || fallback;
  }
  if (typeof value === "object") {
    return JSON.stringify(value, null, 2);
  }
  return String(value);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
