const citiesByState = {
  "NSW": ["Albury","BadgerysCreek", "Cobar", "CoffsHarbour", "Moree", "Newcastle", "NorahHead", "Penrith", "Richmond", "Sydney", "SydneyAirport", "WaggaWagga", "Williamtown", "Wollongong"],
  "VIC": ["Ballarat", "Bendigo", "Sale", "MelbourneAirport", "Melbourne", "Mildura", "Nhil", "Portland", "Watsonia", "Dartmoor"],
  "QLD": ["Brisbane", "Cairns", "GoldCoast", "Townsville"],
  "SA": ["Adelaide", "MountGambier", "Nuriootpa", "Woomera"],
  "WA": ["Albany", "Witchcliffe", "PearceRAAF", "PerthAirport", "Perth", "SalmonGums", "Walpole"],
  "TAS": ["Hobart", "Launceston"],
  "ACT": ["Canberra", "Tuggeranong", "MountGinini"],
  "NT": ["AliceSprings", "Darwin", "Katherine", "Uluru"],
  "Other": ["NorfolkIsland"]
};
//Create Echart instance
var dom = document.getElementById('container_hr');
var myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: false
});
var app = {};

var option;

// Function to update the city options based on the selected state
function updateCities() {
  const stateSelect = document.getElementById("state-select");
  const citySelect = document.getElementById("city-select");
  const selectedState = stateSelect.value;

  // Clear existing city options
  citySelect.innerHTML = "";

  // Populate city options based on the selected state
  citiesByState[selectedState].forEach(city => {
      const option = document.createElement("option");
      option.text = city;
      option.value = city;
      citySelect.add(option);
  });

  // Select the first city by default
  if (citySelect.options.length > 0) {
    citySelect.selectedIndex = 0;
    // Trigger AJAX request for the first city
    sendCityToBackend();
  }
}

 // Function to send selected city to backend using AJAX
 function sendCityToBackend() {
  const selectedCity = document.getElementById("city-select").value;
  console.log("Selected city:", selectedCity);
  const csrftoken = getCookie('csrftoken'); // Get CSRF token
  $.ajax({
      url: "/rainAU/sel_city/",
      type: "POST",
      data: {
          city: selectedCity
      },
      headers: {
        'X-CSRFToken': csrftoken // Add CSRF token to headers
      },
      success: function(response) {
          // Handle successful response from backend
          updateChart(response);
          updateHeading(response.loc);
      },
      error: function(xhr, status, error) {
          // Handle errors
          console.error("Error sending city to backend:", error);
      }
  });
}

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Update h1 content
function updateHeading(city) {
  // Select the h1 element and update its text content with the selected city
  $("h1#city-heading").text("Rainfall vs Evaporation in " + city);
}

// Update chart data
function updateChart(data) {
  // Extract date, rainfall, and evaporation data from the response
  var dateList = data.date_list;
  var rainfallList = data.first_list;
  var evaporationList = data.second_list;

  option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['Rainfall', 'Evaporation']
    },
    toolbox: {
      show: true,
      feature: {
        dataView: { show: true, readOnly: false },
        magicType: { show: true, type: ['line', 'bar'] },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    calculable: true,
    xAxis: [
      {
        type: 'category',
        // prettier-ignore
        data: dateList
      }
    ],
    yAxis: [
      {
        type: 'value'
      }
    ],
    series: [
      {
        name: 'Rainfall',
        type: 'bar',
        data: rainfallList,
        markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' }
          ]
        },
        markLine: {
          data: [{ type: 'average', name: 'Avg' }]
        }
      },
      {
        name: 'Evaporation',
        type: 'bar',
        data: evaporationList,
        markPoint: {
          data: [
            { name: 'Max', value: 182.2, xAxis: 7, yAxis: 183 },
            { name: 'Min', value: 2.3, xAxis: 11, yAxis: 3 }
          ]
        },
        markLine: {
          data: [{ type: 'average', name: 'Avg' }]
        }
      }
    ]
  };
  
  if (option && typeof option === 'object') {
    myChart.setOption(option);
  }
  
  window.addEventListener('resize', myChart.resize);
}

// Call updateCities() initially to populate city options for the default state
updateCities();
