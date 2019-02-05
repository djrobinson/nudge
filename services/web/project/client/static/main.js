// custom javascript

$( document ).ready(() => {
  console.log('Sanity Check!');
});

$('.btn').on('click', function() {
  console.log($(this).text());
  $.ajax({
    url: '/tasks',
    data: { words: $(this).text() },
    method: 'POST'
  })
  .done((res) => {
    console.log("What it is: ", res)
  })
  .fail((err) => {
    console.log(err)
  })
})

$('#start-sockets').on('click', () => {
  $.ajax({
    url: '/websockets/start',
    method: 'GET'
  })
  .done((res) => {
    console.log("What is reponse from start sockets", res)
  })
  .fail((err) => {
    console.log(err)
  })
})

$('#stop-sockets').on('click', () => {
  $.ajax({
    url: '/websockets/stop',
    method: 'GET'
  })
  .done((res) => {
    console.log("What is reponse from stop sockets", res)
  })
  .fail((err) => {
    console.log(err)
  })
})


