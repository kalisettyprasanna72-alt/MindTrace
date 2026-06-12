const appData = {
  currentStep: 0,
  totalSteps: 10,
  responses: [],
  modules: [
    {
      title: 'Sleep Patterns',
      summary: 'Evaluate your sleep duration and quality.',
      fields: [
        { id: 'sleepDuration', label: 'Sleep Duration (hours)', type: 'range', min: 2, max: 12, step: 0.5, value: 7, suffix: 'hrs' },
        { id: 'sleepQuality', label: 'Sleep Quality', type: 'select', options: ['Poor', 'Fair', 'Good', 'Excellent'], value: 'Good' }
      ]
    },
    {
      title: 'Screen Time',
      summary: 'Track your daily screen exposure and pre-sleep habits.',
      fields: [
        { id: 'screenTime', label: 'Screen Time (hours)', type: 'range', min: 0, max: 16, step: 0.5, value: 6, suffix: 'hrs' },
        { id: 'preSleepScreen', label: 'Pre-sleep Screen Usage', type: 'select', options: ['None', 'Low', 'Moderate', 'High'], value: 'Moderate' }
      ]
    },
    {
      title: 'Study Hours',
      summary: 'Understand your study load and break routine.',
      fields: [
        { id: 'studyHours', label: 'Study Hours per Day', type: 'range', min: 0, max: 16, step: 0.5, value: 5, suffix: 'hrs' },
        { id: 'studyBreakPattern', label: 'Study Break Pattern', type: 'select', options: ['None', 'Occasional', 'Regular', 'Frequent'], value: 'Regular' }
      ]
    },
    {
      title: 'Stress Level',
      summary: 'Measure daily stress and anxiety tendencies.',
      fields: [
        { id: 'stressLevel', label: 'Stress Level', type: 'range', min: 1, max: 10, value: 5 },
        { id: 'anxietyEpisodes', label: 'Anxiety Episodes', type: 'number', min: 0, max: 10, value: 2 }
      ]
    },
    {
      title: 'Physical Activity',
      summary: 'Capture exercise habits and activity intensity.',
      fields: [
        { id: 'exerciseMinutes', label: 'Exercise Minutes', type: 'range', min: 0, max: 120, value: 30, suffix: 'min' },
        { id: 'activityType', label: 'Activity Type', type: 'select', options: ['Low', 'Moderate', 'High', 'Very High'], value: 'Moderate' }
      ]
    },
    {
      title: 'Nutrition & Hydration',
      summary: 'Track your fluid intake and meal regularity.',
      fields: [
        { id: 'waterIntake', label: 'Water Intake (liters)', type: 'range', min: 0.5, max: 5, step: 0.1, value: 2.2, suffix: 'L' },
        { id: 'mealRegularity', label: 'Meal Regularity', type: 'select', options: ['Irregular', 'Occasional', 'Consistent', 'Structured'], value: 'Consistent' }
      ]
    },
    {
      title: 'Mood Tracking',
      summary: 'Gauge your mood and emotional state.',
      fields: [
        { id: 'moodScore', label: 'Mood Score', type: 'range', min: 1, max: 10, value: 6 },
        { id: 'irritability', label: 'Irritability', type: 'select', options: ['None', 'Low', 'Moderate', 'High'], value: 'Low' }
      ]
    },
    {
      title: 'Concentration Ability',
      summary: 'Assess focus and distractions.',
      fields: [
        { id: 'focusSpan', label: 'Focus Span (minutes)', type: 'range', min: 5, max: 90, value: 45, suffix: 'min' },
        { id: 'distractionFrequency', label: 'Distraction Frequency', type: 'select', options: ['Rare', 'Sometimes', 'Often', 'Constant'], value: 'Sometimes' }
      ]
    },
    {
      title: 'Caffeine Intake',
      summary: 'Review caffeine and energy drink usage.',
      fields: [
        { id: 'caffeineDrinks', label: 'Caffeine Drinks per Day', type: 'number', min: 0, max: 10, value: 2 },
        { id: 'energyDrink', label: 'Energy Drink Usage', type: 'select', options: ['Never', 'Sometimes', 'Often', 'Daily'], value: 'Sometimes' }
      ]
    },
    {
      title: 'Social & Recovery',
      summary: 'Track breaks and support systems.',
      fields: [
        { id: 'breakTime', label: 'Break Time (hours)', type: 'range', min: 0, max: 8, step: 0.25, value: 1.5, suffix: 'hrs' },
        { id: 'socialSupport', label: 'Social Support', type: 'select', options: ['None', 'Limited', 'Moderate', 'Strong'], value: 'Moderate' }
      ]
    }
  ]
};

const moduleElements = {
  stepLabel: document.getElementById('module-number'),
  title: document.getElementById('module-title'),
  summary: document.getElementById('module-summary'),
  form: document.getElementById('module-form'),
  progress: document.getElementById('progress-bar'),
  progressStep: document.getElementById('progress-step'),
  progressPercent: document.getElementById('progress-percent'),
  analyzeSection: document.getElementById('results-section'),
  analyzeBtn: document.getElementById('analyze-btn'),
  analyzeLoader: document.getElementById('analyze-loader'),
  fatigueScore: document.getElementById('fatigue-score'),
  wellnessScore: document.getElementById('wellness-score'),
  levelBadge: document.getElementById('level-badge'),
  radarChart: document.getElementById('radarChart').getContext('2d'),
  barChart: document.getElementById('barChart').getContext('2d'),
  recommendations: document.getElementById('recommendations'),
  startBtn: document.getElementById('start-btn'),
  prevBtn: document.getElementById('prev-btn'),
  nextBtn: document.getElementById('next-btn'),
  saveBtn: document.getElementById('save-btn')
};

const rangeValueLabels = {};
let radarChart, barChart;

function renderModule(step) {
  const module = appData.modules[step];
  moduleElements.stepLabel.textContent = step + 1;
  moduleElements.title.textContent = module.title;
  moduleElements.summary.textContent = module.summary;
  moduleElements.form.innerHTML = '';

  module.fields.forEach(field => {
    const row = document.createElement('div');
    row.className = 'form-field';

    const label = document.createElement('label');
    label.htmlFor = field.id;
    label.innerHTML = `${field.label} <span class="value-pill" id="value-${field.id}">${field.value}${field.suffix || ''}</span>`;
    row.appendChild(label);

    if (field.type === 'range') {
      const input = document.createElement('input');
      input.type = 'range';
      input.id = field.id;
      input.min = field.min;
      input.max = field.max;
      input.step = field.step || 1;
      input.value = field.value;
      input.addEventListener('input', () => updateRangeValue(field.id, input.value, field.suffix));
      row.appendChild(input);
      rangeValueLabels[field.id] = document.getElementById(`value-${field.id}`);
    } else if (field.type === 'select') {
      const select = document.createElement('select');
      select.id = field.id;
      select.innerHTML = field.options.map(option => `<option value="${option}">${option}</option>`).join('');
      row.appendChild(select);
    } else if (field.type === 'number') {
      const number = document.createElement('input');
      number.type = 'number';
      number.id = field.id;
      number.min = field.min;
      number.max = field.max;
      number.value = field.value;
      row.appendChild(number);
    }

    moduleElements.form.appendChild(row);
    if (field.type === 'range') updateRangeValue(field.id, field.value, field.suffix);
  });
}

function updateRangeValue(id, value, suffix='') {
  const label = document.getElementById(`value-${id}`);
  if (label) {
    label.textContent = `${value}${suffix}`;
  }
}

function updateProgress() {
  const progress = ((appData.currentStep + 1) / appData.totalSteps) * 100;
  moduleElements.progress.style.width = `${progress}%`;
  moduleElements.progressStep.textContent = appData.currentStep + 1;
  moduleElements.progressPercent.textContent = `${Math.round(progress)}%`;
}

function collectCurrentInputs() {
  const module = appData.modules[appData.currentStep];
  const values = {};
  module.fields.forEach(field => {
    const input = document.getElementById(field.id);
    values[field.id] = input ? input.value : field.value;
  });
  appData.responses[appData.currentStep] = values;
}

function applyStageValues() {
  const saved = appData.responses[appData.currentStep];
  if (!saved) return;
  const module = appData.modules[appData.currentStep];
  module.fields.forEach(field => {
    const input = document.getElementById(field.id);
    if (input) {
      input.value = saved[field.id];
      if (field.type === 'range') updateRangeValue(field.id, saved[field.id], field.suffix);
    }
  });
}

function registerNavigation() {
  moduleElements.prevBtn.addEventListener('click', () => {
    if (appData.currentStep === 0) return;
    collectCurrentInputs();
    appData.currentStep -= 1;
    renderModule(appData.currentStep);
    applyStageValues();
    updateProgress();
    updateNavState();
  });

  moduleElements.nextBtn.addEventListener('click', () => {
    if (appData.currentStep === appData.totalSteps - 1) return;
    collectCurrentInputs();
    appData.currentStep += 1;
    renderModule(appData.currentStep);
    applyStageValues();
    updateProgress();
    updateNavState();
  });

  moduleElements.saveBtn.addEventListener('click', () => {
    collectCurrentInputs();
    showToast('Module inputs saved.', 'success');
  });

  moduleElements.startBtn.addEventListener('click', () => {
    document.querySelector('.hero-section').scrollIntoView({ behavior: 'smooth' });
    moduleElements.analyzeSection.classList.remove('hidden');
  });

  moduleElements.analyzeBtn.addEventListener('click', () => {
    collectCurrentInputs();
    simulateAnalysis();
  });
}

function updateNavState() {
  moduleElements.prevBtn.disabled = appData.currentStep === 0;
  moduleElements.nextBtn.disabled = appData.currentStep === appData.totalSteps - 1;
}

function initializeCharts() {
  radarChart = new Chart(moduleElements.radarChart, {
    type: 'radar',
    data: {
      labels: ['Sleep', 'Stress', 'Focus', 'Mood', 'Exercise', 'Hydration'],
      datasets: [{
        label: 'Wellness Profile',
        data: [5, 5, 5, 5, 5, 5],
        backgroundColor: 'rgba(76, 175, 80, 0.16)',
        borderColor: '#4CAF50',
        borderWidth: 2,
        pointBackgroundColor: '#4CAF50'
      }]
    },
    options: {
      scales: {
        r: {
          min: 0,
          max: 10,
          grid: { color: 'rgba(76,175,80,0.18)' },
          angleLines: { color: 'rgba(76,175,80,0.18)' },
          pointLabels: { color: '#4a5a43', font: { size: 13 } }
        }
      },
      plugins: { legend: { display: false } },
      responsive: true
    }
  });

  barChart = new Chart(moduleElements.barChart, {
    type: 'bar',
    data: {
      labels: ['Sleep', 'Stress', 'Screen Time', 'Caffeine', 'Study'],
      datasets: [{
        label: 'Impact Level',
        data: [5, 6, 4, 3, 4],
        backgroundColor: ['#4CAF50', '#FFC107', '#FFB300', '#F44336', '#8BC34A']
      }]
    },
    options: {
      indexAxis: 'y',
      scales: {
        x: {
          beginAtZero: true,
          max: 10,
          grid: { color: 'rgba(76,175,80,0.12)' }
        },
        y: {
          ticks: { color: '#4a5a43' }
        }
      },
      plugins: { legend: { display: false } },
      responsive: true
    }
  });
}

function simulateAnalysis() {
  moduleElements.analyzeBtn.disabled = true;
  moduleElements.analyzeLoader.classList.remove('hidden');
  setTimeout(() => {
    moduleElements.analyzeLoader.classList.add('hidden');
    moduleElements.analyzeBtn.disabled = false;
    const finalScore = computeFatigueScore();
    const wellness = 100 - finalScore;
    const level = finalScore <= 35 ? 'Low Fatigue' : finalScore <= 65 ? 'Medium Fatigue' : 'High Fatigue';
    fillResultCards(finalScore, wellness, level);
    updateCharts(finalScore, wellness);
    renderRecommendations(level);
    moduleElements.analyzeSection.classList.remove('hidden');
    moduleElements.analyzeSection.scrollIntoView({ behavior: 'smooth' });
  }, 1300);
}

function computeFatigueScore() {
  const values = appData.responses.flatMap(obj => Object.entries(obj || {}));
  let score = 20;
  values.forEach(([key, value]) => {
    if (typeof value === 'string') {
      score += value.length % 7;
    } else {
      score += Number(value) * 0.4;
    }
  });
  score += Math.random() * 12;
  return Math.min(100, Math.max(0, Math.round(score)));
}

function fillResultCards(score, wellness, level) {
  moduleElements.fatigueScore.textContent = score;
  moduleElements.wellnessScore.textContent = wellness;
  const className = level === 'Low Fatigue' ? 'level-low' : level === 'Medium Fatigue' ? 'level-medium' : 'level-high';
  moduleElements.levelBadge.textContent = level;
  moduleElements.levelBadge.className = `level-badge ${className}`;
}

function updateCharts(score, wellness) {
  const sleepValue = Math.min(10, Math.max(1, Math.round((110 - score) / 11)));
  radarChart.data.datasets[0].data = [sleepValue, Math.round(score / 12), Math.round(wellness / 10), Math.round(wellness / 12), Math.round((100 - score) / 11), Math.round(wellness / 12)];
  radarChart.update();

  barChart.data.datasets[0].data = [Math.round((100 - score) / 12), Math.round(score / 10), Math.round(score / 11), Math.round(score / 13), Math.round((score + 8) / 12)];
  barChart.update();
}

function renderRecommendations(level) {
  const recommendations = {
    'Low Fatigue': [
      'Keep your current routine and maintain your sleep habits.',
      'Stay hydrated and continue regular study breaks.',
      'Keep tracking your wellness to stay in peak form.'
    ],
    'Medium Fatigue': [
      'Increase nightly sleep by 30 minutes.',
      'Reduce screen time before bed.',
      'Take short breaks every 45 minutes while studying.'
    ],
    'High Fatigue': [
      'Prioritize recovery and rest this week.',
      'Limit caffeine and energy drinks in the evening.',
      'Focus on hydration and light movement daily.'
    ]
  };

  moduleElements.recommendations.innerHTML = recommendations[level]
    .map(text => `<div class="recommendation-card"><h4>Suggestion</h4><p>${text}</p></div>`)
    .join('');
}

function showToast(message, type) {
  const toast = document.createElement('div');
  toast.className = `toast-pill ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add('visible'), 10);
  setTimeout(() => toast.classList.remove('visible'), 2600);
  setTimeout(() => toast.remove(), 3000);
}

function initialize() {
  appData.responses = Array(appData.totalSteps).fill(null);
  renderModule(appData.currentStep);
  updateProgress();
  updateNavState();
  registerNavigation();
  initializeCharts();
}

initialize();
