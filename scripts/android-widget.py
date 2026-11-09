# Junta o widget "Leitura · Para ti" ao projeto Android gerado pelo Tauri.
import glob, os, re, shutil
base = 'src-tauri/gen/android/app/src/main'
act = glob.glob(f'{base}/java/**/MainActivity.kt', recursive=True)[0]
pkg = re.search(r'^package\s+([\w.]+)', open(act).read(), re.M).group(1)
# 1) código Kotlin do widget, no mesmo pacote da MainActivity
src = open('android/HeadlinesWidget.kt').read().replace('__PACKAGE__', pkg)
open(os.path.join(os.path.dirname(act), 'HeadlinesWidget.kt'), 'w').write(src)
# 2) recursos (layout, fundo, configuração)
for f in glob.glob('android/res/**/*.xml', recursive=True):
    dst = os.path.join(base, 'res', os.path.relpath(f, 'android/res'))
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(f, dst)
strings = f'{base}/res/values/strings.xml'
s = open(strings).read()
if 'widget_description' not in s:
    s = s.replace('</resources>', '    <string name="widget_description">As notícias mais relevantes para ti</string>\n</resources>')
    open(strings, 'w').write(s)
# 3) registar o widget no AndroidManifest
man = f'{base}/AndroidManifest.xml'
m = open(man).read()
if 'HeadlinesWidget' not in m:
    rec = '''        <receiver android:name=".HeadlinesWidget" android:exported="false" android:label="Leitura">
            <intent-filter><action android:name="android.appwidget.action.APPWIDGET_UPDATE" /></intent-filter>
            <meta-data android:name="android.appwidget.provider" android:resource="@xml/headlines_widget_info" />
        </receiver>
    </application>'''
    m = m.replace('</application>', rec, 1)
    open(man, 'w').write(m)
# 4) atualizar o widget sempre que o app vai para segundo plano
a = open(act).read()
if 'onPause' not in a:
    method = '''
    override fun onPause() {
        super.onPause()
        try { HeadlinesWidget.refresh(this) } catch (e: Exception) { }
    }
'''
    if re.search(r'class MainActivity\s*:\s*TauriActivity\(\)\s*\{', a):
        a = a[:a.rstrip().rfind('}')] + method + '}\n'
    else:
        a = re.sub(r'class MainActivity\s*:\s*TauriActivity\(\)\s*$', 'class MainActivity : TauriActivity() {' + method + '}', a, flags=re.M)
    open(act, 'w').write(a)
print('Widget adicionado ao pacote', pkg)
print(open(act).read())
