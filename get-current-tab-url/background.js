document.getElementById("myButton").addEventListener("click", myFunction);
function myFunction() {
  console.log("asd");

  var url = "";
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    url = tabs[0].url;

    document.getElementById("demo").innerHTML = url;

    fetch("http://localhost:5000/test", {
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
        
        document.getElementById("out").innerHTML = data["greeting"];
      });
  });
}
document.getElementById("resultButton").addEventListener("click", predict);
function predict() {
  window.open("http://localhost:5000/predict");
}
