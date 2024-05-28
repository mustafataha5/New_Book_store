


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
    //console.log(rev_level)
    // output.innerText = "Rating is: " + n + "/5";
}
 
function gfg_this(ele,n) {
    mystars = ele.children
    for (let i = 0; i < n; i++) {
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        
        mystars[i].className = "star " + cls;
    }
    //console.log(rev_level)
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



myshow = document.querySelectorAll('.myshow')

document.addEventListener('DOMContentLoaded', function() {
    // Set the initial rating value here
   // console.log('**********')
    //console.log('**********',myshow.length)
    for( i =0 ;i<myshow.length;i++){
    const initialRating = 3; // Change this value as needed
    //console.log(myshow[i],'**********',myshow[i].value)
    gfg_this(myshow[i],myshow[i].getAttribute('value'));
  }
});




function get_ajax(bookID) {
    var xhr = new XMLHttpRequest();
    console.log('/ajax/'+bookID)
    xhr.open('GET', '/ajax/'+bookID, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var itemsList = document.getElementById('items-list');
            itemsList.innerHTML = '';
            data.forEach(function(item) {
                var listItem = document.createElement('li');
                listItem.textContent = item.user + ': ' + item.review_level+" : "+item.book+"  "+item.message
                itemsList.appendChild(listItem);
            });
        }
    };
    xhr.send();
} 























