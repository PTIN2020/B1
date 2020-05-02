const express = require('express');

var server = require('http').Server(express);
var io = require('socket.io')(server);
var cotxes = {};

server.listen(3003, function() {
    console.log('WebSocket corriendo en http://localhost:3003');
});


io.on('connection', function(socket) {
    console.log('Un cliente se ha conectado');

    // missatge inicial on el cotche et comunica el seu id
    socket.on('id', (id) => {
        console.log('id del cotche: ' + id);

        //	Es comproba que el cotche existeix en la base de dades. Si no existei es tanca la connexió
        //	amb el socket i si existeix es guarda en el diccionari amb el seu id
        if (id !== '123654'){
            socket.disconnect()
        } else {
            cotxes[socket] = id;
        }
    });

    // missage que reps del posicionament individual de cada cotche
    socket.on('position', (lat,lon) => {
        console.log('position del cotxe '+cotxes[socket]+': ' + lat + " - " + lon);
        //	aqui s'actialitza la posició
    });

    // missage que reps del status individual de cada cotche
    socket.on('status', (msg) => {
        console.log('status del cotxe '+cotxes[socket]+': ' + msg);
        if (msg === 'libre' || msg === 'ocupado' || msg === 'cargando' || msg === 'reparando') {
        //    Aqui s'actualitza el status
        }else {
            console.log('Bad status');
            socket.emit('bad_status', "El status no es correcte");
        }
    });

    // quan un cotxe es desconnecta s'elimina de la llista
    socket.on('disconnect', (reason) => {
        console.log('Cotxe '+cotxes[socket]+' desconnectat');
        delete cotxes[socket]
    });

    socket.emit('message', "missatge de benvinguda"); // ejemplo de mensaje normal, no sirve para nada
    socket.emit('notification', "rebut"); // ejemplo de notidicación a un solo coche
});

io.emit('notification', "Id_aturada_inifial:Id_aturada_final"); //broadcast de notificación


function findSocketFromId(id) {
    for(var client in cotxes) {
        if (cotxes[client] === id ){
            return client
        }
    }
    return null
}

