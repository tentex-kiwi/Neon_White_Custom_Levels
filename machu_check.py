from playwright.sync_api import sync_playwright
import time
import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "jordan.stinson@gmail.com"
EMAIL_PASSWORD = "lssb ioke oiyv rhea"
TO_EMAIL = "jordan.stinson@gmail.com"

URL = "https://tuboleto.cultura.pe/llaqta_machupicchu"
ALREADY_SENT = set()

CHECK_INTERVAL_SECONDS = 600  # 10 minutes

TARGET_DAYS = ["1", "2", "3", "4"]

CIRCUITS = {
    "Circuito 1 - Panorámico": [
        "Ruta 1-A: Ruta Montaña Machupicchu",
        "Ruta 1-B: Ruta terraza superior",
    ],
    "Circuito 2 - Circuito clásico": [
        "Ruta 2-A: Ruta clásico diseñada",
        "Ruta 2-B: Ruta terraza inferior",
    ],
    "Circuito 3 - Machupicchu realeza": [
        "Ruta 3-A: Ruta Montaña Waynapicchu",
    ]
}

def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            smtp.send_message(msg)

        print("Email sent.")

    except Exception as e:

        print(f"Email failed: {e}")

def load_page(page):
    print("\nLoading page...")

    page.goto(
        URL,
        wait_until="networkidle"
    )

    time.sleep(5)


def select_circuit(page, circuit):

    print(f"Selecting circuit: {circuit}")

    page.locator("#mat-select-value-1").click()

    time.sleep(1)

    page.get_by_role(
        "option",
        name=circuit
    ).click()

    time.sleep(2)


def select_route(page, route):

    print(f"Selecting route: {route}")

    page.locator("#mat-select-value-3").click()

    time.sleep(1)

    page.get_by_role(
        "option",
        name=route
    ).click()

    time.sleep(2)


def ensure_calendar_open(page):

    overlays = page.locator(
        ".mat-datepicker-content"
    )

    # Already open
    if overlays.count() > 0:

        print("Calendar already open.")

        return

    print("Opening calendar...")

    calendar_input = page.locator(
        "input"
    ).first

    # JS click avoids overlay issues
    calendar_input.dispatch_event("click")

    page.locator(
        ".mat-datepicker-content"
    ).wait_for(timeout=5000)

    print("Calendar opened.")


def close_calendar(page):

    try:

        backdrop = page.locator(
            ".cdk-overlay-backdrop"
        )

        if backdrop.count() > 0:

            backdrop.click()

            time.sleep(1)

            print("Calendar closed.")

    except Exception as e:

        print(f"Close calendar failed: {e}")


def go_to_june(page):

    while True:

        header = page.locator(
            ".mat-calendar-period-button"
        ).inner_text()

        print(f"Calendar header: {header}")

        if "JUN" in header.upper():
            return

        page.get_by_label(
            "Next month"
        ).click()

        time.sleep(1)


def check_days(page, circuit, route):

    cells = page.locator(
        ".mat-calendar-body-cell"
    )

    count = cells.count()

    print(f"Found {count} calendar cells")

    for target_day in TARGET_DAYS:

        found = False

        for i in range(count):

            cell = cells.nth(i)

            text = cell.inner_text().strip()

            if text != target_day:
                continue

            found = True

            classes = cell.get_attribute(
                "class"
            ) or ""

            if "disabled" in classes.lower():

                print(
                    f"❌ {route} — June {target_day} DISABLED"
                )

            else:

                message = (
                    f"MACHU PICCHU TICKETS FOUND\n\n"
                    f"Circuit: {circuit}\n"
                    f"Route: {route}\n"
                    f"Date: June {target_day}, 2026"
                )

                print(message)

                key = f"{circuit}-{route}-{target_day}"

                if key not in ALREADY_SENT:

                    ALREADY_SENT.add(key)

                    send_email(
                        "Machu Picchu Tickets Found",
                        message
                    )

            break

        if not found:

            print(
                f"❌ Day {target_day} not found"
            )


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    context = browser.new_context()

    page = context.new_page()

    loop_count = 0

    while True:

        loop_count += 1

        print("\n===================================")
        print(f"STARTING CHECK LOOP #{loop_count}")
        print("===================================\n")

        # Restart browser every 10 loops
        if loop_count % 10 == 0:

            print("\nRestarting browser...\n")

            browser.close()

            browser = p.chromium.launch(
                headless=True
            )

            context = browser.new_context()

            page = context.new_page()

        for circuit, routes in CIRCUITS.items():

            for route in routes:

                try:

                    load_page(page)

                    print("\n========================")
                    print(f"CIRCUIT: {circuit}")
                    print(f"ROUTE: {route}")
                    print("========================")

                    select_circuit(
                        page,
                        circuit
                    )

                    select_route(
                        page,
                        route
                    )

                    ensure_calendar_open(page)

                    go_to_june(page)

                    check_days(
                        page,
                        circuit,
                        route
                    )

                    close_calendar(page)

                    print("\nFinished route.")

                except Exception as e:

                    print("\nERROR:")
                    print(e)

                    try:
                        page.screenshot(
                            path="error.png",
                            full_page=True
                        )
                    except:
                        pass

        print("\n===================================")
        print("CHECK COMPLETE")
        print(
            f"Sleeping {CHECK_INTERVAL_SECONDS} seconds..."
        )
        print("===================================\n")

        time.sleep(CHECK_INTERVAL_SECONDS)