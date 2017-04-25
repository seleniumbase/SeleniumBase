var http = require('http');
var express = require('express');
var path = require('path');
var app = express();
var exec = require('child_process').exec;

function run_my_first_test_in_firefox() {
    exec("nosetests my_first_test.py --with-selenium --browser=firefox");
}

function run_my_first_test_in_chrome() {
    exec("nosetests my_first_test.py --with-selenium --browser=chrome");
}

function run_my_first_test_in_firefox_with_demo_mode() {
    exec("nosetests my_first_test.py --with-selenium --browser=firefox --demo_mode");
}

function run_my_first_test_in_chrome_with_demo_mode() {
    exec("nosetests my_first_test.py --with-selenium --browser=chrome --demo_mode");
}

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
})

app.get('/run_my_first_test_in_firefox', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_my_first_test_in_firefox()
})

app.get('/run_my_first_test_in_chrome', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_my_first_test_in_chrome()
})

app.get('/run_my_first_test_in_firefox_with_demo_mode', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_my_first_test_in_firefox_with_demo_mode()
})

app.get('/run_my_first_test_in_chrome_with_demo_mode', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
    res.redirect('/');
    run_my_first_test_in_chrome_with_demo_mode()
})

app.listen(3000, "127.0.0.1", function() {
    console.log('Server running at http://127.0.0.1:3000/');
});

