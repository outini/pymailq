# Testing PyMailq module

Tests require a local installation of postfix and a set of generated mails. Those tests cover both pymailq core module and shell features.

## Preparing local system

Install postfix and configure it to block any mail deliveries (mails are immediatly set as deferred) with a deferred transport. Then inject some mails samples, below is an example of postfix installation and configuration.

```sh
apt-get update -qq
sudo apt-get install -qq postfix
echo "default_transport = hold" >> /etc/postfix/main.cf &&
/etc/init.d/postfix restart
```

A [sample generator](https://github.com/outini/pymailq/blob/master/tests/generate_samples.sh) is provided to fill postfix queue with proper mails for testing. This script will also check your postfix installation and ensure no mail is deliver by adding the _default_transport_ directive if necessary. It should run as root (read it first).

```sh
./tests/generate_samples.sh
```

## Preparing python virtualenvs

Tests require some external python module, you may use the provided [requirements file](https://github.com/outini/pymailq/blob/master/tests/tests.requirements.txt) to prepare your environnment. Pymailq supports both Python 2.7 and Python 3+ versions, don't forget to create multiple environnement to properly test it.

```sh
pip install -r tests/tests.requirements.txt
```

Quick method for those using [pew](https://pypi.python.org/pypi/pew/):
```sh
pew new -ppython2.7 -i "ipython<6" -d pymailq_27
pew in pymailq_27 pip install -r tests/tests.requirements.txt
```
```sh
pew new -ppython3 -d pymailq_3
pew in pymailq_3 pip install -r tests/tests.requirements.txt
```

## Running tests

Tests are based on the [py.test](https://docs.pytest.org) module. Run those in your virtualenv. Don't forget to generate samples before each run (tests end with mails deletion).

```sh
PYTHONPATH=. pytest tests/
```

For those using [pew](https://pypi.python.org/pypi/pew/):

```sh
sudo ./tests/generate_samples.sh &&
PYTHONPATH=. pew in pymailq_27 pytest tests/
```
```sh
sudo ./tests/generate_samples.sh &&
PYTHONPATH=. pew in pymailq_3 pytest tests/
```

Tests are also used for code coverage. The python module [coverage](https://coverage.readthedocs.io) is already declared in the [requirements file](https://github.com/outini/pymailq/blob/master/tests/tests.requirements.txt) and should be installed in your virtualenv.

```sh
PYTHONPATH=. coverage run --source=pymailq/ -m py.test tests/
coverage xml
coverage html
```

The _xml_ file is mostly used to upload your coverage date to some sites like [Codacy](https://www.codacy.com) and its creation may be skipped. Coverage produces an html report to help you check your uncovered code.

```sh
xdg-open htmlcov/index.html
```
