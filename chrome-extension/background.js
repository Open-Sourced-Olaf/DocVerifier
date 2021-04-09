document.getElementById("myButton").addEventListener("click", myFunction);

function myFunction() {
  var url = "";
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    url = tabs[0].url;

    // Make loading spinner visible
    document.getElementById("description").style.display = "none";
    document.getElementById("resultButton").style.display = "none";
    document.getElementById("loader").style.display = "block";
    document.getElementById("loading-text").innerHTML = "Loading...";

    // Fetch scraped data from URL
    fetch("http://localhost:5000/scrape", {
      method: "post",
      headers: {
        Accept: "application/json, text/plain, */*",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tabUrl: url }),
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        // Display the bad policies as output and hide loader
        document.getElementById("out").innerHTML = data["bad"][7];
        document.getElementById("resultButton").style.display = "block";
        document.getElementById("loader").style.display = "none";
        document.getElementById("loading-text").innerHTML = "";
      });
  });
}

// Redirect to the result page
document.getElementById("resultButton").addEventListener("click", predict);
function predict() {
  window.open("http://localhost:5000/predict");
}
