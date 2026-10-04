# Contributing Guidelines

## 🤝 How to Contribute

Thank you for your interest in contributing to the AI Mock Interview System! We welcome contributions from everyone.

## 📋 Before You Start

1. Read this entire guidelines document
2. Check existing issues and pull requests
3. Review the code of conduct
4. Understand the project architecture (see ARCHITECTURE.md)
5. Set up development environment (see DEVELOPMENT.md)

## 🐛 Reporting Bugs

### Create a Bug Report
1. Go to GitHub Issues
2. Click "New Issue"
3. Select "Bug Report" template
4. Provide:
   - Clear description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots/logs
   - System information

### Bug Report Template
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Screenshots
[If applicable]

## Environment
- OS: [Windows/Mac/Linux]
- Python: [version]
- Browser: [if applicable]
```

## 💡 Suggesting Features

### Create a Feature Request
1. Go to GitHub Issues
2. Click "New Issue"
3. Select "Feature Request" template
4. Provide:
   - Clear description
   - Motivation/use case
   - Proposed solution
   - Alternative solutions
   - Additional context

### Feature Request Template
```markdown
## Description
Clear description of the feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should this be implemented?

## Alternatives
Other possible approaches

## Additional Context
Any other relevant information
```

## 🔧 Development Workflow

### 1. Fork the Repository
```bash
git clone https://github.com/yourusername/ai-mock-interview-system.git
cd ai-mock-interview-system
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-name
```

### 3. Make Changes
- Follow code style (see below)
- Write clean, readable code
- Add comments for complex logic
- Update relevant documentation

### 4. Test Your Changes
```bash
# Run tests
cd backend
python manage.py test

# Manual testing
# Test in both frontend and backend
```

### 5. Commit with Clear Messages
```bash
git add .
git commit -m "feat: Add new feature description"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📝 Code Style Guidelines

### Python Code (Backend)
```python
# Use PEP 8 style
# Line length: max 100 characters
# Use type hints
# Add docstrings

def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    return True
```

### Python Code (Frontend)
```python
# Follow same PEP 8 style
# Use clear variable names
# Add comments for non-obvious code
# Keep functions small and focused
```

### Git Commit Messages
```
feat: Add new feature
fix: Fix specific bug
docs: Update documentation
style: Format code
refactor: Reorganize code
test: Add tests
chore: Maintenance tasks
```

## 📚 Documentation

When contributing code, also update:
- [ ] Docstrings in code
- [ ] README.md (if needed)
- [ ] ARCHITECTURE.md (if structure changes)
- [ ] FEATURES.md (if adding features)
- [ ] API docs (if changing API)

## ✅ Pull Request Checklist

Before submitting a PR:
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
- [ ] No debug code left behind
- [ ] Changes are focused and not overly broad

## 🧪 Testing

### Run Unit Tests
```bash
cd backend
python manage.py test

# Or specific test
python manage.py test api.tests.test_api
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Manual Testing Checklist
- [ ] Feature works as described
- [ ] No console errors
- [ ] UI/UX is smooth
- [ ] Responsive design works
- [ ] Performance is acceptable
- [ ] Error handling works

## 🚀 Areas Where Help Is Needed

### High Priority
- [ ] Writing tests for existing code
- [ ] Bug fixes
- [ ] Documentation improvements
- [ ] Performance optimization

### Medium Priority
- [ ] Feature enhancements
- [ ] UI/UX improvements
- [ ] Code refactoring
- [ ] Examples and tutorials

### Low Priority
- [ ] Code style improvements
- [ ] Comment improvements
- [ ] README enhancements

## 📖 Documentation Contributions

### Update README
```bash
# Edit README.md
# Test all links work
# Verify formatting is correct
# Submit PR with changes
```

### Add Code Examples
```python
"""
Example usage:
    >>> from api.models import Interview
    >>> interview = Interview.objects.create(...)
    >>> interview.start()
"""
```

### Write Tutorials
- Create clear step-by-step guides
- Include screenshots
- Test all instructions
- Place in /docs directory

## 🎓 Code Review Process

### What Reviewers Look For
1. **Correctness**: Does the code work?
2. **Style**: Does it follow guidelines?
3. **Performance**: Is it efficient?
4. **Security**: Are there vulnerabilities?
5. **Tests**: Is it well tested?
6. **Documentation**: Is it well documented?

### How to Respond to Reviews
- Don't take feedback personally
- Ask questions if unclear
- Make requested changes
- Update PR after changes
- Re-request review

## 🤖 Automated Checks

Our repository uses:
- **Linting**: Code style enforcement
- **Type Checking**: Python type hints
- **Testing**: Unit tests
- **Coverage**: Code coverage reports

All checks must pass before merge.

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

## 🙏 Code of Conduct

### Be Respectful
- Treat all contributors with respect
- Accept criticism gracefully
- Give credit where due

### Be Inclusive
- Welcome people of all backgrounds
- Use inclusive language
- Help others learn

### Be Professional
- Keep discussions focused
- Avoid personal attacks
- Report harassment

## 📞 Getting Help

### Questions?
- Check existing documentation
- Search GitHub issues
- Ask in discussions
- Email: contributing@mockinterview.ai

### Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Python PEP 8](https://pep8.org/)

## 🎉 Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes
- Project website

Thank you for contributing! 🚀

---

**Last Updated**: May 5, 2026
