let map = L.map('map').setView([-40, -60], 3);  // prikaz mape
let marker = null;
let polyline = null;
let groupedData = {};

// ucitavanje karte
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

// crtanje linije, putanje
function drawPath(data) {
  if (polyline) {   // ukloni sve prethodne linije, iscrtava se samo trenutno odabrana
    map.removeLayer(polyline);
  }
  const latlngs = data.map(p => [p.lat, p.lon]);
  if (latlngs.length === 0) return;

  polyline = L.polyline(latlngs, { color: 'red' }).addTo(map);  // stvori novu crvenu liniju
}

// grupiranje podataka po minutama
function groupByMinute() {
  groupedData = {};

  satellitePath.forEach(p => {
    const date = new Date(p.timestamp * 1000);
    const key = date.getUTCFullYear() + '-' +
                String(date.getUTCMonth() + 1).padStart(2, '0') + '-' +
                String(date.getUTCDate()).padStart(2, '0') + ' ' +
                String(date.getUTCHours()).padStart(2, '0') + ':' +
                String(date.getUTCMinutes()).padStart(2, '0');

    if (!groupedData[key]) {
      groupedData[key] = [];
    }
    groupedData[key].push(p);
  });

  populateDropdown();
}

// popuni dropdown za sekunde
function populateDropdown() {
  const select = document.getElementById('minuteSelect');
  const label = document.getElementById('minuteLabel');
  const minutes = Object.keys(groupedData).sort();

  if (minutes.length > 0) {
    const firstDate = minutes[0].split(' ')[0];
    label.textContent = `Odaberi minutu putanje, datum: ${firstDate}`;
  }

  minutes.forEach(min => {  // kreiraj dropdown menu za odabir tocnog vremena (u sekundama)
    const timePart = min.split(' ')[1];
    const option = document.createElement('option');
    option.value = min;
    option.textContent = min;
    option.textContent = timePart;
    select.appendChild(option);
  });
}

// akcija nakon odabira opcije minute
function onMinuteSelect() {
  const selectedMinute = document.getElementById('minuteSelect').value;
  const secondSelect = document.getElementById('secondSelect');

  if (marker) {   // ukloni prethodni prikaz
    map.removeLayer(marker);
    marker = null;
  }

  secondSelect.innerHTML = '<option value="minute">-------</option>';

  if (selectedMinute === "all") {   // odabrana opcija za prikaz cijele putanje
    drawPath(satellitePath);
    document.getElementById('secondLabel').textContent = "Odaberi sekundu putanje:";
    return;
  }

  const points = groupedData[selectedMinute] || [];
  drawPath(points);

  if (points.length > 0) {
    const firstDate = new Date(points[0].timestamp * 1000);
    const hour = String(firstDate.getUTCHours()).padStart(2, '0');
    const minute = String(firstDate.getUTCMinutes()).padStart(2, '0');
    document.getElementById('secondLabel').textContent = `Odaberi sekundu putanje: ${hour}:${minute}`;
  }

  points.forEach(p => {
    const date = new Date(p.timestamp * 1000);
    const second = String(date.getUTCSeconds()).padStart(2, '0');
    const label = `${second}`;
    
    const option = document.createElement('option');
    option.value = p.timestamp;
    option.textContent = label;
    secondSelect.appendChild(option);
  });
}

// odabrana je sekunda, prikaz tocke
function onSecondSelect() {
  const secondValue = document.getElementById('secondSelect').value;

  if (marker) {   // ukloni prethodne
    map.removeLayer(marker);
    marker = null;
  }

  if (secondValue === "minute") { // nije odabrana sekunda
    onMinuteSelect();
    return;
  }

  const timestamp = parseInt(secondValue, 10);
  const point = satellitePath.find(p => p.timestamp === timestamp);

  if (point) {
    drawPath([]);

    marker = L.circleMarker([point.lat, point.lon], {
      radius: 2,
      color: 'red',
      fillOpacity: 1
    }).addTo(map);

    map.setView([point.lat, point.lon], map.getZoom());
  }
}


groupByMinute();
drawPath(satellitePath);