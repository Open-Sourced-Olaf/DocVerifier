document.getElementById("myButton").addEventListener("click", myFunction);
function myFunction() {
  console.log("asd");

  var url = "";
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    url = tabs[0].url;

    document.getElementById("description").style.display = "none";
    document.getElementById("resultButton").style.display = "none";
    document.getElementById("loader").style.display = "block";
    document.getElementById("loading-text").innerHTML = "Loading...";

    fetch("https://check-privacy.herokuapp.com/test", {
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
        document.getElementById("out").innerHTML = data["bad"][0];
        document.getElementById("resultButton").style.display = "block";
        document.getElementById("loader").style.display = "none";
        document.getElementById("loading-text").innerHTML = "";
      });
  });
}
document.getElementById("resultButton").addEventListener("click", predict);
function predict() {
  window.open("https://check-privacy.herokuapp.com/predict");
}
