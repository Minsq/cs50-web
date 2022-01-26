document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Process the sent forms
  document.querySelector("#compose-form").onsubmit = function(){
    const input_recipient = document.querySelector("#compose-recipients").value;
    const input_subject = document.querySelector("#compose-subject").value;
    const input_body = document.querySelector("#compose-body").value;

    fetch('/emails',{
      method: 'POST',
      body: JSON.stringify({
        recipients: input_recipient,
        subject: input_subject,
        body: input_body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });
  };

});
// #########################################################################################
// all the necessary functions below
function close_email() {
  var email = document.getElementById("email-content");
  if (email !== null) {
    email.remove()
    // email.style.display = 'none';
  }
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector("#compose-header").innerHTML = "New email";
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  close_email()

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function reply_email(data) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  close_email()

  // Fill out the form
  document.querySelector("#compose-header").innerHTML = "Reply email";
  document.querySelector('#compose-recipients').value = `${data.sender}`;
  document.querySelector('#compose-subject').value = `Re: ${data.subject}`;
  document.querySelector('#compose-body').value = `\n\n On ${data.timestamp}: ${data.sender} wrote: \n ${data.body}`;
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  close_email()

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the relevant emails
  // fetch('/emails/inbox')
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    if (emails.length !== 0 ){
      // create table to contain the messages
      let table = document.createElement('table');
      document.querySelector('#emails-view').appendChild(table)
      table.style.width = '100%';

      emails.forEach(function(email) {
        const row = document.createElement('tr');
        row.setAttribute("style", 'border-bottom: solid 0.5px grey; ')
        // row.className = 'email-item';
        // row.setAttribute("email-id", `${email.id}`)

        const sender = document.createElement('td');
        if (mailbox !== 'sent'){
          sender.innerHTML = `${email.sender}`;
        } else {
          sender.innerHTML = `${email.recipients}`;
        }

        // sender.className = "sender-item";
        sender.setAttribute("style", 'padding: 10px; font-weight: bold; width: 25%;')
        sender.className = 'email-item';
        sender.setAttribute("email-id", `${email.id}`)

        const subject = document.createElement('td');
        subject.innerHTML = `${email.subject}`;
        // subject.className = "subject-item";
        subject.setAttribute("style", 'padding: 10px; width:40%')
        subject.className = 'email-item';
        subject.setAttribute("email-id", `${email.id}`)

        const timestamp = document.createElement('td');
        timestamp.innerHTML = `${email.timestamp}`;
        // timestamp.className = "timestamp-item";
        timestamp.setAttribute("style", 'padding: 10px; text-align: right; font-weight: lighter;')

        row.appendChild(sender);
        row.appendChild(subject);
        row.appendChild(timestamp);

        if (mailbox === 'inbox'){
          const archive_button = document.createElement('td');
          archive_button.innerHTML = `<button class="btn btn-sm btn-warning float-right archive" email-id=${email.id}>Archive</button>`;
          row.appendChild(archive_button);

        } else if (mailbox ==='archive'){
          const archive_button = document.createElement('td');
          archive_button.innerHTML = `<button class="btn btn-sm btn-warning float-right archive" email-id=${email.id}>Move to inbox</button>`;
          row.appendChild(archive_button);
          // archive_button.setAttribute("email-id", `${email.id}`)
        }
        // check if row is read or unread, toggle background white and grey respectively
        if (email.read === true){
          row.style.backgroundColor = "#F8F8F8";
        } else {
          row.style.backgroundColor = 'white';
        }

        table.appendChild(row);

      })

      // Add event listener button to open contents of emails
      document.querySelectorAll('.email-item').forEach(row => {
        row.onclick = function() {
         const email_id = row.getAttribute("email-id");
         // do a GET request
         fetch(`/emails/${email_id}`, {
           method: 'GET'
         })
         .then(response => response.json())
         .then(data => {
           // create contents of the email
           const info = document.createElement("div");
           info.id = "email-content"
           info.innerHTML = `<b>From:</b> ${data.sender}  <br>
                             <b>To:</b> ${data.recipients} <br>
                             <b>Subject:</b> ${data.subject} <br>
                             <b>Timetamp:</b> ${data.timestamp} <br>
                             <button class="btn btn-sm btn-outline-primary" id="replyButton">Reply</button> <br> <hr>
                             ${data.body}`
           document.querySelector(".container").appendChild(info);
           document.querySelector('#emails-view').style.display = 'none';

           // add listener on reply button
           document.addEventListener('click', function(e){
            if(e.target && e.target.id== 'replyButton') {
              console.log(data);
              document.querySelector("#replyButton").click = reply_email(data);
               }
            });


         })
         // do a put request
         fetch(`/emails/${email_id}`, {
           method: "PUT",
           body: JSON.stringify({
             read: true
           })
         })
       }
     })

     // Add event listener button to archive emails
     if (mailbox === "inbox"){
       document.querySelectorAll('.archive').forEach(archive_b => {
         archive_b.onclick = function() {
          const email_id = archive_b.getAttribute("email-id");
          // do a PUT request to allow archive
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          .then(() => {
            load_mailbox('inbox');
          })


        }

      })
    } else if (mailbox==='archive'){
      document.querySelectorAll('.archive').forEach(archive_b => {
        archive_b.onclick = function() {
         const email_id = archive_b.getAttribute("email-id");
         // do a PUT request to allow archive
         fetch(`/emails/${email_id}`, {
           method: 'PUT',
           body: JSON.stringify({
             archived: false
           })
         })
         .then(() => {
           load_mailbox('inbox');
         })

       }

     })
    }


    }
  })
}
