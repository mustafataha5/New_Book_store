


let my_cart_total = document.querySelector('#my_cart_total'); 
let total_order = document.querySelector('#total_order')





function add_book_to_cart(ele,bookID){

    //print('>>>>>>>>>>>...',userID.length)
    // if (userID == 'None'){
    //     window.location.href = '/login';
    //     return 
    // }
    dataToSend = {
      
        'bookID':bookID,   
    }
      // Get CSRF token from cookie
      var csrftoken = getCookie('csrftoken');

      $.ajax({
          url: '/cart/'+bookID+'/add/5',
          type: 'POST',
          headers: {'X-CSRFToken': csrftoken}, // Include CSRF token in headers
          //data: dataToSend,
          dataType: 'json',
          success: function(response) {
            
            update_cart(ele,response,bookID)
          },
          error: function(xhr, status, error) {
              console.error('Error:', error);
          }
      });
  }


function delete_book_from_cart(ele,bookID){
    dataToSend = {
      
        'bookID':bookID,   
    }
      // Get CSRF token from cookie
      var csrftoken = getCookie('csrftoken');

      $.ajax({
          url: '/cart/'+bookID+'/delete/5',
          type: 'POST',
          headers: {'X-CSRFToken': csrftoken}, // Include CSRF token in headers
          //data: dataToSend,
          dataType: 'json',
          success: function(response) {
            update_cart(ele,response,bookID)
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


function update_cart(ele,data,bookID){
    my_cart_total.innerHTML = data.total_item ; 
    total_order.innerHTML = `Cart: (${data.total} $)`
    console.log(ele.getAttribute('value'))
    if (ele.getAttribute('value') == 0 ){ 
        ele.innerHTML = 'Delete From Cart' ;
        ele.setAttribute('onclick',`delete_book_from_cart(this,${bookID})`)
        ele.value = 1 ; 
    }
    else{
        ele.innerHTML = 'Add To Cart' ;
        ele.setAttribute('onclick',`add_book_to_cart(this,${bookID})`)
        ele.value = 0 ;
    }  
}





