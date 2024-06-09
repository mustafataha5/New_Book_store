







thead = document.querySelector("#search_table_head")
tbody = document.querySelector("#search_table_body")
typeID = document.querySelector('#typeID')

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

function get_search(ele) {
  const dataToSend = {
      'data': ele.value,
      'typeID': typeID.value,
  };

  $.ajax({
      url: '/search/book',
      type: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      data: dataToSend,
      dataType: 'json',
      success: function(response) {
          show_info_in_table(response, typeID.value);
      },
      error: function(xhr, status, error) {
          console.error('Error:', error);
      }
  });
}

function show_info_in_table(data, info_type) {
  if (info_type == 1) {
      thead.innerHTML = `<tr>
          <th class="text-center" scope="col">Title</th>
          <th class="text-center" scope="col">Author Name</th>
          <th class="text-center" scope="col">Price</th>
          <th class="text-center" scope="col">Num. of Pages</th>
          <th class="text-center" scope="col">Action</th>
      </tr>`;
      tbody.innerHTML = ``;
      data['books_list'].forEach(element => {
          var new_row = document.createElement('tr');
          new_row.innerHTML = `
              <td class="text-center">${element.title}</td>
              <td class="text-center">${data['authors_list'][element.id]}</td>
              <td class="text-center">${element.price}</td>
              <td class="text-center">${element.number_of_pages}</td>
              <td class="text-center"><a href='/book/${element.id}'>view</a></td>`;
          tbody.appendChild(new_row);
      });
  } else if (info_type == 2) {
      thead.innerHTML = `<tr>
          <th class="text-center" scope="col">ID</th>
          <th class="text-center" scope="col">First Name</th>
          <th class="text-center" scope="col">Last Name</th>
          <th class="text-center" scope="col">Books</th>
      </tr>`;
      tbody.innerHTML = ``;
      data['authors_list'].forEach(element => {
          var new_row = document.createElement('tr');
          new_row.innerHTML = `
              <td class="text-center">${element.id}</td>
              <td class="text-center">${element.first_name}</td>
              <td class="text-center">${element.last_name}</td>
              <td class="text-center"><a href='#'>view</a></td>`;
          tbody.appendChild(new_row);
      });
  }
}

