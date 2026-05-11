import asyncio

from playwright.async_api import async_playwright


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
        )
        page = await browser.new_page()
        await page.goto(
            "https://sh.lianjia.com/ershoufang/", wait_until="domcontentloaded"
        )
        future = asyncio.futures.Future[None]()
        page.once("close", lambda x: future.set_result(None))
        await future
        await playwright.stop()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
