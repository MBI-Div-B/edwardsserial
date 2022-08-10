# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<details>
<summary> How to write the changelog </summary>

### Guiding Principles

- Changelogs are for humans, not machines.
- There should be an entry for every single version.
- The same types of changes should be grouped.
- Versions and sections should be linkable.
- The latest version comes first.
- The release date of each version is displayed.
- Mention whether you follow Semantic Versioning.

### Types of changes

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

</details>

## [unreleased] - YYYY-MM-DD
### Added
...

## [0.3.3] - 2022-08-09
### Added
- CHANGELOG.md
- LICENSE
- CONTRIBUTING.md

### Changed
- README.md
- `edwardsserial.serial_protocol.SerialProtocol` now uses `pyserial.serial_for_url` instead of `pyserial.Serial` (contribution by [Paul Grimes](https://gitlab.com/PaulKGrimes))
- dependency: pyserial>2.5.0
