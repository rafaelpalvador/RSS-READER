# Liga a assinatura da APK ao projeto Android gerado pelo Tauri.
# A chave vem de keystore.properties (criado no workflow).
import re, sys
p = 'src-tauri/gen/android/app/build.gradle.kts'
s = open(p).read()
if 'signingConfigs' in s:
    sys.exit(0)
if 'import java.io.FileInputStream' not in s:
    s = 'import java.io.FileInputStream\n' + s
block = '''
    signingConfigs {
        create("release") {
            val keystorePropertiesFile = rootProject.file("keystore.properties")
            val keystoreProperties = Properties()
            if (keystorePropertiesFile.exists()) {
                keystoreProperties.load(FileInputStream(keystorePropertiesFile))
            }
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["password"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["password"] as String
        }
    }
'''
s = re.sub(r'android \{\n', 'android {\n' + block, s, count=1)
s = re.sub(r'(getByName\("release"\) \{\n)', r'\1            signingConfig = signingConfigs.getByName("release")\n', s, count=1)
if 'java.util.Properties' not in s:
    s = 'import java.util.Properties\n' + s
open(p, 'w').write(s)
print('Assinatura configurada')
