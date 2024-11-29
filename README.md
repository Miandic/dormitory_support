# dormitory-support
Support bot to create and answer tickets. Uses database to store tickets, sort them by category in admin panel. 

User can run main menu with */start* command, then pick category of questions and type it. If he confirms his ticket, question goes to db and notifications are sended to admins, else user statrs process again. 

Administratos can check active tickets, get link to telegram account of user who sended it and close tickets after they done.

#### To start run bot_run.py 

## requirements
> aiogram
>
> asyncio
>
> python-decouple
>
> asyncpg_lite

also you need to create .env file with API token and admin ID

### .env file structure
```
TOKEN=<your telegram bot API token here>
ADMINS=<user ID, user ID, ...>
BLACKLIST=<user ID, user ID, ...>
PG_LINK=postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName
ROOT_PASS=<Server root password>
```


## To do:
- [ ] Add admins from admin menu
- [ ] Ban users from admin menu
- [ ] Subscribe / unsubscribe from notifications by category
- [ ] Anonymous questions category with timeout by id
- [ ] Closed tickets history
- [ ] Some interface tweaks (better syntax, text highlighting, emoji, etc)  
- [ ] Integrate AI to analyse ticket and suggest quick answer (need to create prompt with basic knowledge before)