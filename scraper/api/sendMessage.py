import os, pickle, asyncio, logging
from nodriver import Browser, Element, cdp, start
from functions.getUserAgent import *

logging.basicConfig(level=logging.INFO)

async def loadCookiesAndVerify(browser: Browser) -> bool: 
    if os.path.exists('/opt/meinanzeigen/cookies.pkl') and os.path.getsize('/opt/meinanzeigen/cookies.pkl') > 0:
        tab = await browser.get('https://www.kleinanzeigen.de/')
        await tab
        try:
            with open('/opt/meinanzeigen/cookies.pkl', 'rb') as f:
                cookies = pickle.load(f)
                await tab.send(cdp.storage.set_cookies(cookies))
                logging.info("Cookies loaded successfully.")
            await tab.reload()
            agb_button: Element | None = None
            try:
                agb_button = await tab.select('button#gdpr-banner-accept', timeout=3)
            except TimeoutError:
                logging.warning("AGB banner not found, continuing.")
                pass
            if agb_button is not None:
                await agb_button.click()
            logged_in: Element | None = None
            try:
                logged_in = await tab.select('p[data-testid="logged-in-user"]')
            except TimeoutError:
                logging.error("Logged in user not found.")
                return False
            if logged_in is not None:
                logging.debug(logged_in.text)
                return True
        except EOFError:
            logging.error("Cookie file is empty or corrupted, logging in again.")
            return False

# Function to log in to Kleinanzeigen.de and send a message
async def sendMessage(inserat_url, msg):
    try:
        browser = await start(
            browser_args=[
                "--headless=new",
                "--disable-web-security",
            ]
        )
        await loadCookiesAndVerify(browser)
        tab = await browser.get(inserat_url)
        await tab
        msg_button: Element | None = None

        try:
            msg_button = await tab.select('button[id="viewad-contact-button"]', timeout=3)
        except TimeoutError:
            logging.error("Message me button not found.")
            return False

        if msg_button is not None:
            await msg_button.click()

        await asyncio.sleep(3)

        msg_textarea: Element | None = None
        try:
            msg_textarea = await tab.select('textarea[class="viewad-contact-message"]', timeout=3)
        except TimeoutError:
            logging.error("Message textarea not found.")
            return False

        if msg_textarea is not None:
            await msg_textarea.send_keys(msg)

        msg_sentbtn: Element | None = None
        try:
            msg_sentbtn = await tab.select('button[class="button viewad-contact-submit taller"]', timeout=3)
        except TimeoutError:
            logging.error("Send message button not found.")
            return False

        if msg_sentbtn is not None:
            await msg_sentbtn.click()
            logging.info("Sent message!") 
            return True

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False