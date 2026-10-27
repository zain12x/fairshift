from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="FairShift - Decent Work Platform")

SHIFTS = [
    {"worker_id": "W-101", "name": "Ravi Kumar", "sector": "Construction", "hours": 9.5, "base_pay": 800, "overtime_pay": 225},
    {"worker_id": "W-102", "name": "Meena S", "sector": "Campus Facility", "hours": 11.5, "base_pay": 720, "overtime_pay": 380}
]

HAZARDS = [
    {"id": 1, "sector": "Construction", "desc": "Unsecured scaffolding at Block B", "status": "Under Review"},
    {"id": 2, "sector": "Campus Facility", "desc": "Slippery spill near canteen kitchen", "status": "Resolved"}
]

@app.get("/", response_class=HTMLResponse)
def landing():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>FairShift - SDG 8</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100 min-h-screen p-6 flex items-center justify-center font-sans">
      <div class="max-w-md w-full bg-white p-6 rounded-2xl shadow-lg space-y-6">
        <header class="text-center">
          <span class="text-xs uppercase tracking-wider bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-semibold">UN SDG 8</span>
          <h1 class="text-2xl font-bold text-slate-800 mt-3">FairShift Platform</h1>
          <p class="text-xs text-gray-500 mt-1">Decent work, wage transparency & worker safety</p>
        </header>
        <div class="space-y-3">
          <a href="/worker" class="block w-full text-center py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 shadow">👷 Worker Portal (Mobile UI)</a>
          <a href="/admin" class="block w-full text-center py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 shadow">🏢 Employer Admin Dashboard</a>
        </div>
      </div>
    </body>
    </html>
    """

@app.get("/worker", response_class=HTMLResponse)
def worker_view():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>FairShift - Worker</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 min-h-screen p-4 font-sans">
      <div class="max-w-md mx-auto space-y-4">
        <header class="bg-blue-600 text-white p-4 rounded-xl flex justify-between items-center shadow">
          <div>
            <h1 class="text-lg font-bold">Worker Portal</h1>
            <p class="text-xs text-blue-100">Language: English / தமிழ் / हिंदी</p>
          </div>
          <a href="/" class="text-xs bg-blue-800 px-3 py-1 rounded">Home</a>
        </header>

        <div class="bg-white p-4 rounded-xl shadow border border-slate-200 space-y-3">
          <h2 class="text-sm font-bold text-gray-800">Current Shift: Construction Site A</h2>
          <div class="text-xs space-y-1 text-gray-600">
            <div class="flex justify-between"><span>Base Pay (8 hrs):</span><span>₹800</span></div>
            <div class="flex justify-between"><span>Overtime Pay (1.5 hrs):</span><span class="text-green-600 font-semibold">+₹225</span></div>
            <hr class="my-1">
            <div class="flex justify-between font-bold text-gray-900 text-sm"><span>Total Earned:</span><span>₹1,025</span></div>
          </div>
          <span class="inline-block text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-medium">Verified by Site QR</span>
        </div>

        <div class="bg-white p-4 rounded-xl shadow border border-slate-200 space-y-3">
          <h2 class="text-sm font-bold text-gray-800">⚠️ Anonymous Hazard Report</h2>
          <form action="/report-hazard" method="post" class="space-y-3">
            <div>
              <label class="block text-xs text-gray-500 mb-1">Workplace Sector</label>
              <select name="sector" class="w-full border p-2 rounded text-xs bg-gray-50">
                <option value="Construction">Construction Site</option>
                <option value="Campus Facility">Campus Facility</option>
              </select>
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">Incident or Safety Hazard</label>
              <textarea name="desc" rows="3" placeholder="Describe the hazard or risk..." class="w-full border p-2 rounded text-xs" required></textarea>
            </div>
            <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-white font-bold py-2 rounded-lg text-xs">Submit Anonymous Report</button>
          </form>
        </div>
      </div>
    </body>
    </html>
    """

@app.post("/report-hazard")
def submit_hazard(sector: str = Form(...), desc: str = Form(...)):
    HAZARDS.append({"id": len(HAZARDS) + 1, "sector": sector, "desc": desc, "status": "Under Review"})
    return HTMLResponse("<script>alert('Hazard submitted anonymously.'); window.location.href='/worker';</script>")

@app.get("/admin", response_class=HTMLResponse)
def admin_view():
    shift_rows = []
    for s in SHIFTS:
        if s['hours'] > 10:
            badge = "<span class='text-red-600 font-bold bg-red-50 px-2 py-0.5 rounded'>Fatigue Risk</span>"
        else:
            badge = "<span class='text-green-700 bg-green-50 px-2 py-0.5 rounded'>Normal</span>"
        shift_rows.append(f"<tr class='border-b text-xs'><td class='py-2'>{s['worker_id']} ({s['name']})</td><td>{s['sector']}</td><td>{s['hours']} hrs</td><td>{badge}</td></tr>")
    
    rendered_shifts = "".join(shift_rows)

    hazard_rows = [
        f"<li class='p-2 bg-slate-50 border rounded text-xs'><strong>[{h['sector']}]</strong> {h['desc']} — <span class='text-blue-600 font-medium'>{h['status']}</span></li>"
        for h in HAZARDS
    ]
    rendered_hazards = "".join(hazard_rows)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>FairShift - Admin</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100 min-h-screen p-6 font-sans">
      <div class="max-w-4xl mx-auto space-y-6">
        <header class="bg-slate-800 text-white p-4 rounded-xl flex justify-between items-center shadow">
          <div>
            <h1 class="text-xl font-bold">Employer Workforce Health Dashboard</h1>
            <p class="text-xs text-gray-300">Sectors: Construction & Campus Facility Operations</p>
          </div>
          <a href="/" class="text-xs bg-slate-700 px-3 py-1 rounded">Switch Role</a>
        </header>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white p-4 rounded-xl shadow border space-y-3">
            <h2 class="text-sm font-bold text-gray-700">Attendance & Fatigue Tracker</h2>
            <table class="w-full text-left">
              <thead><tr class="border-b text-xs text-gray-500"><th class="pb-2">Worker</th><th>Sector</th><th>Hours</th><th>Status</th></tr></thead>
              <tbody>{rendered_shifts}</tbody>
            </table>
          </div>
          <div class="bg-white p-4 rounded-xl shadow border space-y-3">
            <h2 class="text-sm font-bold text-gray-700">Anonymous Safety Hazard Triage</h2>
            <ul class="space-y-2">{rendered_hazards}</ul>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
