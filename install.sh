#!/bin/sh
# ==========================================================
# Emu Web Panel Automatic Installer for Enigma2
# Developer: Khaled Ali
# ==========================================================

PANEL_URL="https://raw.githubusercontent.com/KhaledAli65/emu/refs/heads/main/emu_panel.py"
INSTALL_PATH="/usr/script/emu_panel.py"
SERVICE_FILE="/etc/systemd/system/emu-panel.service"

echo "=================================================="
echo "      جاري تحميل وتثبيت لوحة إدارة الإيمو...        "
echo "=================================================="

# 1. إيقاف أي نسخة قديمة تعمل حالياً لعدم تعارض البورت
if pgrep -f "emu_panel.py" > /dev/null; then
    echo "[*] إيقاف النسخة القديمة قيد التشغيل..."
    pkill -f "emu_panel.py"
fi

# 2. إنشاء مجلد السكربتات إذا لم يكن موجوداً
mkdir -p /usr/script

# 3. تحميل ملف اللوحة من GitHub بالرابط الخام الصحيح
echo "[*] جاري تحميل ملف اللوحة من GitHub..."
wget -O "$INSTALL_PATH" "$PANEL_URL"

if [ ! -f "$INSTALL_PATH" ]; then
    echo "❌ فشل تحميل الملف. تحقق من الاتصال بالإنترنت."
    exit 1
fi

# 4. إعطاء صلاحية التنفيذ لملف البايثون
chmod +x "$INSTALL_PATH"

# 5. إنشاء وتفعيل خدمة النظام (Systemd Service) للتشغيل الدائم
echo "[*] إعداد خدمة التشغيل الدائم (Daemon)..."
cat << 'EOF' > "$SERVICE_FILE"
[Unit]
Description=Emu Web Panel for Enigma2
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/script/emu_panel.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 6. تحديث وتفعيل الخدمة في النظام
systemctl daemon-reload
systemctl enable emu-panel.service
systemctl restart emu-panel.service

# 7. جلب آيبي الرسيفر بطريقة متوافقة مع BusyBox
IP_ADDR=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d: -f2 | head -n 1)
[ -z "$IP_ADDR" ] && IP_ADDR="IP_الرسيفر"

echo "=================================================="
echo "✅ تم التثبيت والتشغيل الدائم بنجاح!"
echo "🌐 افتح المتصفح وتوجه إلى الرابط التالي:"
echo "   http://$IP_ADDR:8585"
echo "=================================================="
