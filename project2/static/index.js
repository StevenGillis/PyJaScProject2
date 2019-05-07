 document.addEventListener('DOMContentLoaded', () => {

     // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    console.log('socket var is set');

    //When connected make sure you can send messages
    socket.on('connect', () => {
        console.log('socketIO is connected');
        document.querySelector('#chatsubmit').onsubmit = () => {
        message = document.querySelector('#chattext').value;
        usernameSend = "placeholder for username"
        socket.emit('submit message', {"message": message, "usernameSend": usernameSend});
        document.querySelector('#chattext').value = '';
        return false;
        };
    });

    //When a chat message has been emited by other user I wan't to register this
    socket.on('announce message', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.usernameSend}: ${data.message}`;
        document.querySelector('#chathistory').append(li);
        return false;
    });

    //Make sure new channel can be added
    document.querySelector('#addchannel').onsubmit = () => {

          newchannelname = document.querySelector('#channelname').value;
          // Create new item for list
            const li = document.createElement('li');
           // Create <a> for link
            var a = document.createElement('a');
            //document.body.appendChild(li);
            var linkname = "/changechannel/" + newchannelname ;
            a.setAttribute("href",linkname);
            //li.innerHTML = newchannelname;
            a.innerHTML = newchannelname;
        // Add new item to the screen list of channels
        li.appendChild(a);
        document.querySelector('#channellist').appendChild(li);
        // Clear input field
        document.querySelector('#channelname').value = '';
        // Stop form from submitting
        return false;
    };
 });
