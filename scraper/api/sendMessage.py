import os, pickle, asyncio, logging, time, re
from nodriver import Browser, Element, cdp, Tab, start
from functions.getUserAgent import *

logging.basicConfig(level=logging.INFO)


def isPklFile(path):
    try:
        with open(path, "rb") as f:
            pickle.load(f)
        return True
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError):
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


def extract_timestamp(filename: str):
    """
    Extracts a UNIX timestamp from filenames matching 'cookies.<timestamp>.pkl'.
    Returns the timestamp as an int, or None if no match is found.
    """
    match = re.search(r"^cookies\.(\d+)\.pkl$", filename)
    return int(match.group(1)) if match else None


def loadCookiesPklFromDisk(path: str):
    try:
        if not os.path.isdir(path):
            logging.error(f"Provided path is not a directory: {path}")
            return None

        pkl_files = [f for f in os.listdir(path) if f.endswith(".pkl")]
        timestamped = []
        for f in pkl_files:
            ts = extract_timestamp(f)
            if ts is not None:
                timestamped.append((ts, f))

        if timestamped:
            # Use the file with the highest timestamp
            _, best_file = max(timestamped)
        elif "cookies.pkl" in pkl_files:
            best_file = "cookies.pkl"
        else:
            logging.error("No valid cookies .pkl file found.")
            return None

        full_path = os.path.join(path, best_file)

        if (
            os.path.exists(full_path)
            and os.path.getsize(full_path) > 0
            and isPklFile(full_path)
        ):
            with open(full_path, "rb") as f:
                return pickle.load(f)
        else:
            logging.error(f"Selected cookie file is invalid: {full_path}")
            return None

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None


async def saveCookiesAsPkl(tab: Tab, path: str):
    try:
        cookies = await tab.send(cdp.storage.get_cookies())
        with open(path, "wb") as f:
            pickle.dump(cookies, f)
        if os.path.exists(path) and os.path.getsize(path) > 0 and isPklFile(path):
            logging.info("Successfully saved cookies pkl file.")
        else:
            logging.error("Error saving cookies pkl file.")
    except Exception as e:
        logging.error(f"Unexpected error while saving cookies: {e}")
        return False


async def login(browser: Browser) -> bool:
    tab = await browser.get("https://www.kleinanzeigen.de/")
    await tab
    cookies = loadCookiesPklFromDisk("/opt/meinanzeigen/")
    if cookies is not None:
        # print(getCookieUrls(cookies))
        await tab.send(cdp.storage.set_cookies(cookies))
        logging.info("Cookies loaded successfully.")
        await tab.reload()
    else:
        logging.error("Error loading cookies.")
        return
    agb_button: Element | None = None
    try:
        agb_button = await tab.select("button#gdpr-banner-accept", timeout=5)
    except TimeoutError:
        logging.warning("AGB banner not found, continuing.")
        pass
    if agb_button is not None:
        await agb_button.click()
    logged_in: Element | None = None
    try:
        logged_in = await tab.select('p[data-testid="logged-in-user"]', timeout=10)
    except TimeoutError:
        logging.error("Logged in user not found.")
        return False
    if logged_in is not None:
        logging.debug(logged_in.text)
        await saveCookiesAsPkl(
            tab, "/opt/meinanzeigen/cookies." + str(time.time()) + ".pkl"
        )
        return True


# Function to log in to Kleinanzeigen.de and send a message
async def sendMessage(inserat_url, msg):
    try:
        browser = await start(
            browser_args=[
                "--headless=new",
                "--disable-web-security",
            ]
        )
        await login(browser)
        tab = await browser.get(inserat_url)
        await tab
        msg_button: Element | None = None

        try:
            msg_button = await tab.select(
                'button[id="viewad-contact-button"]', timeout=6
            )
        except TimeoutError:
            logging.error("Message me button not found.")
            return

        if msg_button is not None:
            await msg_button.click()

        await asyncio.sleep(3)

        msg_textarea: Element | None = None
        try:
            msg_textarea = await tab.select(
                'textarea[class="viewad-contact-message"]', timeout=6
            )
        except TimeoutError:
            logging.error("Message textarea not found.")
            return

        if msg_textarea is not None:
            await msg_textarea.send_keys(msg)

        msg_sentbtn: Element | None = None
        try:
            msg_sentbtn = await tab.select(
                'button[class="button viewad-contact-submit taller"]', timeout=6
            )
        except TimeoutError:
            logging.error("Send message button not found.")
            return

        if msg_sentbtn is not None:
            await msg_sentbtn.click()
            logging.info("Sent message!")
            return

    except Exception as e:
        logging.error(f"An error occurred: {e} at kleinanzeigen-URL: {inserat_url}")
        return
