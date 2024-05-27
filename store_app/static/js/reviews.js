


function shutdown_start(ele){
    console.log(">>>>>",ele.getAttribute('data-rating'))
}


function light_start(ele){             
    console.log("<<<<<<>>>>>>>>>>>",ele.getAttribute('data-rating'))
}



function set_star_level(ele){
    console.log("click ",ele.getAttribute('data-rating'))
}


let stars = document.getElementsByClassName("star");
// let output = document.getElementById("output");

rev_level = document.getElementById('review_level')    
// Funtion to update rating
function gfg(n) {
    remove();
    for (let i = 0; i < n; i++) {
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        
        stars[i].className = "star " + cls;
    }
    rev_level.value = n; 
    console.log(rev_level)
    // output.innerText = "Rating is: " + n + "/5";
}
 
// To remove the pre-applied styling
function remove() {
    let i = 0;
    while (i < 5) {
        stars[i].className = "star";
        i++;
    }
}


























