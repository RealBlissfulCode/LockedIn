set -u
cd /home/user/lockedin
reset(){ php -r 'require "api/boot.php"; q("SET FOREIGN_KEY_CHECKS=0");
  foreach(["doc_history","docs","invites","members","sessions","households","accounts"] as $t){
    try{ q("DELETE FROM $t"); }catch(Throwable $e){} }
  q("SET FOREIGN_KEY_CHECKS=1");' 2>/dev/null; }
for t in apitest.sh reorder-test.py charts-test.py modaldrag-test.py overlap-test.py alignment-test.py sectionio-test.py \
         planroads-test.py everysection-test.py allsections-test.py dataloss-test.py \
         twodevice-test.py livesync-test.py daysync-test.py household-test.py \
         offline-test.py nohistory-test.py; do
  php api/migrate.php >/dev/null 2>&1
  reset
  echo "##### $t"
  if [ "${t##*.}" = sh ]; then timeout 600 bash tools/$t 2>&1 | grep -iE "^FAIL|FAILURES|^passed|failed|MISALIGNED|PROBLEMS|Traceback|Error:" | head -8
  else timeout 900 python3 -u tools/$t 2>&1 | grep -iE "^FAIL|FAILURES|^passed|MISALIGNED|PROBLEMS|Traceback|Error:" | head -8; fi
done
php api/migrate.php >/dev/null 2>&1
echo "##### sweep done"
