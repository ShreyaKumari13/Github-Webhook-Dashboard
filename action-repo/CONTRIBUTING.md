# Contributing to Action Repo

Thank you for your interest in contributing to this project! This repository is designed to demonstrate GitHub webhook functionality.

## How to Contribute

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/action-repo.git
cd action-repo
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Add new features to the sample application
- Update documentation as needed
- Follow existing code style and conventions

### 4. Test Your Changes
```bash
# Install dependencies
npm install

# Run the application
npm start

# Test the endpoints
curl http://localhost:3000/health
```

### 5. Commit and Push
```bash
git add .
git commit -m "Add: your descriptive commit message"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to GitHub and create a pull request
- Provide a clear description of your changes
- Reference any related issues

## Code Style Guidelines

### JavaScript
- Use ES6+ features where appropriate
- Follow consistent indentation (2 spaces)
- Use meaningful variable and function names
- Add comments for complex logic

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

## Types of Contributions

### 🐛 Bug Fixes
- Fix issues in the sample application
- Improve error handling
- Update dependencies

### ✨ New Features
- Add new API endpoints
- Enhance existing functionality
- Improve user experience

### 📚 Documentation
- Update README files
- Add code comments
- Create usage examples

### 🧪 Testing
- Add unit tests
- Improve test coverage
- Create integration tests

## Development Setup

### Prerequisites
- Node.js 16+ and npm
- Git

### Installation
```bash
npm install
```

### Running the Application
```bash
npm start
```

### Running Tests
```bash
npm test
```

## Pull Request Process

1. **Update Documentation**: Ensure README and other docs reflect your changes
2. **Add Tests**: Include tests for new functionality
3. **Check Code Style**: Follow the established patterns
4. **Update Version**: Bump version numbers if applicable
5. **Get Reviews**: Wait for maintainer review and approval

## Webhook Testing

When making changes, test that webhooks are still triggered properly:

1. Make your changes
2. Commit and push to a feature branch
3. Create a pull request
4. Verify webhook events appear in the monitoring dashboard
5. Merge the pull request and verify merge events

## Issue Reporting

### Bug Reports
Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Node.js version, etc.)

### Feature Requests
Include:
- Clear description of the desired feature
- Use case and motivation
- Possible implementation approach

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

## Getting Help

- Check existing issues and documentation
- Ask questions in issue comments
- Reach out to maintainers for guidance

## Recognition

Contributors will be recognized in:
- README acknowledgments
- Release notes
- Project documentation

Thank you for contributing! 🎉
