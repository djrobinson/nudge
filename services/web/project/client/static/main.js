$( document ).ready(() => {
  console.log('Sanity Check!');
});

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


function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.data.task_id}</td>
        <td>${res.data.task_status}</td>
        <td>${JSON.stringify(res.data.task_result)}</td>
      </tr>`
    $('#tasks').prepend(html)
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished' || taskStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  })
}

