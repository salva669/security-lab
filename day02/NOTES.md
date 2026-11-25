1. Bandit catches most flows but falis to catch A10, A02 flaws(DEBUG=True, ALLOWED_HOSTS issues and also the SECRET_KEY whih it treats as the password).
Django's own checker although do catch the A02 flaws.

2. A10 flaws are very dangerous in HIS as they may lead to leakage of sensitive info.

3. A01 happens in some workings i have managed on DHIS2 integrations where users were seeing data of other regions which are not theirs.
