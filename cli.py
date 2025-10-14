#!/usr/bin/env python3
"""
Command-line interface for the media crawler.
Provides easy access to crawler functionality from the terminal.
"""
import argparse
import logging
import sys
import os
from typing import List

from media_crawler.config import (
    ApplicationConfig, CrawlerConfig, DatabaseConfig,
    DownloadConfig, SeleniumConfig
)
from media_crawler.factory import CrawlerFactory
from media_crawler.exceptions import CrawlerException

# Configure logging
logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Media Crawler - Download content from YouTube, SoundCloud, and more',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # YouTube search
  python cli.py youtube -k "lofi hip hop" "jazz music" -d 2
  
  # YouTube direct URLs
  python cli.py youtube -u "https://youtube.com/@channel" -d 1
  
  # SoundCloud
  python cli.py soundcloud -u "https://soundcloud.com/discover" -d 3
  
  # Custom settings
  python cli.py youtube -k "ambient" -d 2 -w 16 -o ~/Music/Ambient/ -q 320
        """
    )
    
    # Platform selection
    parser.add_argument(
        'platform',
        choices=['youtube', 'soundcloud'],
        help='Platform to crawl'
    )
    
    # Input URLs or keywords
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-u', '--urls',
        nargs='+',
        help='Starting URLs to crawl'
    )
    input_group.add_argument(
        '-k', '--keywords',
        nargs='+',
        help='Search keywords (YouTube only)'
    )
    
    # Crawler settings
    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=2,
        help='Maximum crawl depth (default: 2)'
    )
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=8,
        help='Number of parallel download workers (default: 8)'
    )
    parser.add_argument(
        '-s', '--scroll',
        type=int,
        default=10,
        help='Number of page scrolls (default: 10)'
    )
    
    # Download settings
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output folder for downloads'
    )
    parser.add_argument(
        '-q', '--quality',
        type=str,
        default='192',
        help='Audio quality/bitrate (default: 192)'
    )
    parser.add_argument(
        '-f', '--format',
        type=str,
        default='mp3',
        choices=['mp3', 'wav', 'flac', 'm4a'],
        help='Audio format (default: mp3)'
    )
    
    # Database settings
    parser.add_argument(
        '--db',
        type=str,
        help='Database file path'
    )
    
    # Other settings
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Show browser window (not headless)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output (DEBUG level)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output (errors only)'
    )
    parser.add_argument(
        '--clear-state',
        action='store_true',
        help='Clear saved state and start fresh'
    )
    
    return parser.parse_args()


def build_config(args) -> ApplicationConfig:
    """
    Build application configuration from command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Application configuration
    """
    # Crawler config
    crawler_config = CrawlerConfig(
        max_depth=args.depth,
        max_workers=args.workers,
        scroll_count=args.scroll
    )
    
    # Database config
    db_path = args.db if args.db else f"{args.platform}.db"
    database_config = DatabaseConfig(db_path=db_path)
    
    # Download config
    download_config = DownloadConfig(
        download_folder=args.output if args.output else os.path.expanduser('~/Music/Downloads/'),
        audio_quality=args.quality,
        audio_format=args.format
    )
    
    # Selenium config
    selenium_config = SeleniumConfig(
        headless=not args.no_headless
    )
    
    # Platform config
    if args.platform == 'youtube':
        config = ApplicationConfig.for_youtube(
            crawler_config=crawler_config,
            database_config=database_config,
            download_config=download_config,
            selenium_config=selenium_config
        )
    elif args.platform == 'soundcloud':
        config = ApplicationConfig.for_soundcloud(
            crawler_config=crawler_config,
            database_config=database_config,
            download_config=download_config,
            selenium_config=selenium_config
        )
    else:
        raise ValueError(f"Unsupported platform: {args.platform}")
    
    return config


def get_start_urls(args) -> List[str]:
    """
    Get starting URLs from arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        List of starting URLs
    """
    if args.urls:
        return args.urls
    elif args.keywords:
        if args.platform != 'youtube':
            raise ValueError("Keywords search only supported for YouTube")
        return [f'https://youtube.com/results?search_query={kw}' for kw in args.keywords]
    else:
        raise ValueError("Either --urls or --keywords must be provided")


def main():
    """Main CLI entry point."""
    args = parse_arguments()
    
    # Set logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Build configuration
        config = build_config(args)
        if not args.quiet:
            logger.info(f"Configuration: Platform={args.platform}, Depth={args.depth}, Workers={args.workers}")
        
        # Get start URLs
        start_urls = get_start_urls(args)
        if not args.quiet:
            logger.info(f"Starting URLs: {start_urls}")
        
        # Create crawler
        crawler = CrawlerFactory.create_crawler(config, start_urls, quiet=args.quiet)
        
        # Clear state if requested
        if args.clear_state:
            crawler.state_manager.clear_state()
            if not args.quiet:
                logger.info("Cleared saved state")
        
        # Run crawler
        if not args.quiet:
            logger.info("Starting crawl...")
        crawler.crawl()
        
        # Show statistics (progress display already shows summary)
        if args.quiet:
            stats = crawler.get_stats()
            logger.info("=" * 60)
            logger.info("CRAWL COMPLETED")
            logger.info("=" * 60)
            logger.info(f"URLs in queue: {stats['queue_size']}")
            logger.info(f"URLs visited: {stats['visited_count']}")
            logger.info(f"Tracks downloaded: {stats['downloaded_count']}")
            logger.info(f"Tracks pending: {stats['pending_count']}")
            logger.info("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except CrawlerException as e:
        logger.error(f"Crawler error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
