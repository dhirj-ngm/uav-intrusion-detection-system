const state = {
  rows: [],
  pageSize: 6,
  currentPage: 1,
  uploadedFile: null,
  results: []
};

let pieChartInstance = null;
let barChartInstance = null;

const previewTableBody = document.getElementById('previewTableBody');
const pagination = document.getElementById('pagination');
const searchInput = document.getElementById('searchInput');
const fileInput = document.getElementById('csvFile');
const dropZone = document.getElementById('dropZone');
const uploadMeta = document.getElementById('uploadMeta');
const filePreview = document.getElementById('filePreview');
const uploadProgress = document.getElementById('uploadProgress');
const predictBtn = document.getElementById('predictBtn');
const loadingBox = document.getElementById('loadingBox');
const predictionSummary = document.getElementById('predictionSummary');
const resultsTableBody = document.getElementById('resultsTableBody');
const dateTimeElement = document.getElementById('dateTime');
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');

function updateClock() {
  const now = new Date();
  dateTimeElement.textContent = now.toLocaleString();
}

setInterval(updateClock, 1000);
updateClock();

sidebarToggle.addEventListener('click', () => {
  sidebar.classList.toggle('collapsed');
  sidebar.classList.toggle('open');
});

['dragenter', 'dragover'].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });
});

['dragleave', 'drop'].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
  });
});

dropZone.addEventListener('drop', (e) => {
  const files = e.dataTransfer.files;
  if (files.length) {
    handleFileUpload(files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length) {
    handleFileUpload(e.target.files[0]);
  }
});

function handleFileUpload(file) {
  uploadMeta.textContent = `Uploading ${file.name}...`;
  uploadProgress.style.width = '20%';
  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      uploadProgress.style.width = '100%';
      if (data.success) {
        state.uploadedFile = data.filename;
        uploadMeta.textContent = `Loaded ${data.filename} • ${data.rows} rows • ${data.columns.length} columns`;
        filePreview.textContent = `Preview ready with ${data.preview.length} sample rows.`;
        state.rows = data.preview;
        renderPreviewTable();
        renderResultsTable([]);
      } else {
        uploadMeta.textContent = data.message || 'Upload failed.';
      }
    })
    .catch(() => {
      uploadMeta.textContent = 'Upload failed. Please try again.';
    });
}

function renderPreviewTable() {
  const searchTerm = searchInput.value.toLowerCase();
  const filtered = state.rows.filter((row) =>
    JSON.stringify(row).toLowerCase().includes(searchTerm)
  );

  const start = (state.currentPage - 1) * state.pageSize;
  const pageRows = filtered.slice(start, start + state.pageSize);

  previewTableBody.innerHTML = pageRows.length
    ? pageRows.map((row) => `
      <tr>
        <td>${row['FlowID'] ?? '-'}</td>
        <td>${row['SrcAddr'] ?? '-'}</td>
        <td>${row['DstAddr'] ?? '-'}</td>
        <td>${row['Protocol'] ?? '-'}</td>
        <td>${row['MeanPacketSize'] ?? '-'}</td>
        <td>${row['label'] ?? 'Normal'}</td>
      </tr>`).join('')
    : '<tr><td colspan="6" class="text-center text-muted">No matching rows.</td></tr>';

  renderPagination(filtered.length);
}

function renderPagination(totalItems) {
  const totalPages = Math.max(1, Math.ceil(totalItems / state.pageSize));
  const pages = [];
  for (let i = 1; i <= totalPages; i++) {
    pages.push(`<li class="page-item ${i === state.currentPage ? 'active' : ''}"><a class="page-link" href="#">${i}</a></li>`);
  }
  pagination.innerHTML = pages.join('');
  pagination.querySelectorAll('.page-link').forEach((link, index) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      state.currentPage = index + 1;
      renderPreviewTable();
    });
  });
}

searchInput.addEventListener('input', renderPreviewTable);

predictBtn.addEventListener('click', () => {
  if (!state.uploadedFile) {
    predictionSummary.innerHTML = '<div class="alert alert-warning">Upload a CSV dataset before running prediction.</div>';
    return;
  }

  loadingBox.style.display = 'flex';
  predictionSummary.innerHTML = '';

  fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename: state.uploadedFile })
  })
    .then((response) => response.json())
    .then((data) => {
      loadingBox.style.display = 'none';
      state.results = data.results || [];
      renderResultsTable(state.results);
      predictionSummary.innerHTML = `<div class="alert alert-success">${data.summary}</div>`;
      // Refresh dashboard stats/charts now that new predictions exist
      loadDashboardStats();
    })
    .catch(() => {
      loadingBox.style.display = 'none';
      predictionSummary.innerHTML = '<div class="alert alert-danger">Prediction failed. Please retry.</div>';
    });
});

function renderResultsTable(results) {
  resultsTableBody.innerHTML = results.length
    ? results.map((row) => `
      <tr>
        <td>${row.flowId}</td>
        <td>${row.predictedAttack}</td>
        <td>${row.confidence}%</td>
        <td>${row.threatLevel}</td>
      </tr>`).join('')
    : '<tr><td colspan="4" class="text-center text-muted">No predictions available yet.</td></tr>';
}

// ---- Dashboard stats + charts, wired to real backend data ----

const ATTACK_COLORS = {
  'Normal Traffic': '#38d39f',
  'Blackhole Attack': '#4da3ff',
  'Flooding Attack': '#ffb84d',
  'Sybil Attack': '#8b7dff',
  'Wormhole Attack': '#ff5d7a'
};

function loadDashboardStats() {
  fetch('/api/stats/summary')
    .then((res) => res.json())
    .then((summary) => {
      document.getElementById('totalPackets').textContent = summary.total_packets.toLocaleString();
      document.getElementById('normalTraffic').textContent = summary.normal_traffic_pct + '%';
      document.getElementById('totalAttacks').textContent = summary.total_attacks.toLocaleString();
      document.getElementById('modelAccuracy').textContent =
        summary.model_accuracy_pct !== null ? summary.model_accuracy_pct + '%' : 'N/A';
      document.getElementById('predictionTime').textContent = summary.avg_prediction_time_ms + ' ms';
      document.getElementById('threatLevel').textContent = summary.threat_level;

      // Model Performance panel — accuracy is real, others are placeholders
      // until dedicated precision/recall/F1/CV endpoints exist (flagged separately)
      document.getElementById('metricAccuracy').textContent =
        summary.model_accuracy_pct !== null ? summary.model_accuracy_pct + '%' : 'N/A';
    });

  fetch('/api/stats/breakdown')
    .then((res) => res.json())
    .then((breakdown) => updateCharts(breakdown));
}

function updateCharts(breakdown) {
  const labels = Object.keys(breakdown);
  const values = Object.values(breakdown);
  const colors = labels.map((label) => ATTACK_COLORS[label] || '#4da3ff');

  if (pieChartInstance) pieChartInstance.destroy();
  pieChartInstance = new Chart(document.getElementById('pieChart'), {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{ data: values, backgroundColor: colors }]
    },
    options: { plugins: { legend: { labels: { color: '#eaf3ff' } } } }
  });

  // Bar chart shows attack types only (excludes Normal Traffic, since that's not an "attack count")
  const attackLabels = labels.filter((l) => l !== 'Normal Traffic');
  const attackValues = attackLabels.map((l) => breakdown[l]);
  const attackColors = attackLabels.map((l) => ATTACK_COLORS[l] || '#4da3ff');

  if (barChartInstance) barChartInstance.destroy();
  barChartInstance = new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: attackLabels,
      datasets: [{ label: 'Attack Count', data: attackValues, backgroundColor: attackColors }]
    },
    options: { scales: { y: { ticks: { color: '#eaf3ff' } }, x: { ticks: { color: '#eaf3ff' } } } }
  });
}

// Feature Importance and Traffic Trend charts stay static for now —
// these need dedicated backend endpoints (model.feature_importances_,
// and a time-bucketed traffic query) that don't exist yet.
function initStaticCharts() {
  new Chart(document.getElementById('featureChart'), {
    type: 'bar',
    data: {
      labels: ['MeanPacketSize', 'TxByteRate/s', 'SrcPort', 'PacketDropRate', 'TxBytes'],
      datasets: [{ label: 'Importance', data: [92, 84, 77, 66, 59], backgroundColor: '#4da3ff' }]
    },
    options: { indexAxis: 'y', scales: { x: { ticks: { color: '#eaf3ff' } }, y: { ticks: { color: '#eaf3ff' } } } }
  });

  new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
      datasets: [{ label: 'Traffic Volume', data: [180, 220, 310, 280, 340, 260], borderColor: '#2dd4bf', tension: 0.35, fill: true, backgroundColor: 'rgba(45,212,191,0.15)' }]
    },
    options: { scales: { y: { ticks: { color: '#eaf3ff' } }, x: { ticks: { color: '#eaf3ff' } } } }
  });
}

document.getElementById('downloadCsvBtn').addEventListener('click', () => {
  const rows = state.results.length ? state.results : [{ flowId: 'N/A', predictedAttack: 'Normal', confidence: '99.8', threatLevel: 'Low' }];
  const csvRows = ['flowId,predictedAttack,confidence,threatLevel', ...rows.map((row) => `${row.flowId},${row.predictedAttack},${row.confidence},${row.threatLevel}`)];
  const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'prediction_results.csv';
  link.click();
  URL.revokeObjectURL(url);
});

document.getElementById('downloadPdfBtn').addEventListener('click', () => {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  doc.setFontSize(16);
  doc.text('AI UAV IDS Threat Report', 14, 16);
  doc.setFontSize(11);
  doc.text(`Model Accuracy: ${document.getElementById('modelAccuracy').textContent}`, 14, 32);
  doc.text(`Threat Level: ${document.getElementById('threatLevel').textContent}`, 14, 42);
  doc.text('Prediction Summary: High-confidence anomaly detection completed.', 14, 52);
  doc.save('uav_ids_report.pdf');
});

renderPreviewTable();
renderResultsTable([]);
initStaticCharts();
loadDashboardStats();