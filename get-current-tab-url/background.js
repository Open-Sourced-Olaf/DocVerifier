document.getElementById("myButton").addEventListener("click", myFunction);
function myFunction() {
  console.log("asd");

  var url = "";
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    console.log("url", tabs[0].url);
    url = tabs[0].url;
    alert(tabs[0].url);
  });

  document.getElementById("demo").innerHTML = url + "anjali";
}
