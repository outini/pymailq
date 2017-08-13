#!/usr/bin/env bash

# Lock postfix transports
echo "default_transport = hold" >> /etc/postfix/main.cf
/etc/init.d/postfix restart

# Generate mails
gen_mail() {
    from=sender-$1
    to=user-$2
    msg="This is test $3"
    sendmail -f $from@testsend_domain.tld \
             -r $from@testsend_domain.tld \
             $to@test-domain.tld <<<$msg
}
for i in `seq 5`; do
    gen_mail 1 1 XXXXXX
    gen_mail 1 2 XX
    echo -n "." && sleep $(($RANDOM%2))
done
for i in `seq 5`; do
    gen_mail 2 1 XXXXXX
    gen_mail 2 3 XX
    echo -n "." && sleep $(($RANDOM%2))
done
for i in `seq 5`; do
    gen_mail 3 2 XXXXXX
    gen_mail 4 3 XX
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
# rm -r /var/spool/postfix/{deferred,defer}
# rsync -rtv tests/samples/spool/postfix/ /var/spool/postfix/
# chown -R postfix:postfix /var/spool/postfix/{deferred,defer}