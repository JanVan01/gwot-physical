function submit_form(url, method){
  console.log('blub');
  form = $('form');
  formdata = JSON.stringify(form.serializeArray()
      .reduce(function(a, x) { a[x.name] = x.value; return a; }, {}));
  console.log(formdata);
  $.ajax({
      cache: false,
      type: method,
      contentType: 'application/json',
      dataType:'json',
      url: url,
      data : formdata,
      success: function() {
          form.find("input[type=text], input[type=password]").val("");
      },
      error: function() {
          form.find("input[type=text], input[type=password]").val("");
      }
  });

}
