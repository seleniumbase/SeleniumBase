const express = require('express');
const cookieParser = require('cookie-parser');
const csrf = require('csrf');
const app = express();

// Initialize CSRF protection
const tokens = new csrf();

// Middleware setup
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// CSRF middleware
app.use((req, res, next) => {
  // Generate secret if not exists
  if (!req.cookies._csrf_secret) {
    const secret = tokens.secretSync();
    res.cookie('_csrf_secret', secret, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict'
    });
    req.csrfSecret = secret;
  } else {
    req.csrfSecret = req.cookies._csrf_secret;
  }

  // For GET requests, provide token
  if (req.method === 'GET') {
    req.csrfToken = tokens.create(req.csrfSecret);
    res.locals.csrfToken = req.csrfToken;
  }

  // For state-changing requests, validate token
  if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(req.method)) {
    const token = req.body._csrf || req.headers['x-csrf-token'] || req.headers['csrf-token'];
    
    if (!token || !tokens.verify(req.csrfSecret, token)) {
      return res.status(403).json({ error: 'Invalid CSRF token' });
    }
  }

  next();
});

// Example route that provides CSRF token
app.get('/csrf-token', (req, res) => {
  res.json({ csrfToken: req.csrfToken });
});

// Your existing routes go here
app.get('/', (req, res) => {
  res.json({ message: 'Server is running with CSRF protection' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

module.exports = app;
