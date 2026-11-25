1. Bandit catches most flows(Injections, SQL XSS, shell), MD5 and hardcoded secrets but falis to catch A10(fail-open auth,error leakage), A02 flaws(DEBUG=True, ALLOWED_HOSTS issues and also the SECRET_KEY whih it treats as the password) and A01 (IDOR in patient_record).
Django's own checker although do catch the A02 flaws.
SAST sees dangerous calls in functions but not the missing logic

2. A10 flaws are very dangerous in HIS as they may lead to leakage of sensitive info.
A fail-open excet turns any error into an access-control bypass

3. A01 happens in some workings i have managed on DHIS2 integrations where users were seeing data of other regions which are not theirs. 
This happended in a custom App implementation.
