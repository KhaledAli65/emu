#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# ==========================================================
# إعدادات السكربت والبورت (عدّل روابط GitHub هنا)
# ==========================================================
PORT = 8585
OSCAM_SCRIPT_URL = "https://raw.githubusercontent.com/KhaledAli65/emu/main/install_oscam.sh"
NCAM_SCRIPT_URL  = "https://raw.githubusercontent.com/KhaledAli65/emu/main/install_ncam.sh"

# مسارات ملفات الإعدادات
PATH_CCCAM_ETC    = "/etc/CCcam.cfg"
PATH_CCCAM_TUXBOX = "/etc/tuxbox/config/CCcam.cfg"
PATH_NCAM_SERVER  = "/etc/tuxbox/config/ncam.server"
PATH_OSCAM_SERVER = "/etc/tuxbox/config/oscam.server"

# تتبع المسار الحالي للتيرمنال داخل الجلسة
CURRENT_CWD = "/home/root" if os.path.exists("/home/root") else "/"
# ==========================================================

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>لوحة إدارة الإيمو والاشتراكات</title>
<style>
  :root {
    --bg-dark: #0f172a;
    --card-bg: #1e293b;
    --card-border: #334155;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --primary: #3b82f6;
    --primary-hover: #2563eb;
    --success: #10b981;
    --success-hover: #059669;
    --purple: #8b5cf6;
    --purple-hover: #7c3aed;
    --amber: #f59e0b;
    --amber-hover: #d97706;
    --danger: #ef4444;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

  body {
    background: radial-gradient(circle at top right, #1e1b4b, var(--bg-dark) 60%);
    color: var(--text-main);
    min-height: 100vh;
    padding: 25px 15px;
  }

  .container {
    max-width: 900px;
    margin: 0 auto;
  }

  .header {
    text-align: center;
    margin-bottom: 30px;
    padding: 25px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  }

  .header h1 {
    font-size: 1.9rem;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
  }

  .header p { color: var(--text-muted); font-size: 0.95rem; }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
  }

  .card-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: #e2e8f0;
    border-bottom: 1px solid var(--card-border);
    padding-bottom: 12px;
  }

  .emu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 15px;
  }

  .btn {
    border: none;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  }

  .btn:hover { transform: translateY(-2px); filter: brightness(1.1); }
  .btn:active { transform: translateY(0); }
  .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

  .btn-oscam { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
  .btn-ncam  { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
  .btn-green { background: linear-gradient(135deg, #10b981, #059669); }
  .btn-teal  { background: linear-gradient(135deg, #0d9488, #0f766e); }
  .btn-amber { background: linear-gradient(135deg, #f59e0b, #d97706); }
  .btn-indigo{ background: linear-gradient(135deg, #4f46e5, #4338ca); }
  .btn-cyan  { background: linear-gradient(135deg, #0284c7, #0369a1); }
  .btn-gray  { background: linear-gradient(135deg, #475569, #334155); }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 18px;
  }

  .input-group { display: flex; flex-direction: column; gap: 6px; }
  .input-group label { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; }

  input, textarea {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px 14px;
    color: #fff;
    font-size: 0.95rem;
    direction: ltr;
    text-align: left;
    transition: border-color 0.2s;
  }

  textarea {
    font-family: 'Courier New', Courier, monospace;
    min-height: 76px;
    resize: vertical;
  }

  input:focus, textarea:focus {
    outline: none;
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
  }

  .quick-line { margin-bottom: 18px; }

  .actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
  }

  .term-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 12px;
  }

  .console-box {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 15px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.88rem;
    color: #34d399;
    min-height: 160px;
    max-height: 360px;
    overflow-y: auto;
    direction: ltr;
    text-align: left;
    white-space: pre-wrap;
    line-height: 1.5;
  }

  .badge {
    font-size: 0.75rem;
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: auto;
  }
</style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>لوحة خدمات الإيمو والسيرفرات</h1>
    <p>تثبيت الإيموهات من GitHub وإدارة ملفات السيسكام والأوسكام والإنكام وتنفيذ أوامر التيرمنال</p>
  </div>

  <!-- قسم تثبيت الإيموهات -->
  <div class="card">
    <div class="card-title">
      <span>🚀 تثبيت الإيموهات (GitHub Scripts)</span>
      <span class="badge">تثبيت تلقائي</span>
    </div>
    <div class="emu-grid">
      <button class="btn btn-oscam" onclick="installEmu('oscam')">
        <span>⚡ تثبيت إيمو OSCam</span>
      </button>
      <button class="btn btn-ncam" onclick="installEmu('ncam')">
        <span>🔥 تثبيت إيمو NCam</span>
      </button>
    </div>
  </div>

  <!-- قسم بيانات الاشتراك -->
  <div class="card">
    <div class="card-title">
      <span>🔑 بيانات اشتراك CCcam</span>
      <span class="badge">تعبئة ذكية</span>
    </div>

    <div class="input-group quick-line">
      <label>لصق سطر السيسكام كاملاً (اختياري - سيقوم بتعبئة الحقول تلقائياً):</label>
      <input type="text" id="raw_cline" placeholder="C: server.example.com 12000 username password" oninput="parseCline(this.value)">
    </div>

    <div class="form-grid">
      <div class="input-group">
        <label>الهوست (Host / Server)</label>
        <input type="text" id="host" placeholder="example.ddns.net">
      </div>
      <div class="input-group">
        <label>البورت (Port)</label>
        <input type="text" id="port" placeholder="12000">
      </div>
      <div class="input-group">
        <label>اسم المستخدم (User)</label>
        <input type="text" id="user" placeholder="user123">
      </div>
      <div class="input-group">
        <label>كلمة المرور (Password)</label>
        <input type="text" id="pass" placeholder="pass123">
      </div>
    </div>

    <div class="actions-grid">
      <button class="btn btn-green" onclick="saveSub('cccam_etc')">
        <span>📄 حفظ في /etc/CCcam.cfg</span>
      </button>
      <button class="btn btn-teal" onclick="saveSub('cccam_tuxbox')">
        <span>📂 حفظ في /etc/tuxbox/config/CCcam.cfg</span>
      </button>
      <button class="btn btn-indigo" onclick="saveSub('ncam_server')">
        <span>🟣 كتابة ريدر في ncam.server</span>
      </button>
      <button class="btn btn-amber" onclick="saveSub('oscam_server')">
        <span>🟠 كتابة ريدر في oscam.server</span>
      </button>
    </div>
  </div>

  <!-- قسم التيرمنال المباشر -->
  <div class="card">
    <div class="card-title">
      <span>💻 تيرمنال الأوامر المباشر (Web Shell)</span>
      <span class="badge" id="cwd_badge">المسار: /home/root</span>
    </div>

    <div class="input-group">
      <label>الصق أمراً واحداً أو عدة أوامر (Enter للتنفيذ السريع، أو Shift+Enter لسطر جديد):</label>
      <textarea id="cmd_input" placeholder="مثال: opkg update && ls -la /etc/tuxbox/config" onkeydown="handleCmdKey(event)"></textarea>
    </div>

    <div class="term-controls">
      <button class="btn btn-cyan" onclick="runShellCmd()">
        <span>▶️ تنفيذ الأمر</span>
      </button>
      <button class="btn btn-gray" onclick="clearConsole()">
        <span>🧹 مسح السجل</span>
      </button>
    </div>
  </div>

  <!-- شاشة السجل والنتائج -->
  <div class="card">
    <div class="card-title">
      <span>🖥️ سجل العمليات (Console Output)</span>
    </div>
    <div class="console-box" id="console">Ready... في انتظار تنفيذ الأوامر.</div>
  </div>
</div>

<script>
  function log(msg, append = false) {
    const box = document.getElementById('console');
    if (append && box.textContent !== 'Ready... في انتظار تنفيذ الأوامر.') {
      box.textContent += '\n' + msg;
    } else {
      box.textContent = msg;
    }
    box.scrollTop = box.scrollHeight;
  }

  function clearConsole() {
    document.getElementById('console').textContent = '';
  }

  function handleCmdKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      runShellCmd();
    }
  }

  function parseCline(val) {
    const clean = val.trim().replace(/^C:\s*/i, '');
    const parts = clean.split(/\s+/);
    if (parts.length >= 4) {
      document.getElementById('host').value = parts[0];
      document.getElementById('port').value = parts[1];
      document.getElementById('user').value = parts[2];
      document.getElementById('pass').value = parts[3];
    }
  }

  function setButtonsDisabled(state) {
    document.querySelectorAll('.btn').forEach(b => b.disabled = state);
  }

  async function installEmu(type) {
    setButtonsDisabled(true);
    log(`⏳ جاري تحميل وتنفيذ سكربت تثبيت ${type.toUpperCase()} من GitHub...\nيرجى الانتظار حتى انتهاء العملية...`);
    try {
      const res = await fetch('/api/install', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ emu: type })
      });
      const data = await res.json();
      log(data.output);
    } catch (e) {
      log('❌ خطأ في الاتصال بالرسيفر: ' + e);
    }
    setButtonsDisabled(false);
  }

  async function saveSub(target) {
    const host = document.getElementById('host').value.trim();
    const port = document.getElementById('port').value.trim();
    const user = document.getElementById('user').value.trim();
    const pass = document.getElementById('pass').value.trim();

    if (!host || !port || !user || !pass) {
      log('⚠️ تنبيه: يرجى ملء جميع الحقول (Host, Port, User, Password) أولاً!');
      return;
    }

    setButtonsDisabled(true);
    log('⏳ جاري كتابة بيانات الاشتراك...');
    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ target, host, port, user, pass })
      });
      const data = await res.json();
      log(data.output);
    } catch (e) {
      log('❌ خطأ في الحفظ: ' + e);
    }
    setButtonsDisabled(false);
  }

  async function runShellCmd() {
    const cmdBox = document.getElementById('cmd_input');
    const cmd = cmdBox.value.trim();
    if (!cmd) {
      log('⚠️ يرجى لصق أو كتابة أمر لتنفيذه.', true);
      return;
    }

    setButtonsDisabled(true);
    log(`$ ${cmd}\n⏳ جاري التنفيذ...`, true);
    try {
      const res = await fetch('/api/exec', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ cmd })
      });
      const data = await res.json();
      if (data.cwd) {
        document.getElementById('cwd_badge').textContent = `المسار: ${data.cwd}`;
      }
      log(data.output, true);
      cmdBox.value = '';
    } catch (e) {
      log('❌ خطأ أثناء تنفيذ الأمر: ' + e, true);
    }
    setButtonsDisabled(false);
  }
</script>
</body>
</html>
"""

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class EmuWebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # إيقاف سجلات الاتصال المزعجة في التيرمينال

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        try:
            payload = json.loads(body)
        except Exception:
            self._send_json({"output": "❌ بيانات غير صالحة"}, 400)
            return

        if self.path == "/api/install":
            emu = payload.get("emu")
            url = OSCAM_SCRIPT_URL if emu == "oscam" else NCAM_SCRIPT_URL
            cmd = f'wget -qO- "{url}" | sh'
            try:
                proc = subprocess.run(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180
                )
                out = proc.stdout.strip() or "✅ تم تنفيذ السكربت بنجاح."
                self._send_json({"output": f"✅ انتهى تثبيت {emu.upper()}:\n\n{out}"})
            except subprocess.TimeoutExpired:
                self._send_json({"output": "⚠️ انتهت مهلة التثبيت (Timeout)."})
            except Exception as e:
                self._send_json({"output": f"❌ حدث خطأ أثناء التثبيت:\n{str(e)}"})

        elif self.path == "/api/save":
            target = payload.get("target")
            host = payload.get("host")
            port = payload.get("port")
            user = payload.get("user")
            passwd = payload.get("pass")

            cline = f"C: {host} {port} {user} {passwd}\n"
            reader_block = (
                f"\n[reader]\n"
                f"label                         = CCcam_{host}\n"
                f"protocol                      = cccam\n"
                f"device                        = {host},{port}\n"
                f"user                          = {user}\n"
                f"password                      = {passwd}\n"
                f"inactivitytimeout             = 30\n"
                f"group                         = 1\n"
                f"cccversion                    = 2.3.2\n"
                f"ccckeepalive                  = 1\n"
                f"audisabled                    = 1\n"
            )

            try:
                if target == "cccam_etc":
                    self._write_file(PATH_CCCAM_ETC, cline, append=False)
                    msg = f"✅ تم حفظ السطر بنجاح في:\n{PATH_CCCAM_ETC}\n\nالمحتوى:\n{cline}"
                elif target == "cccam_tuxbox":
                    self._write_file(PATH_CCCAM_TUXBOX, cline, append=False)
                    msg = f"✅ تم حفظ السطر بنجاح في:\n{PATH_CCCAM_TUXBOX}\n\nالمحتوى:\n{cline}"
                elif target == "ncam_server":
                    self._write_file(PATH_NCAM_SERVER, reader_block, append=True)
                    msg = f"✅ تم إضافة الريدر بنجاح في:\n{PATH_NCAM_SERVER}\n{reader_block}"
                elif target == "oscam_server":
                    self._write_file(PATH_OSCAM_SERVER, reader_block, append=True)
                    msg = f"✅ تم إضافة الريدر بنجاح في:\n{PATH_OSCAM_SERVER}\n{reader_block}"
                else:
                    msg = "❌ مسار غير معروف."

                self._send_json({"output": msg})
            except Exception as e:
                self._send_json({"output": f"❌ فشل الكتابة في الملف:\n{str(e)}"})

        elif self.path == "/api/exec":
            global CURRENT_CWD
            cmd = (payload.get("cmd") or "").strip()
            if not cmd:
                self._send_json({"output": "⚠️ الأمر فارغ.", "cwd": CURRENT_CWD})
                return

            # تشغيل الأمر داخل المجلد الحالي ثم طباعة المجلد الجديد بعد التنفيذ
            wrapped_cmd = f"{cmd}\n__PWD_MARKER__\npwd"
            wrapped_cmd = f"{cmd} ; echo '___CWD___' ; pwd"
            try:
                proc = subprocess.run(
                    wrapped_cmd,
                    shell=True,
                    cwd=CURRENT_CWD if os.path.isdir(CURRENT_CWD) else "/",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=180
                )
                raw_out = proc.stdout or ""
                if "___CWD___" in raw_out:
                    parts = raw_out.rsplit("___CWD___", 1)
                    out_text = parts[0].strip()
                    new_cwd = parts[1].strip().splitlines()[-1].strip() if parts[1].strip() else CURRENT_CWD
                    if os.path.isdir(new_cwd):
                        CURRENT_CWD = new_cwd
                else:
                    out_text = raw_out.strip()

                final_out = out_text if out_text else "✅ تم تنفيذ الأمر (لا يوجد مخرج نصي)."
                self._send_json({"output": final_out, "cwd": CURRENT_CWD})
            except subprocess.TimeoutExpired:
                self._send_json({"output": "⚠️ انتهت مهلة تنفيذ الأمر (180 ثانية).", "cwd": CURRENT_CWD})
            except Exception as e:
                self._send_json({"output": f"❌ خطأ أثناء التنفيذ:\n{str(e)}", "cwd": CURRENT_CWD})
        else:
            self.send_error(404)

    def _write_file(self, filepath, content, append=False):
        folder = os.path.dirname(filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        mode = "a" if append and os.path.exists(filepath) else "w"
        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), EmuWebHandler)
    print(f"Emu Web Panel running on http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
