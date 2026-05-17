# Security Policy

## Reporting Security Vulnerabilities

### Please Do NOT Create Public Issues

If you discover a security vulnerability, **please email** the details instead of creating a public GitHub issue.

**Email:** adityamaurya@mmmut.ac.in  
**Subject:** `[SECURITY] Vulnerability Report - [Brief Description]`

Include the following information:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

- **24 hours:** Initial acknowledgment
- **72 hours:** Initial assessment
- **7 days:** Proposed timeline for fix
- **30 days:** Target fix release

---

## Security Best Practices

### Authentication & Authorization

```python
# Good - Use strong authentication
@app.route("/api/protected")
@require_auth
def protected_endpoint():
    return jsonify({"data": "sensitive"})

# Bad - No authentication
@app.route("/api/data")
def public_endpoint():
    return sensitive_data
```

### Input Validation

```python
# Good - Validate all inputs
def predict(link_id: str, features: List[float]) -> Dict:
    if not isinstance(features, list):
        raise ValueError("Features must be a list")
    
    if len(features) != 5:
        raise ValueError("Expected 5 features")
    
    if any(f < 0 for f in features):
        raise ValueError("Features must be non-negative")

# Bad - No validation
def predict(link_id, features):
    return model.predict([features])
```

### SQL Injection Prevention

```python
# Good - Use parameterized queries
db.execute(
    "SELECT * FROM predictions WHERE link_id = ?",
    (link_id,)
)

# Bad - String concatenation
query = f"SELECT * FROM predictions WHERE link_id = '{link_id}'"
db.execute(query)
```

### CORS Configuration

```python
# Good - Restrict origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://trusted-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"],
    }
})

# Bad - Allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})
```

### Error Handling

```python
# Good - Don't expose sensitive information
try:
    result = model.predict(features)
except Exception as e:
    logger.error(f"Prediction error: {str(e)}")
    return jsonify({"error": "Prediction failed"}), 500

# Bad - Exposing error details
try:
    result = model.predict(features)
except Exception as e:
    return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
```

### Dependency Management

```bash
# Check for vulnerable dependencies
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit

# Keep dependencies updated
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Environment Variables

```bash
# Good - Use .env for sensitive data
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')

# Bad - Hardcoding secrets
SECRET_KEY = "my-secret-key"

# .gitignore
.env
.env.local
*.key
*.pem
```

---

## HTTPS/SSL Configuration

### Required Security Headers

```nginx
# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

### SSL/TLS Configuration

```nginx
# Modern (recommended)
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;

# Add HSTS header
add_header Strict-Transport-Security "max-age=31536000" always;
```

---

## Database Security

### Connection Security

```python
# Good - Secure connection
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "username": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "ssl": True,
    "authSource": "admin",
}

# Bad - Plain text credentials
db_config = {
    "host": "localhost",
    "username": "admin",
    "password": "password123",
}
```

### Data Encryption

```python
from cryptography.fernet import Fernet

# Encrypt sensitive data
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"sensitive data")

# Decrypt
decrypted = cipher.decrypt(encrypted)
```

---

## API Security

### Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@limiter.limit("5 per minute")
@app.route("/api/predict", methods=["POST"])
def predict():
    pass
```

### API Authentication

```python
from functools import wraps
import jwt

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            request.user = data
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/api/protected")
@require_auth
def protected_endpoint():
    return jsonify({"user": request.user})
```

---

## Code Security

### Static Analysis Tools

```bash
# Bandit - Security issues
bandit -r backend/

# Pylint - Code quality
pylint backend/

# MyPy - Type checking
mypy backend/

# Flake8 - Style guide
flake8 backend/
```

### Security Scanning in CI/CD

```yaml
# GitHub Actions
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install bandit safety pip-audit
      - name: Run security checks
        run: |
          bandit -r backend/
          safety check
          pip-audit
```

---

## Infrastructure Security

### Firewall Rules

```bash
# Only allow required ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp          # SSH
sudo ufw allow 80/tcp          # HTTP
sudo ufw allow 443/tcp         # HTTPS
sudo ufw allow 5000/tcp        # Backend (restricted)
sudo ufw enable
```

### Network Isolation

```yaml
# Kubernetes Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: sdn-ai-policy
spec:
  podSelector:
    matchLabels:
      app: sdn-ai-backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: sdn-ai
      ports:
        - protocol: TCP
          port: 5000
```

---

## Monitoring & Auditing

### Security Logging

```python
import logging

# Audit logger
audit_logger = logging.getLogger("audit")

def log_security_event(event: str, user: str, status: str):
    audit_logger.info(
        f"Security Event: {event} | User: {user} | Status: {status}"
    )

# Log authentication attempts
log_security_event("login", user_id, "success")
log_security_event("api_access", user_id, "granted")
```

### Intrusion Detection

```bash
# Install AIDE (File Integrity Monitoring)
sudo apt install aide aide-common
sudo aideinit
sudo aide --check
```

---

## Compliance

### GDPR Compliance

- [ ] User consent for data collection
- [ ] Data retention policies
- [ ] Right to be forgotten implementation
- [ ] Data export functionality
- [ ] Privacy policy documentation

### Data Protection

- [ ] Encryption at rest
- [ ] Encryption in transit (HTTPS)
- [ ] Secure password hashing (bcrypt)
- [ ] Access control lists
- [ ] Audit logging

---

## Security Checklist

### Before Deployment

- [ ] All dependencies are up-to-date
- [ ] No hardcoded secrets in code
- [ ] All inputs are validated
- [ ] HTTPS is enabled
- [ ] Security headers are configured
- [ ] Rate limiting is implemented
- [ ] Authentication is enforced
- [ ] Logging is configured
- [ ] Error handling doesn't expose sensitive info
- [ ] Database credentials are secured
- [ ] API keys are rotated
- [ ] Firewall is configured
- [ ] Security scan passed (bandit, safety)
- [ ] Code review completed
- [ ] Documentation updated

### During Production

- [ ] Monitor security logs
- [ ] Check for unusual activity
- [ ] Verify SSL certificate validity
- [ ] Update dependencies regularly
- [ ] Audit user access
- [ ] Back up sensitive data

### After Incident

- [ ] Document incident details
- [ ] Identify root cause
- [ ] Implement fix
- [ ] Deploy patch
- [ ] Communicate with users
- [ ] Post-incident review

---

## Vulnerability Disclosure

If you discover a vulnerability:

1. **DO NOT** disclose publicly
2. **Email** security details
3. **Wait** for acknowledgment
4. **Provide** additional info if requested
5. **Respect** coordinated disclosure timeline

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Flask Security](https://flask-security-too.readthedocs.io/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

## Contact

**Security Email:** adityamaurya@mmmut.ac.in  
**Response Time:** 24-72 hours
