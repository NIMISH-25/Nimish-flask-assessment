# Bug Report (Flask App)

This report documents the 3 intentional bugs described in the assessment.

---

## Bug #1: Dashboard is accessible without login (and can crash)

**What's broken:**  
`/dashboard` can be opened without being logged in, and it can crash because `email` can be `None`.

**Where:**  
In the original `app.py`, the `dashboard()` route had no auth check and used `email = session.get('email')` LINE-55.

**Why it matters:**  
Functionality and security: unauthenticated users can see a protected page, and the app can throw errors.

**How I fixed it:**  
Added a small `login_required` decorator and applied it to `/dashboard` (and also `/upload` and `/search`). If the user is not logged in or the email is not known, it redirects to `/login`.

**How to test:**  
1. Start the app and open `/dashboard` in an incognito window.  
2. Verify you get redirected to `/login`.  
3. Log in with `test@example.com` / `password123` and verify `/dashboard` loads.

---

## Bug #2: Inefficient file listing (N+1 style pattern)

**What's broken:**  
`/api/files` loops all files, and for each file it does a user lookup. In a real database this pattern becomes very slow.

**Where:**  
In the original `app.py`, `/api/files` did the user lookup inside the loop LINE-76.

**Why it matters:**  
Performance: this scales poorly as file counts grow.

**How I fixed it:**  
Look up the logged in user name once, filter to only the current user’s files, then build the response list.

**How to test:**  
1. Log in.  
2. Call `GET /api/files` and confirm you still get the same file list.
---

## Bug #3: Weak filename validation allows disguised uploads

**What's broken:**  
`/upload` accepts any string containing a dot. A filename like `malware.exe.pdf` passes.

**Where:**  
In the original `app.py`, upload validation only checked `if '.' in filename:` LINE-91.

**Why it matters:**  
Security: it makes it easier to sneak in dangerous file types disguised as “safe” files.

**How I fixed it:**  
Added allowlisted extensions and blocked “double extension” tricks by rejecting dangerous intermediate extensions (example: `exe` in `malware.exe.pdf`). Also normalized the name using `secure_filename`.

**How to test:**  
1. Log in.  
2. Try uploading `malware.exe.pdf` → should return `400 Invalid filename`.  
3. Try uploading `research_paper.pdf` → should be accepted and show up on the dashboard.
