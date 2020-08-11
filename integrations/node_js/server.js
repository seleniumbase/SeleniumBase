const http = require('http');
const express = require('express');
const path = require('path');
const app = express();
const exec = require('child_process').exec;
var server_info = '\nServer running at http://127.0.0.1:3000/  (CTRL-C to stop)';

function run_command(command) {
    console.log("\n" + command);
    exec(command, (err, stdout, stderr) => console.log(stdout, server_info));
}

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/run_my_first_test', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_command("pytest my_first_test.py");
});

app.get('/run_test_demo_site', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_command("pytest test_demo_site.py");
});

app.get('/run_my_first_test_with_demo_mode', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_command("pytest my_first_test.py --demo_mode");
});

app.get('/run_test_demo_site_with_demo_mode', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_command("pytest test_demo_site.py --demo_mode");
});

app.listen(3000, "127.0.0.1", function() {
    console.log(server_info);
});
