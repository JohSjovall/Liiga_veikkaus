// import the http module
var http = require('http');

// handel sending reguests and returning responses
function handleRequestes(req, res) {
    //retur string
    res.end('Hello world')
}

//creat the server
var server = http.createServer(handleRequestes);

//start server and listen on port x
server.listen(8080, function() {
    console.log('listeening on port 8080');
});