document.getElementById("nextButton").addEventListener('click', function (){
    var answersInQ1 = document.querySelectorAll("#q1 .answer");
    var answersInQ2 = document.querySelectorAll("#q2 .answer");
    var answersInQ3 = document.querySelectorAll("#q3 .answer");

    var leadersInQ1 = document.querySelectorAll("#q1 .leader");
    var leadersInQ2 = document.querySelectorAll("#q2 .leader");
    var leadersInQ3 = document.querySelectorAll("#q3 .leader");

    var t2 = document.getElementById("t2");
    var stylet2 = window.getComputedStyle(t2);
    var t3 = document.getElementById("t3");
    var stylet3 = window.getComputedStyle(t3);



    if (stylet2.display === 'none') {
        for (var i = 0; i < answersInQ1.length; i++) {
            var style = window.getComputedStyle(answersInQ1[i]);
            if (style.display === 'none') {
                answersInQ1[i].style.display = 'block';
                if (i + 1 < leadersInQ1.length) {
                    leadersInQ1[i + 1].style.display = 'block'; // 显示下一个leader
                } else {
                    t2.style.display = 'block';
                    leadersInQ2[0].style.display = 'block';
                }
                break;
            }
        }
    }

    else if (t2.style.display === 'block' && stylet3.display === 'none') {
        for (var i = 0; i < answersInQ2.length; i++) {
            var style = window.getComputedStyle(answersInQ2[i]);
            if (style.display === 'none') {
                answersInQ2[i].style.display = 'block';
                if (i + 1 < leadersInQ2.length) {
                    leadersInQ2[i + 1].style.display = 'block'; // 显示下一个leader
                } else {
                    t3.style.display = 'block';
                    leadersInQ3[0].style.display = 'block';
                }
                break;
            }
        }
    }

    else if (t3.style.display === 'block') {
        for (var i = 0; i < answersInQ3.length; i++) {
            var style = window.getComputedStyle(answersInQ3[i]);
            if (style.display === 'none') {
                answersInQ3[i].style.display = 'block';
                if (i + 1 < leadersInQ3.length) {
                    leadersInQ3[i + 1].style.display = 'block'; // 显示下一个leader
                } else {
                    // 检查是否所有的answer都已经显示，如果是，则隐藏next按钮，显示back按钮
                    var answers = document.querySelectorAll(".answer")
                    var allVisible = Array.from(answers).every(ans => window.getComputedStyle(ans).display !== 'none');
                    if (allVisible) {
                        document.getElementById("nextButton").style.display = 'none';
                        document.getElementById("back").style.display = 'block';
                    }
                }
                break;
            }
        }
    }

})


