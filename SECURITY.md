# Security Policy

## 🔒 Reporting Security Vulnerabilities

**IMPORTANT:** Please do NOT file public GitHub issues for security vulnerabilities.

### Responsible Disclosure

If you discover a security vulnerability in TES Algorithm UVEG, please email:

- **Primary Contact:** daniel.salinas@uv.es
- **Secondary Contact:** drazen.skokovic@uv.es

### What to Include

1. **Description:** Clear, detailed description of the vulnerability
2. **Impact:** Potential impact on users and systems
3. **Reproduction Steps:** Step-by-step instructions to reproduce
4. **Proposed Fix:** If you have one (optional but helpful)
5. **Your Contact:** How to reach you for follow-up

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Every 7 days during investigation
- **Resolution:** Within 30 days when possible
- **Disclosure Coordination:** 90 days after patch release

---

## 🛡️ Security Practices

### Code Security

1. **No Hardcoded Secrets**
   - Never commit API keys, passwords, or tokens
   - Use `.env` for sensitive configuration
   - `.env` is in `.gitignore`

2. **Dependency Scans**
   - All dependencies pinned in `requirements.txt`
   - Regular updates for security patches
   - Use `pip audit` to check vulnerabilities:
     ```bash
     pip install pip-audit
     pip-audit
     ```

3. **Type Safety**
   - Encouraged use of type hints (PEP 561)
   - Use `mypy` for static type checking

---

## ✅ Security Checklist for Contributors

Before submitting a pull request:

- [ ] No secrets in code (API keys, credentials, passwords)
- [ ] No hardcoded paths (use environment variables)
- [ ] External dependencies reviewed and trusted
- [ ] Input validation on untrusted data
- [ ] Proper error handling (no stack traces exposed)
- [ ] No SQL injection vulnerabilities (if applicable)
- [ ] Dependencies pass `pip audit` check

```bash
# Run security checks
pip-audit
mypy services/ utilities/ --strict
flake8 services/ utilities/ --select=B
```

---

## 🔐 Sensitive Data Guidelines

### What NOT to Commit

- ❌ `.env` files with real credentials
- ❌ Private SSH keys (`.pem`, `.key`)
- ❌ AWS credentials or tokens
- ❌ Database credentials
- ❌ API keys
- ❌ Personal information (emails, phone numbers)
- ❌ Large data files not needed for repository

### Secure Alternatives

- ✅ Use `.env.example` for templates
- ✅ Document required secrets with dummy values
- ✅ Use GitHub Secrets for CI/CD
- ✅ Use AWS Secrets Manager for production

### If You Accidentally Committed Secrets

1. **Immediately Rotate** the exposed credentials
2. **Contact maintainers** at daniel.salinas@uv.es
3. **Remove from history** using:
   ```bash
   git filter-branch --index-filter "git rm -r --cached --ignore-unmatch <file>" HEAD
   ```
4. **Force push** (use with caution):
   ```bash
   git push --force origin main
   ```

---

## 🔄 Dependencies & Updates

### Staying Up-to-Date

```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt safely
pip-upgrade --requirement requirements.txt

# Audit for vulnerabilities
pip-audit --fix
```

### Critical Dependencies

- **netCDF4:** HDF5/NetCDF-C library bindings - HIGH RISK if compromised
- **NumPy:** Core numerical library - HIGH RISK if compromised
- **RTTOV:** External radiative transfer - VERIFY sources

### Verification

All critical packages should be sourced from:
- Official PyPI (pypi.org)
- Official GitHub repositories
- Verified upstream maintainers

---

## 🚨 Known Vulnerabilities

### None Currently Identified

This project does not have any known critical security vulnerabilities as of June 2026.

For details on past vulnerabilities, see [CHANGELOG.md](CHANGELOG.md#security-advisories).

---

## 🔐 Production Deployment Security

### Before Production Deployment

1. **Environment Variables**
   ```bash
   export RTTOV_ROOT_PATH=/path/to/rttov
   export MODIS_DATA_PATH=/path/to/data
   export OUTPUT_PATH=/path/to/output
   # Never log these in output
   ```

2. **File Permissions**
   ```bash
   # Restrict access to sensitive data
   chmod 750 /path/to/output/
   chmod 640 .env
   ```

3. **Logging**
   - Never log sensitive paths or values
   - Enable structured logging for auditing
   - Set appropriate log levels (not DEBUG in production)

4. **Access Control**
   - Restrict data directory access
   - Use SSH keys (not passwords)
   - Implement role-based access control

5. **Monitoring**
   - Enable error notification system
   - Monitor disk space and memory
   - Set up security alerts

---

## 📋 Compliance & Standards

### Standards Followed

- **OWASP Top 10:** Prevention measures for web/API security
- **PEP 8:** Python code style and security guidelines
- **semver:** Semantic versioning for releases
- **CWE-89:** SQL Injection prevention (if applicable)
- **CWE-434:** Unrestricted File Upload prevention

### Data Protection

- **Data Anonymization:** User/institution data anonymized in examples
- **GDPR:** Compliant with personal data handling
- **Open Science:** Data sharing with privacy controls

---

## 🔍 Audit Trail

### Git Security

- All commits must be signed (recommended):
  ```bash
  git config --global user.signingkey <your-key>
  git commit -S -m "message"
  ```

- Protect main branch:
  - Require pull request reviews
  - Require status checks before merge
  - Dismiss stale PR approvals
  - Require code owner review

### Access Logs

- GitHub Actions logs reviewed quarterly
- Deployment logs archived for 1 year
- Security incidents documented

---

## 📞 Security Contact

**For security issues:** daniel.salinas@uv.es  
**For policy questions:** drazen.skokovic@uv.es  
**General inquiries:** jose.sobrino@uv.es

---

## 📚 References

- [OWASP Security Guidelines](https://owasp.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [PEP 529: Change Windows filesystem encoding to UTF-8](https://www.python.org/dev/peps/pep-0529/)

---

**Last Updated:** June 2026  
**Policy Version:** 1.0

*This security policy is subject to updates without prior notice.*
