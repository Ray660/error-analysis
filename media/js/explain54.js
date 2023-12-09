

document.getElementById("nextButton").addEventListener("click", function (){
    var known = document.getElementById("known")
    var q1 = document.getElementById("q1")
    var style1 = window.getComputedStyle(q1)
    var a1 = document.getElementById("1")
    var q2 = document.getElementById("q2")
    var style2 = window.getComputedStyle(q2)
    var a2 = document.getElementById("2")
    var q3 = document.getElementById("q3")
    var style3 = window.getComputedStyle(q3)
    var a3 = document.getElementById("3")
    var next = document.getElementById("nextButton")
    var back = document.getElementById("back")

    if (known.style.display === 'none' && style1.display === 'none'){
        known.style.display = 'block';
        q1.style.display = 'block';
    } else if (q1.style.display === 'block' && style2.display === 'none'){
        a1.style.display = 'block';
        q2.style.display = 'block';
    } else if (q2.style.display === 'block' && style3.display === 'none'){
        a2.style.display = 'block';
        q3.style.display = 'block';
    } else if (q3.style.display === 'block'){
        a3.style.display = 'block';
        next.style.display = 'none';
        back.style.display = 'block';
    }
})