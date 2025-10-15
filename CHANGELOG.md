# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Complete documentation suite

## [1.0.0] - 2024-10-15

### Added
- Core crawler functionality with depth-based traversal
- Multi-platform support (YouTube and SoundCloud)
- Parallel download manager with configurable workers
- SQLite database for tracking downloads and preventing duplicates
- State management for resumable crawls
- Rich progress display with real-time updates
- Command-line interface with extensive options
- Configuration system using dataclasses
- Retry mechanism with exponential backoff
- Selenium WebDriver integration for dynamic content
- yt-dlp integration for media downloads
- Link extraction strategies (Strategy pattern)
- Factory pattern for component creation
- Dependency injection architecture
- Comprehensive error handling and custom exceptions
- Type hints throughout codebase
- Extensive documentation (README, API, Architecture)
- Example scripts demonstrating usage
- Unit tests for core components

### Features

#### Crawler
- Configurable maximum depth
- Parallel worker threads
- Dynamic page scrolling for lazy-loaded content
- Smart URL filtering and deduplication
- Platform-specific link extraction
- Automatic state persistence

#### Downloads
- Multiple format support (MP3, M4A, etc.)
- Configurable audio quality
- Automatic audio conversion via FFmpeg
- Resume capability for interrupted downloads
- Duplicate detection and skipping
- Parallel download execution

#### Database
- SQLite backend
- Track metadata storage
- Download status tracking
- Timestamp recording
- Indexed queries for performance
- Thread-safe operations

#### CLI
- Keyword search support (YouTube)
- Direct URL crawling
- Multiple URL inputs
- Customizable output directories
- Quality settings
- Worker pool configuration
- Verbose logging option
- Headless/headed browser mode
- State resumption controls

#### Configuration
- Modular configuration classes
- Factory methods for common platforms
- Sensible defaults
- Full customization support
- Validation on initialization

### Technical Details

#### Architecture
- SOLID principles implementation
- Interface-based design
- Factory pattern for object creation
- Strategy pattern for platform-specific logic
- Dependency injection throughout
- Clear separation of concerns

#### Code Quality
- Type hints for all public APIs
- Docstrings following Google style
- PEP 8 compliance
- Comprehensive error handling
- Logging throughout application
- Thread-safe operations

#### Dependencies
- selenium - Browser automation
- yt-dlp - Media downloading
- beautifulsoup4 - HTML parsing
- rich - Terminal formatting
- sqlite3 - Database (built-in)

### Documentation
- Comprehensive README with examples
- Detailed API documentation
- Architecture documentation
- Contributing guidelines
- Code of conduct
- License (MIT)

### Examples
- Basic usage examples
- Advanced configuration examples
- Platform-specific examples
- Error handling examples
- Diagnostic scripts

### Known Limitations
- Requires Chrome/Chromium browser
- Requires ChromeDriver installation
- Some platforms may require authentication
- Rate limiting may affect performance
- Dynamic content may not always load completely

### Future Roadmap
- Additional platform support (Spotify, Apple Music, etc.)
- GUI interface
- Playlist management features
- Video download support
- Docker containerization
- Cloud storage integration
- REST API
- Real-time monitoring dashboard
- Distributed crawling support
- Advanced filtering options
- Custom hook system for events
- Plugin architecture for extensions

## [0.9.0] - 2024-10-01 (Beta)

### Added
- Initial beta release
- Core crawler functionality
- YouTube support
- Basic CLI interface
- Database tracking
- Download management

### Changed
- Refactored from monolithic script to modular architecture
- Improved error handling
- Better progress reporting

### Fixed
- Various bug fixes from alpha testing
- Memory leaks in download manager
- State persistence issues

## [0.5.0] - 2024-09-15 (Alpha)

### Added
- Proof of concept implementation
- Basic YouTube crawling
- Simple download functionality
- Minimal CLI

### Known Issues
- Limited error handling
- No state management
- Performance issues with large crawls
- Memory leaks

---

## Version History

- **1.0.0** - First stable release with full feature set
- **0.9.0** - Beta release with core functionality
- **0.5.0** - Alpha/proof of concept

## Upgrade Guide

### From 0.9.0 to 1.0.0

**Configuration Changes:**
- State file management has been simplified
- Database paths now support relative and absolute paths
- New configuration options for retry behavior

**API Changes:**
- `CrawlerFactory.create_crawler()` now uses `state_file_name` as optional parameter
- Added new factory methods: `for_youtube()` and `for_soundcloud()`
- Progress display can now be toggled with `quiet` parameter

**Breaking Changes:**
- State file format has changed (old states will be migrated automatically)
- Some internal APIs have been refactored (only affects direct internal usage)

**Migration:**
```python
# Old (0.9.0)
crawler = CrawlerFactory.create_crawler(
    config=config,
    start_urls=urls,
    state_file="state.json"
)

# New (1.0.0)
crawler = CrawlerFactory.create_crawler(
    config=config,
    start_urls=urls,
    # state_file_name is now optional and deprecated
)
```

## Support

For issues, questions, or contributions:
- **GitHub Issues**: [Report bugs or request features](https://github.com/HasanRagab/media-crawler/issues)
- **GitHub Discussions**: [Ask questions or discuss](https://github.com/HasanRagab/media-crawler/discussions)
- **Email**: hasanmragab@gmail.com

---

**Note**: This project follows semantic versioning. Version numbers follow the format MAJOR.MINOR.PATCH where:
- MAJOR version changes for incompatible API changes
- MINOR version adds functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes
