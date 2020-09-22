/**
Application : ants-demo
Description : 人流クラウド化の導通試験用プログラム
Version : 1.0.0
Dependencies : node.js + Express + Socket.io
Auther : Magosa
**/

const express = require('express');
const app = express();
const bodyparser = require('body-parser');
const http = require('http').Server(app);
const fs = require('fs');
const io = require('socket.io')(http);
const PORT = process.env.PORT || 8080;


app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS');
  next();
});

app.use(bodyparser.urlencoded({
  extended: true
}));

app.use(bodyparser.json());

app.options('*', (req, res) => {
  res.sendStatus(200);
});

io.on('connection', socket => {
  socket.on('current_data', msg => {
    let data = JSON.parse(msg);
    console.log(msg);
    io.emit('routing_data', data);
  });
});

http.listen(PORT, () => {
  console.log("server listening. Port:" + PORT);
});
