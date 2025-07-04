// MongoDB initialization script
db = db.getSiblingDB('github_webhooks');

// Create the events collection
db.createCollection('events');

// Create indexes for better performance
db.events.createIndex({ "timestamp": -1 });
db.events.createIndex({ "event_type": 1 });
db.events.createIndex({ "repository": 1 });
db.events.createIndex({ "author": 1 });

// Insert sample data for testing
db.events.insertMany([
    {
        event_type: "PUSH",
        author: "john_doe",
        to_branch: "main",
        from_branch: null,
        timestamp: new Date(),
        repository: "sample-repo",
        commits: 3
    },
    {
        event_type: "PULL_REQUEST",
        author: "jane_smith",
        to_branch: "main",
        from_branch: "feature/new-feature",
        timestamp: new Date(Date.now() - 3600000), // 1 hour ago
        repository: "sample-repo",
        action: "opened"
    },
    {
        event_type: "MERGE",
        author: "bob_johnson",
        to_branch: "main",
        from_branch: "hotfix/critical-bug",
        timestamp: new Date(Date.now() - 7200000), // 2 hours ago
        repository: "sample-repo",
        action: "merged"
    }
]);

print("Database initialized with sample data");
