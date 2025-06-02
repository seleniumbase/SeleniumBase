const express = require('express');
const cookieParser = require('cookie-parser');
const { doubleCsrf } = require('csrf');

const app = express();

// Configure CSRF protection
const {
  invalidCsrfTokenError,
  generateToken,
  validateRequest,
} = doubleCsrf({
  getSecret: () => process.env.CSRF_SECRET || 'your-csrf-secret-key-change-in-production',
  cookieName: '__Host-psifi.x-csrf-token',
  cookieOptions: {
    httpOnly: true,
    sameSite: 'strict',
    secure: process.env.NODE_ENV === 'production',
    maxAge: 3600000, // 1 hour
  },
  size: 64,
  ignoredMethods: ['GET', 'HEAD', 'OPTIONS'],
});

// Middleware setup
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// CSRF token endpoint
app.get('/csrf-token', (req, res) => {
  const token = generateToken(req, res);
  res.json({ csrfToken: token });
});

// CSRF validation middleware for protected routes
const csrfProtection = (req, res, next) => {
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next();
  }
  
  try {
    validateRequest(req);
    next();
  } catch (error) {
    if (error === invalidCsrfTokenError) {
      return res.status(403).json({ error: 'Invalid CSRF token' });
    }
    next(error);
  }
};

// Apply CSRF protection to all routes
app.use(csrfProtection);

// Your existing routes go here
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Error handling middleware
app.use((error, req, res, next) => {
  if (error === invalidCsrfTokenError) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  res.status(500).json({ error: 'Internal server error' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

module.exports = app;
