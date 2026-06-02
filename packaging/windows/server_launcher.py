import getpass
import os
import socket
import sys
import time
import traceback
import webbrowser
from pathlib import Path


PORT = os.environ.get("PORT", "8000")


def app_data_dir():
    configured = os.environ.get("MUSTANGROUNDUP_DATA_DIR")
    root = Path(configured) if configured else Path(os.environ.get("LOCALAPPDATA", Path.home())) / "MustangRoundup"
    root.mkdir(parents=True, exist_ok=True)
    return root


def local_addresses():
    addresses = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            address = info[4][0]
            if address != "127.0.0.1" and not address.startswith("169.254."):
                addresses.append(address)
    except socket.gaierror:
        pass
    return sorted(set(addresses))


def prompt_for_admin():
    from django.contrib.auth import get_user_model
    from django.core.management import call_command

    User = get_user_model()
    if User.objects.filter(is_staff=True, is_superuser=True).exists():
        return

    print("")
    print("First-time setup: create the administrator login.")
    username = input("Admin username [admin]: ").strip() or "admin"

    while True:
        password_one = getpass.getpass("Admin password, 8+ characters: ")
        password_two = getpass.getpass("Type the admin password again: ")
        if len(password_one) < 8:
            print("Password must be at least 8 characters.")
        elif password_one != password_two:
            print("Passwords did not match.")
        else:
            break

    call_command("ensure_admin", username=username, password=password_one)
    print("Write this username and password down before show day.")


def main():
    data_dir = app_data_dir()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mustangroundupsite.settings")
    os.environ.setdefault("MUSTANGROUNDUP_DATA_DIR", str(data_dir))

    import django
    from django.core.management import call_command, execute_from_command_line

    django.setup()
    call_command("migrate", interactive=False, verbosity=0)
    prompt_for_admin()

    print("")
    print("Mustang Roundup is starting.")
    print("Keep this window open while the show is running.")
    print("")
    print("Operator dashboard on this computer:")
    print(f"  http://127.0.0.1:{PORT}/")
    print("Admin setup:")
    print(f"  http://127.0.0.1:{PORT}/admin/")
    print("")
    print("Judge links for phones on the same Wi-Fi:")
    addresses = local_addresses()
    if addresses:
        for address in addresses:
            print(f"  http://{address}:{PORT}/judge/login/")
    else:
        print("  No local network address was detected yet.")
        print("  Connect this computer to the event Wi-Fi, then restart Mustang Roundup.")
    print("")
    print(f"Event data folder: {data_dir}")
    print("Press Ctrl+C to stop the server after the event.")
    print("")

    if os.environ.get("MUSTANGROUNDUP_NO_BROWSER") != "1":
        time.sleep(1)
        webbrowser.open(f"http://127.0.0.1:{PORT}/")

    execute_from_command_line(
        [
            "MustangRoundup.exe",
            "runserver",
            f"0.0.0.0:{PORT}",
            "--noreload",
        ]
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print("Mustang Roundup stopped.")
    except Exception as exc:
        print("")
        print("Mustang Roundup could not start:")
        print(f"  {exc}")
        print("")
        traceback.print_exc()
        print("")
        try:
            input("Press Enter to close this window.")
        except EOFError:
            pass
        sys.exit(1)
