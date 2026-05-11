import argparse
import asyncio
import os

from playwright.async_api import Page, async_playwright

from lianjia_crawler.consts import BROWSER_STATE_FILE, home_url


async def signin(args: argparse.Namespace) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
        )
        context = await browser.new_context(
            storage_state=None
            if args.new or not BROWSER_STATE_FILE.exists()
            else BROWSER_STATE_FILE
        )
        page = await context.new_page()
        await page.goto(home_url, wait_until="commit")
        future = asyncio.futures.Future[None]()
        page.once("close", lambda x: future.set_result(None))
        await future
        os.makedirs(BROWSER_STATE_FILE.parent, exist_ok=True)
        await context.storage_state(path=BROWSER_STATE_FILE)
        await playwright.stop()


async def worker(page: Page) -> None:
    future = asyncio.futures.Future[None]()
    page.once("close", lambda x: future.set_result(None))
    await future


async def run(args: argparse.Namespace) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
        )
        context = await browser.new_context(
            storage_state=BROWSER_STATE_FILE if BROWSER_STATE_FILE.exists() else None,
        )
        async with asyncio.TaskGroup() as tg:
            for _ in range(args.jobs):
                tg.create_task(worker(await context.new_page()))
        await playwright.stop()


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    login_parser = subparsers.add_parser("login")
    login_parser.add_argument(
        "--new",
        action="store_true",
        help="Don't load the old browser context",
    )
    login_parser.set_defaults(func=signin)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=4,
        help="Number of tabs to open concurrently",
    )
    run_parser.set_defaults(func=run)
    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
