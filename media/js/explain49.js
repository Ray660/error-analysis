
document.getElementById("nextButton").addEventListener("click", function (){
    var airplane1 = document.getElementById("airplane1")
    var airplane2 = document.getElementById("airplane2")
    var bottun = document.getElementById("nextButton")

    if (airplane1.style.display === "none" && airplane2.style.display === "none") {
    airplane1.style.display = "block";
  } else if (airplane1.style.display === "block" && airplane2.style.display === "none") {
    airplane2.style.display = "block";
    airplane1.style.display = "none";
    bottun.style.display = "none";
    back.style.display = "block";
  }

})