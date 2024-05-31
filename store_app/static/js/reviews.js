



let stars = document.getElementsByClassName("star");
// let output = document.getElementById("output");
let review_message = document.querySelector("#review_message")
let review_level = document.querySelector("#review_level")
let review_error = document.querySelector('#review_error')
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





document.addEventListener('DOMContentLoaded', function() {
    let myshow = document.querySelectorAll('.myshow')
    for( i =0 ;i<myshow.length;i++){
    const initialRating = 3; // Change this value as needed
    gfg_this(myshow[i],myshow[i].getAttribute('value'));
  }
});

function light_star_ajax() {
    let myshow = document.querySelectorAll('.myshow')
    for( i =0 ;i<myshow.length;i++){
    const initialRating = 3; // Change this value as needed
    gfg_this(myshow[i],myshow[i].getAttribute('value'));
  }
}


function get_ajax(bookID) {

    var xhr = new XMLHttpRequest();
    console.log('/ajax/'+bookID)
    xhr.open('GET', '/ajax/'+bookID, true);
    //xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var container = document.getElementById('reviews-container');
            container.innerHTML = '';
            data['reviews_list'].forEach(function(review) {
                var reviewDiv = document.createElement('div');
                reviewDiv.className = 'row';
                let r_date = new Date(review.updated_at)
                var options = {  year: 'numeric', month: 'long', day: 'numeric',hour:'numeric',minute:'numeric',second:'numeric'};
                reviewDiv.innerHTML = `
                    <div class="col-md-12 mt-5 reviews review_card">
                        <h4 class="user_review">${full_username(data['user_list'], review.user_id)}</h4>
                        <div class=" myshow" value="${review.review_level}">
                            ${generateStars(review.review_level)}
                        </div>
                        <div class="form-group">
                            <p class="user_review">${review.message}</p>
                            <p class="user_review">${r_date.toLocaleDateString("en-US", options)}</p>
                        </div>
                    </div>`;
                
                container.appendChild(reviewDiv);
            });
            light_star_ajax();          
        }
    };
    xhr.send();
} 

function post_data_from_ajax(data,userID){
    var container = document.getElementById('reviews-container');
        container.innerHTML = '';
        data['reviews_list'].forEach(function(review) {
        var reviewDiv = document.createElement('div');
        reviewDiv.className = 'row';
        let r_date = new Date(review.updated_at)
        var options = {  year: 'numeric', month: 'long', day: 'numeric',hour:'numeric',minute:'numeric',second:'numeric'};
        myhtml = `
                    <div class="col-md-12 mt-5 reviews review_card">
                        <h4 class="user_review">${full_username(data['user_list'], review.user_id)}</h4>
                        <div class=" myshow" value="${review.review_level}">
                            ${generateStars(review.review_level)}
                        </div>
                        <div class="form-group">
                            <p class="user_review">${review.message}</p>
                            <p class="user_review">${r_date.toLocaleDateString("en-US", options)}</p>
                        </div>`;
                if (review.user_id == userID){                    
                    myhtml +=`<button onclick='deleteReview(${review.id},${userID})'> delete</button> 
                    </div>`;
                }
                else{
                    myhtml +=`</div>`;
                }

                reviewDiv.innerHTML = myhtml;
                container.appendChild(reviewDiv);
        });
        light_star_ajax();
}
function full_username(data,id){
    for (var i in data) {
        if (data[i].id === id) {
            return username = data[i].first_name + ' ' + data[i].last_name; 
            //break; // Break the loop once the user is found
        }
    }
}



function generateStars(reviewLevel) {
    // Generate stars based on review level
    var stars = '';
    for (var i = 0; i < reviewLevel; i++) {
        stars += '<span class="show_star">★</span>';
    }
    return stars;
}


function show_review_error(data){
    review_error.innerHTML = ''+data['error']
    review_error.classList.add('error')
}

function deleteReview(reviewID,userID){
    dataToSend = {
        'reviewID': reviewID ,  
    }
      // Get CSRF token from cookie
      var csrftoken = getCookie('csrftoken');

      $.ajax({
          url: '/ajax/review/delete',
          type: 'POST',
          headers: {'X-CSRFToken': csrftoken}, // Include CSRF token in headers
          data: dataToSend,
          dataType: 'json',
          success: function(response) {
            if ('error' in response){  // Handle the response
                show_review_error(response)
                gfg(0);
                review_message.value = ''
            }
            else{
                post_data_from_ajax(response);
                show_review_error({'error':''});
                gfg(0);
                review_message.value = ''
                 
            }
          },
          error: function(xhr, status, error) {
              console.error('Error:', error);
          }
      });
  }

function postData(bookID,userID) {

    dataToSend = {
        'message': review_message.value,
        'review_level': review_level.value,
        'bookID':bookID, 
        'userID':userID,
    }
      // Get CSRF token from cookie
      var csrftoken = getCookie('csrftoken');

      $.ajax({
          url: '/ajax/review/create',
          type: 'POST',
          headers: {'X-CSRFToken': csrftoken}, // Include CSRF token in headers
          data: dataToSend,
          dataType: 'json',
          success: function(response) {
            console.log(response);  // Handle the response
            if ('error' in response){  // Handle the response
                show_review_error(response,userID)
                gfg(0);
                review_message.value = ''
            }
            else{
                post_data_from_ajax(response,userID);
                show_review_error({'error':''});
                gfg(0);
                review_message.value = ''
                 
            }
              
          },
          error: function(xhr, status, error) {
              console.error('Error:', error);
          }
      });
  }
  
  // Function to get CSRF cookie value
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }


















