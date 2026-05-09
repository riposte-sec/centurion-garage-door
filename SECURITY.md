# Security Policy

## Supported Versions

Only the latest release is actively supported with security fixes.

| Version | Supported |
| ------- | --------- |
| Latest  | Yes       |
| Older   | No        |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately via one of the following:

- **GitHub private disclosure**: use the [Security Advisory](https://github.com/riposte-sec/centurion-garage-door/security/advisories/new) tab in this repository
- **Email**: claudeai@riposte.dev (include "SECURITY" in the subject line)

### What to include

- A clear description of the vulnerability and its potential impact
- Steps to reproduce or a proof-of-concept
- Affected version(s)
- Any suggested fix, if you have one

### Response timeline

| Milestone | Target |
| --------- | ------ |
| Initial acknowledgement | 48 hours |
| Triage and severity assessment | 5 business days |
| Fix or mitigation | Depends on severity |

We will keep you informed as the issue is investigated and resolved. We ask that you observe responsible disclosure and allow us reasonable time to address the issue before any public disclosure.

## Scope

This integration runs entirely on your local network and communicates with your Centurion garage door controller via its local API. Security-relevant areas include:

- Credential handling (API keys, camera stream credentials stored in Home Assistant config entries)
- Network communication between Home Assistant and the local device
- Authentication and authorisation within the integration's config flow

Out of scope:
- Vulnerabilities in Home Assistant Core itself — report those to the [Home Assistant security team](https://www.home-assistant.io/security/)
- Vulnerabilities in the Centurion device firmware — contact Centurion directly
- Issues that require physical access to the local network with no additional attack surface
