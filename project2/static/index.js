 document.addEventListener('DOMContentLoaded', () => {

     // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    console.log('socket var is set');

    //When connected make sure you can send messages
    socket.on('connect', () => {
        console.log('socketIO is connected');
        document.querySelector('#chatsubmit').onsubmit = () => {
        console.log('printed');
        message = document.querySelector('#chattext').value;
        console.log(message);
        usernameSend = "gebruikersnaam";
        socket.emit('submit message', {"message": message, "usernameSend": usernameSend});
        return false;
        };
    });

    //var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    //When a chat message has been emited by other user I wan't to register this
    socket.on('announce message', data => {
        console.log('gehoord');
        const li = document.createElement('li');
        li.innerHTML = `${data.usernameSend}: ${data.message}`;
        document.querySelector('#chathistory').append(li);
        return false;
    });
    /*
    //borrowed from class
    document.querySelector('#chat').onsubmit = () => {

        //Button should emit the text message
        const message = document.querySelector('#chattext').value;
            socket.emit('chatmessage', {"message": message})

            // Create new item for list
            const li = document.createElement('li');
            li.innerHTML = document.querySelector('#chattext').value;

            // Add new item to task list
            document.querySelector('#chathistory').append(li);
            // Clear input field
            document.querySelector('#chattext').value = '';

            // Stop form from submitting
            return false;
        };

    */

    document.querySelector('#addchannel').onsubmit = () => {

        // Create new item for list
        const li = document.createElement('li');
        li.innerHTML = document.querySelector('#channelname').value;

        // Add new item to task list
        document.querySelector('#channellist').append(li);

        // Clear input field
        document.querySelector('#channelname').value = '';

        // Stop form from submitting
        return false;
    };

 });
