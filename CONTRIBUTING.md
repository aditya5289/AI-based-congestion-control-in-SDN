# Contributing to AI-Based Congestion Control in SDN

Welcome! We appreciate your interest in contributing to this project. This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)
- [Getting Help](#getting-help)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We pledge to make participation in this project a harassment-free experience for everyone.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing opinions
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or intimidation of any kind
- Discrimination based on personal characteristics
- Trolling, insulting/derogatory comments
- Public or private attacks
- Publishing others' private information without consent

---

## 🚀 Getting Started

### Prerequisites

- **Python** ≥ 3.8
- **Git**
- **GitHub account**
- **Mininet** (for network simulation testing)
- **Node.js** ≥ 16.x (for frontend development)

### Fork & Clone

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-based-congestion-control-in-SDN.git
   cd AI-based-congestion-control-in-SDN
   ```

3. **Add upstream** remote:
   ```bash
   git remote add upstream https://github.com/aditya5289/AI-based-congestion-control-in-SDN.git
   ```

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Pre-commit hooks (optional)
pre-commit install
```

---

## 🔄 Development Workflow

### Branch Naming Convention

Use descriptive branch names following this format:

```
{type}/{description}
```

**Types:**
- `feature/` - New feature
- `bugfix/` - Bug fix
- `hotfix/` - Urgent production fix
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions
- `ci/` - CI/CD changes

**Examples:**
```bash
git checkout -b feature/lstm-attention-layer
git checkout -b bugfix/model-loading-error
git checkout -b docs/api-documentation
```

### Before Making Changes

```bash
# Update local main branch
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

```bash
# Make your changes
# Commit regularly with descriptive messages

# Stage changes
git add .

# Commit with proper format (see Commit Message Format)
git commit -m "feat(lstm): add attention mechanism"

# Push to your fork
git push origin feature/your-feature-name
```

---

## 📝 Coding Standards

### Python Code Style

Follow **PEP 8** guidelines:

```python
# Good - Clear naming and formatting
def predict_congestion(link_id: str, features: List[float]) -> Dict[str, float]:
    """
    Predict congestion probability for a network link.
    
    Args:
        link_id: Unique link identifier
        features: Input feature vector [bandwidth, rtt, drops, queue, inter_arrival]
    
    Returns:
        Dictionary with 'probability' and 'risk_level' keys
    """
    if not isinstance(features, list):
        raise ValueError("Features must be a list")
    
    prediction = self.model.predict([features])
    return {
        "probability": float(prediction[0]),
        "risk_level": self._classify_risk(prediction[0])
    }

# Bad - Poor naming and no documentation
def pred(l, f):
    p = model.predict([f])
    return {"p": p[0]}
```

### Type Hints

Always use type hints:

```python
# Good
from typing import List, Dict, Optional, Tuple

def process_data(
    data: List[float],
    threshold: float = 0.7
) -> Tuple[bool, Dict[str, float]]:
    """Process data and return results."""
    pass

# Bad
def process_data(data, threshold=0.7):
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_metrics(predictions: List[float], actuals: List[float]) -> Dict:
    """
    Calculate performance metrics for predictions.
    
    Args:
        predictions: List of predicted values
        actuals: List of actual values
    
    Returns:
        Dictionary with keys:
            - accuracy (float): Overall accuracy
            - precision (float): Precision score
            - recall (float): Recall score
            - f1_score (float): F1 score
    
    Raises:
        ValueError: If lists have different lengths
    """
    if len(predictions) != len(actuals):
        raise ValueError("Lists must have equal length")
    
    # Implementation
    return metrics
```

### Code Formatting

```bash
# Format code with Black
black backend/

# Sort imports
isort backend/

# Check style compliance
flake8 backend/

# Lint code
pylint backend/

# Type checking
mypy backend/
```

---

## 🧪 Testing Requirements

### Test Structure

```
tests/
├── test_lstm_model.py          # Unit tests for LSTM
├── test_dqn_agent.py           # Unit tests for DQN
├── test_api_endpoints.py       # Integration tests
├── test_data_processing.py     # Data pipeline tests
└── fixtures/
    ├── sample_data.csv
    └── mock_model.pkl
```

### Writing Tests

```python
import pytest
from backend.lstm_model import LSTMPredictor

class TestLSTMPredictor:
    """Tests for LSTM congestion predictor."""
    
    @pytest.fixture
    def predictor(self):
        """Create predictor instance for testing."""
        return LSTMPredictor(model_path="tests/fixtures/mock_model.pkl")
    
    def test_predict_valid_input(self, predictor):
        """Test prediction with valid input."""
        features = [0.75, 12.3, 0.02, 45.6, 0.8]
        result = predictor.predict("s1-s3", features)
        
        assert isinstance(result, dict)
        assert "probability" in result
        assert 0 <= result["probability"] <= 1
    
    def test_predict_invalid_features(self, predictor):
        """Test prediction with invalid features."""
        with pytest.raises(ValueError):
            predictor.predict("s1-s3", [0.75, 12.3])  # Only 2 features
    
    def test_predict_negative_features(self, predictor):
        """Test prediction with negative features."""
        with pytest.raises(ValueError):
            predictor.predict("s1-s3", [-0.75, 12.3, 0.02, 45.6, 0.8])
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test
pytest tests/test_lstm_model.py::TestLSTMPredictor::test_predict_valid_input

# Run with verbose output
pytest -v

# Run in parallel
pytest -n auto
```

### Test Coverage

- Aim for **80%+** code coverage
- All public functions must have tests
- Include edge cases and error conditions
- Test integration between components

---

## 📌 Commit Message Format

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Format Examples

```bash
# Feature commit
git commit -m "feat(lstm): add bidirectional LSTM layer

- Improves congestion prediction accuracy
- Processes sequences in both directions
- Adds 15% performance improvement"

# Bug fix
git commit -m "fix(api): handle missing features in prediction endpoint

Fixes #42

- Add validation for required fields
- Return meaningful error messages
- Add unit tests"

# Documentation
git commit -m "docs(api): update prediction endpoint documentation

- Add request/response examples
- Document error cases
- Add curl examples"
```

### Commit Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Test additions/updates
- `chore:` - Build/tooling changes
- `ci:` - CI/CD changes

---

## 🔄 Pull Request Process

### Before Submitting PR

1. **Update your branch**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   pytest --cov=backend
   ```

3. **Check code quality**:
   ```bash
   black backend/
   flake8 backend/
   pylint backend/
   mypy backend/
   ```

4. **Security check**:
   ```bash
   bandit -r backend/
   safety check
   ```

### PR Title and Description

**Use this template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Code review requested
```

### PR Review Process

1. **Automated checks** must pass:
   - Tests
   - Code quality
   - Security scan

2. **Human review** requirements:
   - At least 1 approval from core maintainers
   - Address feedback
   - Request re-review after changes

3. **Merge criteria**:
   - All checks pass
   - At least 1 approval
   - No conflicts with main
   - PR title and description are clear

---

## 🎯 Areas for Contribution

### 🟢 Beginner-Friendly

- [ ] Documentation improvements
- [ ] Add examples/tutorials
- [ ] Fix typos/grammar
- [ ] Add unit tests
- [ ] Improve comments

**Difficulty:** Easy | **Time:** 1-2 hours

### 🟡 Medium Difficulty

- [ ] API endpoint enhancements
- [ ] Performance optimizations
- [ ] Error handling improvements
- [ ] Logging enhancements
- [ ] Code refactoring

**Difficulty:** Medium | **Time:** 4-8 hours

### 🔴 High Priority Features

- [ ] Multi-Agent RL implementation
- [ ] Transformer-based predictor
- [ ] sFlow/NetFlow integration
- [ ] Intent-Based Networking
- [ ] gRPC telemetry plane

**Difficulty:** Hard | **Time:** 20+ hours

### 📚 Documentation Needed

- [ ] API documentation
- [ ] Development guide
- [ ] Deployment guide
- [ ] Troubleshooting guide
- [ ] Architecture documentation

### 🐛 Known Issues

See [GitHub Issues](https://github.com/aditya5289/AI-based-congestion-control-in-SDN/issues) for open issues to work on.

---

## 🆘 Getting Help

### Questions?

- **GitHub Discussions:** [Ask a question](https://github.com/aditya5289/AI-based-congestion-control-in-SDN/discussions)
- **Email:** adityamaurya@mmmut.ac.in
- **Issues:** [Create an issue](https://github.com/aditya5289/AI-based-congestion-control-in-SDN/issues)

### Resources

- [Development Guide](DEVELOPMENT.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Security Policy](SECURITY_POLICY.md)
- [README](README.md)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
