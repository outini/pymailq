#!/usr/bin/env bash

# This script need some root privileges to cleanup mails queue
# or reconfigure and restart mail service.

# You may use this script followed by pytest to generate a bunch of test mails.
# Wait few seconds after the sample generation to let postfix stabilize his
# queue, this is useful when generating thousand of mails.
# sudo ./tests/generate_samples.sh
# PYTHONPATH=. pytest -v tests/

# Cleanup all queued mails
echo "cleaning queued messages."
postsuper -d ALL

# Sleep few seconds to let postfix cleanup his queue.
# sleep 3

# Lock postfix transports
echo "checking postfix configuration."
grep -q "default_transport" /etc/postfix/main.cf || {
    echo "reconfiguration of postfix."
    echo "default_transport = hold" >> /etc/postfix/main.cf &&
    /etc/init.d/postfix restart
}

# Generate mails
msg() { printf "This is test.\n%$1s\n"; }
gen_mail() {
    sendmail -f "sender-$1@test-domain.tld" \
             -r "sender-$1@test-domain.tld" \
             "user-$2@test-domain.tld" <<<"$3"
}

echo -n "injecting test mails "
(for i in `seq 50`; do gen_mail 1 1 "`msg 1000`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 1 2 "`msg 10`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 2 1 "`msg 1000`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 2 3 "`msg 10`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 3 2 "`msg 1000`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 4 3 "`msg 10`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 5 2 "`msg 1000`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 6 3 "`msg 10`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 7 2 "`msg 1000`"; done; echo -n ".") &
(for i in `seq 50`; do gen_mail 8 3 "`msg 10`"; done; echo -n ".") &
wait
echo " done."

# Checks that mails queue is stabilized before proceeding further
echo "waiting for queue stabilization."
while [ `sendmail -bp | grep -c '^[A-F0-9]'` -ne 500 ]; do
    sleep 1
done
echo "generated `sendmail -bp | grep -c '^[A-F0-9]'` emails."

# Modify error messages
echo "setting error messages."
i=0
for mail in `find /var/spool/postfix/defer/ -type f` ; do
    if [ $i -le 15 ]; then
        sed -i "s/reason=.*/reason=Test error message/" "$mail"
    else
        break
    fi
    ((i++))
done
