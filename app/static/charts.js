chartColours = [
  "#ff6384",
  "#36a2eb",
  "#ffce56",
  "#4bc0c0",
  "#9966ff",
  "#ff9f40",
  "#c9cbcf",
  "#7bc22d",
  "#be29ec",
  "#d42222",
  "#22cece",
  "#1c1c1c",
];

function render_bar_chart(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  const isMobile = window.innerWidth < 768;

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: data.graph_name,
          data: data.values,
          backgroundColor: chartColours,
        },
      ],
    },
    options: {
      scales: {
        x: {
          display: !isMobile, // hides labels on mobile
        },
      },
    },
  });
}

function render_logarithmic_bar_chart(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  const isMobile = window.innerWidth < 768;

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: data.graph_name + " - Logarithmic",
          data: data.values,
          backgroundColor: chartColours,
        },
      ],
    },
    options: {
      scales: {
        y: {
          display: true,
          type: "logarithmic",
        },
        x: {
          display: !isMobile, // hides labels on mobile
        },
      },
    },
  });
}

function render_doughnut_chart(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  const isMobile = window.innerWidth < 768;

  new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: data.graph_name,
          data: data.values,
          backgroundColor: chartColours,
          hoverOffset: 10,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      layout: {
        padding: 20,
      },
      plugins: {
        legend: {
          position: "bottom",
          display: !isMobile, // hides legend on mobile
        },
      },
    },
  });
}
