var xmpp = require('simple-xmpp');

var jid = 'minerei@jix.im';
var senha = 'lucass2156';
var server = 'jix.im';
var port = 5222;

xmpp.on('online', function(data) {
    console.log('Connected with JID: ' + data.jid.user);
    xmpp.send('dallamico@jix.im', 'hello! time is '+new Date(), false);
});

xmpp.on('error', function(err) {
    console.error("error:", JSON.stringify(err));
});

xmpp.connect({
    jid: jid,
    password: senha,
    host: server,
    port: port
});

// Main ?
xmpp.connect()

// Minhas implementações
function envia_ping()
{
    xmpp.connect()
    xmpp.on()
}