const message = document.getElementById('message');

function showMessage(text, ok = true) {
  message.textContent = text;
  message.style.color = ok ? '#166534' : '#b91c1c';
}

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || 'Ocurrió un error.');
  return data;
}

async function loadDashboard() {
  try {
    const period = document.getElementById('period').value;
    const data = await request(`/api/dashboard?period=${encodeURIComponent(period)}`);
    const labels = [
      ['Incidentes', data.incidents],
      ['Días perdidos', data.lost_days],
      ['Personal', data.personnel],
      ['Registros IPER', data.iper_records],
      ['Riesgo crítico', data.critical_risk_records],
    ];
    document.getElementById('metrics').innerHTML = labels.map(([name, value]) =>
      `<div class="metric"><strong>${value}</strong><span>${name}</span></div>`).join('');
    document.getElementById('byType').innerHTML = Object.entries(data.incidents_by_person_type)
      .map(([key, value]) => `<div class="item">${key}: <strong>${value}</strong></div>`).join('') || '<div class="item">Sin datos</div>';
    document.getElementById('bySeverity').innerHTML = Object.entries(data.incidents_by_severity)
      .map(([key, value]) => `<div class="item">${key}: <strong>${value}</strong></div>`).join('') || '<div class="item">Sin datos</div>';
  } catch (error) { showMessage(error.message, false); }
}

async function loadTables() {
  try {
    const [personnel, incidents] = await Promise.all([
      request('/api/personnel'), request('/api/incidents')
    ]);
    document.getElementById('personnelTable').innerHTML = personnel.map(item =>
      `<tr><td>${item.full_name}</td><td>${item.dni}</td><td>${item.company}</td><td>${item.status}</td></tr>`).join('') || '<tr><td colspan="4">Sin registros</td></tr>';
    document.getElementById('incidentTable').innerHTML = incidents.map(item =>
      `<tr><td>${item.incident_date}</td><td>${item.project_name}</td><td>${item.injured_name}</td><td>${item.severity_type}</td><td>${item.lost_days}</td></tr>`).join('') || '<tr><td colspan="5">Sin registros</td></tr>';
  } catch (error) { showMessage(error.message, false); }
}

async function submitJsonForm(formId, url) {
  const form = document.getElementById(formId);
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    if ('lost_days' in data) data.lost_days = Number(data.lost_days);
    try {
      await request(url, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
      form.reset();
      showMessage('Registro guardado correctamente.');
      await Promise.all([loadDashboard(), loadTables()]);
    } catch (error) { showMessage(error.message, false); }
  });
}

document.getElementById('excelForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  try {
    const data = await request('/api/import-excel', { method: 'POST', body: formData });
    showMessage(`Importación correcta: ${data.imported} incidentes.`);
    event.target.reset();
    await Promise.all([loadDashboard(), loadTables()]);
  } catch (error) { showMessage(error.message, false); }
});

submitJsonForm('personnelForm', '/api/personnel');
submitJsonForm('incidentForm', '/api/incidents');
loadDashboard();
loadTables();
