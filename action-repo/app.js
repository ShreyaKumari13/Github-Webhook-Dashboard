const express = require('express');
const { formatDate } = require('./src/utils');
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Request logging middleware
app.use((req, res, next) => {
    const timestamp = formatDate(new Date());
    console.log(`[${timestamp}] ${req.method} ${req.path} - ${req.ip}`);
    next();
});

// Sample data
const users = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com' }
];

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Welcome to Action Repo API',
        description: 'Sample Express.js application for GitHub webhook testing',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        endpoints: {
            users: '/api/users',
            health: '/health',
            version: '/version'
        },
        documentation: 'See README.md for setup and usage instructions'
    });
});

app.get('/version', (req, res) => {
    res.json({
        name: 'action-repo',
        version: '1.0.0',
        description: 'Sample Express.js application for GitHub webhook testing',
        node_version: process.version,
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

app.get('/api/users', (req, res) => {
    res.json({
        success: true,
        data: users,
        count: users.length
    });
});

app.get('/api/users/:id', (req, res) => {
    const userId = parseInt(req.params.id);
    const user = users.find(u => u.id === userId);
    
    if (!user) {
        return res.status(404).json({
            success: false,
            message: 'User not found'
        });
    }
    
    res.json({
        success: true,
        data: user
    });
});

app.post('/api/users', (req, res) => {
    const { name, email } = req.body;
    
    if (!name || !email) {
        return res.status(400).json({
            success: false,
            message: 'Name and email are required'
        });
    }
    
    const newUser = {
        id: users.length + 1,
        name,
        email
    };
    
    users.push(newUser);
    
    res.status(201).json({
        success: true,
        data: newUser,
        message: 'User created successfully'
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        success: false,
        message: 'Something went wrong!'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: 'Endpoint not found'
    });
});

app.listen(port, () => {
    console.log(`Action Repo API running on port ${port}`);
    console.log(`Visit http://localhost:${port} to get started`);
});

module.exports = app;
