function render_bar_chart(canvasId, data) {
  const canvas = document.getElementById(canvasId);

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: data.graph_name,
          data: data.values,
        },
      ],
    },
  });
}

function render_logarithmic_bar_chart(canvasId, data) {
  const canvas = document.getElementById(canvasId);

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: data.graph_name + " - Logarithmic",
          data: data.values,
        },
      ],
    },
    options: {
      scales: {
        y: {
          display: true,
          type: "logarithmic",
        },
      },
    },
  });
}

function render_doughnut_chart(canvasId, data) {
  const canvas = document.getElementById(canvasId);

  new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: data.graph_name,
          data: data.values,
          backgroundColor: [
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
          ],
          hoverOffset: 10,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true, // Keeps it a circle
      // This is the magic property to shrink the actual circle
      // without shrinking the legend
      layout: {
        padding: 20,
      },
      plugins: {
        legend: {
          position: "top",
        },
      },
    },
  });
}
