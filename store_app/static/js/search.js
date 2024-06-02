








thead = document.querySelector("#search_table_head")
tbody = document.querySelector("#search_table_body")
typeID = document.querySelector('#typeID')

function get_search(ele){
    dataToSend = {
        'data':ele.value,   
    }
 
      // Get CSRF token from cookie
      var csrftoken = getCookie('csrftoken');

      $.ajax({
          url: '/search/'+typeID.value,
          type: 'POST',
          headers: {'X-CSRFToken': csrftoken}, // Include CSRF token in headers
          data: dataToSend,
          dataType: 'json',
          success: function(response) {
            show_info_in_table(response,typeID.value)
            // console.log(response)
          },
          error: function(xhr, status, error) {
              console.error('Error:', error);
          }
      });
}

function show_info_in_table(data,info_type){
    if (info_type == 1 ){
        thead.innerHTML = `<tr>
        <th class="text-center" scope="col">Title</th>
        <th class="text-center" scope="col">Author Name</th>
        <th class="text-center" scope="col">Price</th>
        <th class="text-center" scope="col">Num. of Pages</th>
        <th class="text-center" scope="col">Action</th>
      </tr>`
      tbody.innerHTML = `` 
    //   console.log(data['books_list'].length)
        data['books_list'].forEach(element => {
            var new_row = document.createElement('tr');
            new_row.innerHTML =`
            <td class="text-center">${element.title}</td>
            <td class="text-center">${data['authors_list'][element.id]}</td>
            <td class="text-center">${element.price}</td>
            <td class="text-center">${element.number_of_pages}</td>
            <td class="text-center"><a href='/book/${element.id}'>view</a></td>` ; 
            //console.log(new_row)
             
         tbody.appendChild(new_row)  
        });

    }
    else if (info_type == 2){
        thead.innerHTML = `<tr>
        <th class="text-center" scope="col">ID</th>
        <th class="text-center" scope="col">First Name</th>
        <th class="text-center" scope="col">Last Name</th>
        <th class="text-center" scope="col">Books</th>
      </tr>`
      tbody.innerHTML = `` ;
      data['authors_list'].forEach(element => {
        console.log(element)
        var new_row = document.createElement('tr');
        new_row.innerHTML =`
        <td class="text-center">${element.id}</td>
        <td class="text-center">${element.first_name}</td>
        <td class="text-center">${element.last_name}</td>
        <td class="text-center"> <a href='#'>view</a></td>
       ` ; 
        //console.log(new_row)
         
        tbody.appendChild(new_row)  
      });
    }
}







