# 🤝 Contributing to Action Repo

Thank you for your interest in contributing to this project! This repository is designed to demonstrate GitHub webhook functionality and serves as a testing ground for the webhook monitoring system.

![Contributors Welcome](https://img.shields.io/badge/Contributors-Welcome-brightgreen)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-blue)

## 🎯 Project Overview

This repository is part of a **two-repo webhook monitoring system**:
- **action-repo** (this repo) - Generates webhook events
- **webhook-repo** - Captures and displays webhook events

Your contributions help improve both the sample application and the webhook testing capabilities.

## 🚀 How to Contribute

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/action-repo.git
cd action-repo

# Add upstream remote for syncing
git remote add upstream https://github.com/ORIGINAL_OWNER/action-repo.git
```

### 2. Set Up Development Environment
```bash
# Install dependencies
npm install

# Verify setup
npm start
curl http://localhost:3000/health
```

### 3. Create a Feature Branch
```bash
# Always create a new branch for your changes
git checkout -b feature/your-feature-name

# Examples of good branch names:
# feature/add-logging-endpoint
# fix/user-validation-bug
# docs/update-api-documentation
```

### 4. Make Your Changes
- **Add new features** to the Express.js application
- **Fix bugs** in existing functionality
- **Update documentation** as needed
- **Follow existing code style** and conventions
- **Add comments** for complex logic

### 5. Test Your Changes Thoroughly
```bash
# Test the application locally
npm start

# Test all endpoints
curl http://localhost:3000/health
curl http://localhost:3000/api/users
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'

# Test webhook integration (if webhook-repo is running)
# Make commits and check if webhooks are triggered properly
```

### 6. Commit and Push
```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add: descriptive commit message"

# Push to your fork
git push origin feature/your-feature-name
```

### 7. Create Pull Request
- Go to GitHub and create a pull request
- **Provide a clear description** of your changes
- **Reference any related issues** using `#issue-number`
- **Include screenshots** if UI changes are involved
- **Test webhook functionality** if applicable

## 📋 Code Style Guidelines

### JavaScript Standards
- **ES6+ Features**: Use modern JavaScript features (arrow functions, destructuring, etc.)
- **Indentation**: Use 2 spaces consistently
- **Naming**: Use meaningful variable and function names
- **Comments**: Add JSDoc comments for functions
- **Error Handling**: Include proper error handling and validation
- **Async/Await**: Prefer async/await over promises when possible

### Code Examples
```javascript
// ✅ Good
const getUserById = async (userId) => {
    try {
        const user = users.find(u => u.id === parseInt(userId));
        if (!user) {
            throw new Error('User not found');
        }
        return user;
    } catch (error) {
        console.error('Error fetching user:', error);
        throw error;
    }
};

// ❌ Avoid
function getUser(id) {
    return users.find(function(u) { return u.id == id; });
}
```

### Commit Message Format
```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```bash
feat: add user authentication endpoint
fix: resolve email validation bug in user creation
docs: update API documentation with new endpoints
```

## 🎯 Types of Contributions

### 🐛 Bug Fixes
- **API Issues**: Fix problems with existing endpoints
- **Validation**: Improve input validation and error handling
- **Dependencies**: Update outdated or vulnerable packages
- **Performance**: Optimize slow operations

### ✨ New Features
- **API Endpoints**: Add new REST API endpoints
- **Middleware**: Create reusable middleware functions
- **Utilities**: Add helpful utility functions
- **Integration**: Improve webhook testing capabilities

### 📚 Documentation
- **README Updates**: Keep documentation current and accurate
- **Code Comments**: Add JSDoc comments for better code understanding
- **Examples**: Create usage examples and tutorials
- **API Docs**: Document new endpoints and parameters

### 🧪 Testing & Quality
- **Unit Tests**: Add tests for individual functions
- **Integration Tests**: Test API endpoints end-to-end
- **Webhook Testing**: Verify webhook integration works properly
- **Code Coverage**: Improve test coverage

## 🛠️ Development Setup

### Prerequisites
- **Node.js 16+** and npm
- **Git** for version control
- **GitHub account** for webhook testing
- **webhook-repo** running (for full integration testing)

### Environment Setup
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/action-repo.git
cd action-repo

# Install dependencies
npm install

# Verify installation
npm start
```

### Development Workflow
```bash
# Start development server
npm start

# In another terminal, test the API
curl http://localhost:3000/health
curl http://localhost:3000/api/users

# Make changes to code
# Test changes immediately
```

### Available Scripts
```bash
npm start       # Start the server
npm run dev     # Start development server (same as start)
npm test        # Run tests (placeholder - add real tests!)
```

## 🔄 Pull Request Process

### Before Submitting
1. **✅ Update Documentation**: Ensure README reflects your changes
2. **✅ Add Tests**: Include tests for new functionality (when test framework is added)
3. **✅ Check Code Style**: Follow established patterns and conventions
4. **✅ Test Locally**: Verify all endpoints work correctly
5. **✅ Test Webhooks**: Ensure webhook integration still works

### PR Checklist
- [ ] Code follows the style guidelines
- [ ] Self-review of the code completed
- [ ] Documentation updated (if applicable)
- [ ] No new warnings or errors introduced
- [ ] Webhook functionality tested (if applicable)
- [ ] Related issues referenced in PR description

### Review Process
1. **Automated Checks**: Ensure all checks pass
2. **Code Review**: Wait for maintainer review
3. **Address Feedback**: Make requested changes
4. **Final Approval**: Get approval from maintainers
5. **Merge**: Maintainer will merge the PR

## 🔗 Webhook Testing Protocol

**Important**: Always test webhook functionality when making changes!

### Testing Steps
1. **Setup webhook-repo**: Ensure the Flask monitoring app is running
2. **Configure GitHub webhook**: Point to your tunnel URL
3. **Make your changes** to action-repo
4. **Test the workflow**:
   ```bash
   # Create feature branch
   git checkout -b feature/test-webhooks

   # Make a small change
   echo "// Test comment" >> src/utils.js
   git add . && git commit -m "Test webhook integration"

   # Push (should trigger push webhook)
   git push origin feature/test-webhooks

   # Create PR on GitHub (should trigger PR webhook)
   # Merge PR (should trigger merge webhook)
   ```
5. **Verify events** appear in webhook-repo dashboard
6. **Check webhook deliveries** in GitHub Settings → Webhooks

### Webhook Event Types to Test
- **Push Events**: Any commit push to any branch
- **Pull Request Events**: Opening, updating, closing PRs
- **Merge Events**: Merging PRs into main/target branch
- **Issue Events**: Creating/updating issues (if configured)
- **Release Events**: Creating releases/tags (if configured)

## 🐛 Issue Reporting

### Bug Reports
When reporting bugs, please include:

**Required Information:**
- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs **actual behavior**
- **Environment details**:
  - OS (Windows/macOS/Linux)
  - Node.js version (`node --version`)
  - npm version (`npm --version`)
  - Browser (if applicable)

**Example Bug Report:**
```markdown
## Bug: User creation endpoint returns 500 error

### Description
The POST /api/users endpoint returns a 500 error when creating a user with a valid email.

### Steps to Reproduce
1. Start the server with `npm start`
2. Send POST request: `curl -X POST http://localhost:3000/api/users -H "Content-Type: application/json" -d '{"name":"Test","email":"test@example.com"}'`
3. Observe 500 error response

### Expected Behavior
Should return 201 status with user data

### Environment
- OS: Windows 11
- Node.js: v18.17.0
- npm: 9.6.7
```

### Feature Requests
When requesting features, please include:

- **Clear description** of the desired feature
- **Use case and motivation** - why is this needed?
- **Possible implementation approach** (if you have ideas)
- **Examples** of similar features in other projects

## 📜 Code of Conduct

### Our Standards
- **Be respectful and inclusive** to all contributors
- **Focus on constructive feedback** that helps improve the project
- **Help others learn and grow** through mentoring and guidance
- **Maintain a professional environment** in all interactions
- **Welcome newcomers** and help them get started

### Unacceptable Behavior
- Harassment, discrimination, or personal attacks
- Trolling, insulting comments, or inflammatory language
- Publishing private information without permission
- Spam or off-topic discussions
- Any other unprofessional conduct

### Enforcement
Instances of unacceptable behavior may result in:
1. Warning from maintainers
2. Temporary ban from the project
3. Permanent ban from the project

## 🆘 Getting Help

### Before Asking for Help
1. **Check existing documentation** (README, this file)
2. **Search existing issues** for similar problems
3. **Try the troubleshooting steps** in the README

### How to Get Help
- **GitHub Issues**: Create an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Comments**: Ask questions in existing issue/PR comments
- **Email**: Reach out to maintainers for sensitive issues

### Response Times
- **Issues**: We aim to respond within 48 hours
- **Pull Requests**: Reviews typically within 72 hours
- **Security Issues**: Immediate attention (email maintainers)

## 🏆 Recognition

Contributors will be recognized in:
- **README acknowledgments** section
- **Release notes** for significant contributions
- **Project documentation** and changelog
- **GitHub contributors** page
- **Special mentions** in project updates

### Contribution Levels
- **🌟 First-time contributors**: Welcome badge and special mention
- **🚀 Regular contributors**: Listed in README contributors section
- **💎 Core contributors**: Invited to join the maintainer team

## 📞 Contact

### Maintainers
- **Primary Maintainer**: [GitHub Profile]
- **Code Review**: [GitHub Profile]
- **Documentation**: [GitHub Profile]

### Communication Channels
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions
- **Email**: For security issues or private matters

---

## 🎉 Thank You!

Thank you for taking the time to contribute to this project! Every contribution, no matter how small, helps make this project better for everyone.

**Happy coding! 🚀**
