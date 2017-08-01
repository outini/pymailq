#!/usr/bin/env bash

# Lock postfix transports
echo "default_transport = hold" >> /etc/postfix/main.cf
/etc/init.d/postfix restart

# Generate mails
for i in `seq 30`; do
from=sender-$(($RANDOM%10))
to=user-$(($RANDOM%10))
sendmail -f $from@testsend_domain.tld \
         -r $from@testsend_domain.tld \
         $to@test-domain.tld <<<"This is test $RANDOM"""
echo -n "." && sleep $(($RANDOM%2))
done

# Modify error messages
for mail in `find /var/spool/postfix/defer/ -type f` ; do
sed -i "s/reason=.*/reason=Error message number $(($RANDOM%9))/" "$mail"
done

# Once samples has been generated, you can save those to tests/samples
# directory. Don't forget to adapt tests result with your newly generated
# samples.
#
# You may deploy samples with the following commands
# rsync -rtv tests/samples/spool/postfix/ /var/spool/postfix/
# chown -R postfix:postfix /var/spool/postfix/{deferred,defer}