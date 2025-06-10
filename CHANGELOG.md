# Changelog

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-06-10

### Changed

- Updated Dockerfile to use Alpine-based Python 3.13.4 image for reduced image
  size and lower CVE exposure.
- Replaced Debian `slim-bookworm` base image with `alpine3.22`.
- Installed runtime dependencies using `apk` for compatibility and minimal footprint.
- Restructured multi-stage build for clearer separation between build-time and
  runtime layers.
- Ensured only required packages and binaries are included in final image.

### Security

- Removed known Python package vulnerabilities by upgrading:
  - `setuptools`
  - `requests`
  - `starlette`
  - Other indirect dependencies
- Eliminated high and critical OS-level CVEs by switching to Alpine base and
  removing unnecessary system packages.

## [1.0.0] - Initial release

- First public release of the Accounts Service application.
