#!/bin/sh
# ==========================================================
# Emu Web Panel Automatic Installer for Enigma2
# Developer: Khaled Ali
# ==========================================================

PANEL_URL="https://raw.githubusercontent.com/KhaledAli65/emu/main/emu_panel.py"
INSTALL_PATH="/usr/script/emu_panel.py"

echo "=================================================="
echo "      جاري تحميل وتثبيت لوحة إدارة الإيمو...        "
echo "=================================================="

# 1. إيقاف أي نسخة قديمة تعمل حالياً
if pgrep -f "emu_panel.py" > /dev/null; then
    echo "[*] إيقاف النسخة القديمة قيد التشغيل..."
    pkill -f "emu_panel.py"
fi

# 2. إنشاء مجلد السكربتات إذا لم يكن موجوداً
mkdir -p /usr/script

# 3. تحميل ملف اللوحة من GitHub
echo "[*] جاري تحميل ملف اللوحة..."
wget -O "$INSTALL_PATH" "$PANEL_URL"

if [ ! -f "$INSTALL_PATH" ]; then
    echo "❌ فشل تحميل الملف من GitHub. تحقق من الرابط أو الاتصال بالإنترنت."
    exit 1
fi

# 4. إعطاء صلاحية التنفيذ
chmod +x "$INSTALL_PATH"

# 5. ضبط التشغيل التلقائي مع الإقلاع (rc.local)
RC_FILE="/etc/rc.local"
if [ ! -f "$RC_FILE" ]; then
    echo -e "#!/bin/sh\npython3 $INSTALL_PATH &\nexit 0" > "$RC_FILE"
    chmod +x "$RC_FILE"
else
    # إضافة السطر إذا لم يكن موجوداً مسبقاً
    if ! grep -q "emu_panel.py" "$RC_FILE"; then
        sed -i '/^exit 0/i python3 ' "$INSTALL_PATH" ' &' "$RC_FILE" || echo "python3 $INSTALL_PATH &" >> "$RC_FILE"
    fi
fi

# 6. تشغيل اللوحة في الخلفية فوراً
python3 "$INSTALL_PATH" &

# 7. جلب آيبي الرسيفر وعرض رسالة النجاح
IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="IP_الرسيفر"

echo "=================================================="
echo "✅ تم التثبيت والتشغيل بنجاح!"
echo "🌐 افتح المتصفح وتوجه إلى الرابط التالي:"
echo "   http://$IP_ADDR:8585"
echo "=================================================="
