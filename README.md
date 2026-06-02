# Mustang Roundup

Mustang Roundup is a local car-show judging app. One Windows laptop runs the
show server. Judges connect their phones to the same Wi-Fi network and use a
normal mobile browser. Internet access is not required during the event.

## Plain-English Setup

For a non-technical show operator, the goal is this:

1. Download `MustangRoundup-Setup.exe`.
2. Double-click it.
3. Use the `Mustang Roundup` desktop shortcut.

The installer is not code-signed, so Windows may show a SmartScreen warning.
That is expected for a small unsigned app. The operator can click `More info`
and then `Run anyway`.

The older PowerShell setup path is still documented below as a fallback for
developers or helpers.

## What You Need

- A Windows 10 or Windows 11 laptop.
- A Wi-Fi network that the laptop and judges' phones can all join.
- A power outlet or battery plan for the laptop.
- Printed judge PINs or a way to hand them to judges.

A dedicated travel router is strongly recommended for an event. It is more
reliable than depending on weak cell service or a laptop hotspot.

## Public Or Internet Deployment Safety

The Windows launcher and PowerShell start scripts are for a trusted local event
network. They intentionally expose the judge pages on the laptop's Wi-Fi
address so phones can connect.

Do not expose the local `runserver` workflow directly to the internet. For a
public hosted deployment, run behind HTTPS with a production web server and set
these environment variables:

```text
MUSTANGROUNDUP_LOCAL_EVENT_MODE=0
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=<long random secret>
DJANGO_ALLOWED_HOSTS=<your-hostname>
DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-hostname>
```

If every subdomain for that hostname is HTTPS-only and you want HSTS preload
eligibility, also set:

```text
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=1
DJANGO_SECURE_HSTS_PRELOAD=1
```

Use non-obvious judge PINs and change them between events. The app throttles
repeated failed PIN attempts, but short or reused PINs are still weak on a
public network.

## Easiest Install For The Show Operator

Use this section for the person running the show.

### 1. Download The Installer

Download:

```text
MustangRoundup-Setup.exe
```

Only download the installer from the project owner or the official GitHub
release page.

### 2. Run The Installer

1. Double-click `MustangRoundup-Setup.exe`.
2. If Windows shows a blue SmartScreen warning, click `More info`.
3. Click `Run anyway`.
4. Follow the installer prompts.
5. Leave `Create a desktop shortcut` checked.

The installer creates:

- a Start Menu shortcut named `Mustang Roundup`;
- a desktop shortcut named `Mustang Roundup`;
- an app data folder for the event database.

### 3. Start Mustang Roundup

Double-click the `Mustang Roundup` desktop shortcut.

A black server window opens. Keep that window open while the show is running.
The app will also open the operator dashboard in the browser.

On first run, the app asks you to create the administrator login. Write that
username and password down.

The server window prints judge links for phones on the same Wi-Fi, such as:

```text
http://192.168.50.10:8000/judge/login/
```

Use that link for judges. Do not give judges the `127.0.0.1` link.

## Manual Windows Setup Fallback

Use this section only if you do not have the installer.

### 1. Install Python

The manual setup requires Python. The normal installer above does not require
the operator to install Python separately.

1. Go to https://www.python.org/downloads/
2. Download Python 3.12 for Windows.
3. Start the installer.
4. Check the box named `Add python.exe to PATH`.
5. Click `Install Now`.

### 2. Put The App On The Laptop

Copy or unzip the `mustang-roundup` folder onto the show laptop. A simple place
is:

```text
C:\MustangRoundup
```

### 3. Open PowerShell In The App Folder

1. Open the `mustang-roundup` folder in File Explorer.
2. Hold `Shift`.
3. Right-click in the empty space inside the folder.
4. Choose `Open PowerShell window here` or `Open in Terminal`.

### 4. Run The Setup Script

In PowerShell, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

The setup script will:

- create a local Python environment;
- install the app requirements;
- prepare the local SQLite database;
- ask you to create an admin username and password.

Write down the admin username and password. You will need them to set up the
show.

## Starting The App

If you installed with `MustangRoundup-Setup.exe`, use the desktop shortcut.

If you are using the manual folder setup, open PowerShell in the app folder and
run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-server.ps1
```

Keep the server window open while the show is running. Closing it stops the
server.

The script prints links like these:

```text
Operator dashboard on this computer:
  http://127.0.0.1:8000/

Admin setup:
  http://127.0.0.1:8000/admin/

Judge links for phones on the same Wi-Fi:
  http://192.168.50.10:8000/judge/login/
```

Use `127.0.0.1` only on the laptop. Judges' phones must use the local network
address, usually something like `192.168.x.x`.

## Creating A Show

Open the admin page on the laptop:

```text
http://127.0.0.1:8000/admin/
```

Sign in with the admin username and password you created during setup.

Create records in this order:

1. `Shows`
2. `Divisions`
3. `Classes`
4. `Categories`
5. `Cars`
6. `Judges`
7. `Judge assignments`

### Shows

A show is the event itself. Set:

- name;
- date;
- location;
- status.

Use these statuses:

- `Setup`: before judging starts.
- `Open for judging`: judges can log in and submit scores.
- `Judging closed`: judges can no longer submit scores.
- `Finalized`: event is complete.

### Divisions And Classes

Use divisions and classes to organize cars.

Example:

```text
Division: Classic
Class: 1964-1973
Class: 1974-1993

Division: Modern
Class: 1994-2004
Class: 2005-Present
```

### Categories

Categories are the things judges score.

Example:

```text
Exterior, max score 10
Interior, max score 10
Engine, max score 10
```

### Cars

Each car needs:

- entry number;
- owner name;
- year, make, model, and trim;
- class.

Entry numbers must be unique inside the show.

### Judges

Each judge needs:

- name;
- PIN;
- active checkbox.

The PIN is what the judge enters on their phone. Keep PINs simple enough to type
but not obvious to the public.

### Judge Assignments

Assignments control what each judge can score.

You can assign a judge to:

- a whole division;
- one class;
- one category;
- or a combination.

If a judge has no assignments, the judge can score all cars and all categories
for the show.

## Day-Of Event Checklist

1. Turn on the travel router or event Wi-Fi.
2. Connect the laptop to that Wi-Fi.
3. Start the app from the `Mustang Roundup` desktop shortcut.

If you used the manual setup instead, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-server.ps1
```

4. Open the operator dashboard:

```text
http://127.0.0.1:8000/
```

5. Confirm the show is set to `Open for judging`.
6. Give judges the Wi-Fi name and password.
7. Give judges the judge link printed by the start script.
8. Give each judge their PIN.
9. Watch the dashboard for submitted and missing scores.
10. Close judging when scoring is complete.
11. Export results.
12. Back up the database.

## Judge Instructions

Give judges these instructions:

1. Join the event Wi-Fi.
2. Open the judge link on your phone.
3. Enter your judge PIN.
4. Tap a car.
5. Enter scores.
6. Tap `Save Draft` if you are not finished.
7. Tap `Submit Final` when the score is complete.
8. Return to the judge dashboard and continue with the next car.

Judges do not need cell service or internet access. They only need to be on the
same Wi-Fi network as the laptop.

## Operator Dashboard

Open:

```text
http://127.0.0.1:8000/
```

The dashboard shows:

- number of cars;
- number of judges;
- number of categories;
- submitted scores;
- draft scores;
- missing scores;
- recent judge activity.

The dashboard also lets you:

- change show status;
- show or hide public results;
- open setup/admin;
- export CSV results.

## Results

Open:

```text
http://127.0.0.1:8000/results/
```

Public results are hidden unless `Public standings` is turned on for the show.
Staff users can preview results even while public results are hidden.

To export:

```text
http://127.0.0.1:8000/results.csv
```

The CSV includes class, place, entry number, owner, vehicle, total score, and
number of submitted scores.

## Diagnostics And QR Code

Open:

```text
http://127.0.0.1:8000/diagnostics/
```

This page shows:

- the judge login URL;
- QR code for judge login;
- local IP addresses;
- database path;
- a database backup button.

If judges cannot connect, this page is the first place to check.

## Backing Up The Event

From the diagnostics page, click `Backup Database`.

Backups are saved in:

```text
backups
```

The main event database is:

```text
db.sqlite3
```

After the show, copy the `backups` folder or `db.sqlite3` to a USB drive or cloud
storage.

## Stopping The App

Go to the black server window or PowerShell window running the server and press:

```text
Ctrl+C
```

Wait for it to stop, then close the window.

## Testing With Demo Data

For a quick test event, run:

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo
```

The demo judge PIN is:

```text
1234
```

Do not use the demo show as your real event unless you have edited it for the
actual show.

## Troubleshooting

### The Browser Says "127.0.0.1 Refused To Connect"

The server is not running. Start it again from the `Mustang Roundup` desktop
shortcut.

If you are using the manual setup, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-server.ps1
```

### Judges Cannot Open The Link

Check these items:

- The laptop and phones are on the same Wi-Fi network.
- The phones are using the `192.168.x.x` style link, not `127.0.0.1`.
- Windows Firewall allowed Python when prompted.
- The PowerShell server window is still open.
- The laptop did not go to sleep.

### Windows Firewall Asks About Python

Choose `Allow access`. The app needs permission so phones on the local Wi-Fi can
reach the laptop.

If the installed app asks, the name may be `MustangRoundup.exe` instead of
Python.

### I Forgot The Admin Password

Open PowerShell in the app folder and run:

```powershell
.\.venv\Scripts\python.exe manage.py ensure_admin --username admin --password NewPassword123
```

Then sign in with:

```text
Username: admin
Password: NewPassword123
```

### The Laptop Changed IP Address

Restart the start script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-server.ps1
```

Use the new judge link printed by the script.

### Scores Look Incomplete

Check:

- show status is `Open for judging`;
- judges are active;
- judge assignments are correct;
- each car has the correct class;
- each category belongs to the correct show.

## Developer Notes

For development:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver 127.0.0.1:8000
```

The app is intentionally local-first:

- Django 5.2 LTS;
- SQLite database;
- server-rendered pages;
- phone-friendly judge forms;
- local backup and CSV export;
- small PWA shell for cached assets.

## Building The One-File Windows Installer

This section is for the project owner, not the show operator.

The normal handoff artifact should be:

```text
MustangRoundup-Setup.exe
```

It is an unsigned installer. Without a paid code-signing certificate, Windows
SmartScreen may warn the operator. That is expected. Tell the operator to use
`More info` and `Run anyway`.

### Build In GitHub

Push this branch to GitHub. The workflow at:

```text
.github/workflows/windows-installer.yml
```

builds and uploads `MustangRoundup-Setup.exe` as a GitHub Actions artifact.

### Build Locally On Windows

Install Inno Setup 6, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\packaging\windows\build-installer.ps1
```

The installer is created at:

```text
dist\installer\MustangRoundup-Setup.exe
```

If Inno Setup is not installed, the script creates a portable zip instead.
