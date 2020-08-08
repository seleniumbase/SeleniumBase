var http = require('http');
var express = require('express');
var path = require('path');
var app = express();
var exec = require('child_process').exec;

function run_my_first_test() {
    exec("pytest my_first_test.py");
}

function run_test_demo_site() {
    exec("pytest test_demo_site.py");
}

function run_my_first_test_with_demo_mode() {
    exec("pytest my_first_test.py --demo_mode");
}

function run_test_demo_site_with_demo_mode() {
    exec("pytest test_demo_site.py --demo_mode");
}

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
})

app.get('/run_my_first_test', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_my_first_test()
})

app.get('/run_test_demo_site', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_test_demo_site()
})

app.get('/run_my_first_test_with_demo_mode', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_my_first_test_with_demo_mode()
})

app.get('/run_test_demo_site_with_demo_mode', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_test_demo_site_with_demo_mode()
})

app.listen(3000, "127.0.0.1", function() {
    console.log('Server running at http://127.0.0.1:3000/  (CTRL-C to stop)');
});
