# Raidware
A C2 Framework developed as an FYP


---

In order to initialize Raidware, you need to firstly run the following command:

```bash
$ sudo python3 raidware.py server
## OR:
$ sudo python3 raidware.py server --host "0.0.0.0" --port 42560
```

Then, in another terminal, you need to run the following command:
```bash
$ sudo python3 raidware.py cli <username> <password> <team_password>
```
This command will let you use Raidware's powerful CLI.

Although, in order to use it, you must firstly create a new account. A default account with the credentials `raidware:raidware` has been provided. Although, if you want to create your own, you can use the endpoint '/register' with the following parameters:
```bash
$ curl -X POST -d "username=<username>&password=<password>&team_password=<team_password>" http://localhost:42560/v1/register
```
The valid response would be:

```json
{"status": "success", "message": "Account created successfully"}
```
Errors may include:
```json
{"status": "failed", "message": "The user <username> already exists."}
{"status": "failed", "message": "The team password is incorrect."}
{"status": "failed", "message": "Weak password"}
```