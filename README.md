# Rising Mod
Legacy Discord bot focused on moderation and user engagement, originally created for Rising Hub's (https://risinghub.net) Discord server.

**Beware**: This project uses an ancient Python lib that very likely does not work, or even exist anymore.

# settings.json
All of the settings below must be filled for the bot to work correctly. It probably won't start at all if you miss any...

`prefix`: The prefix you'd like to use. It can be a list of prefixes or just one.
`rpctype`: Status type. Must be an integer between 0 and 3. Controls whether the status is "Playing", "Watching", "Listening", etc.

```
{
    "token": "Your Discord bot's token.",
    "botid": "Your bot's user ID.",
    "server": "Your server's ID.",
    "prefix": ["~","-"],
    "status": "Your status message.",
    "welcome_message": "Message sent to server newcomers.",
    "muted": "Your muted role ID.",
    "announcement_channel": "Channel where bot's ready message is sent.",
    "alerts_channel": "Channel ID where you want the bot to send the alerts.",
    "filter_channel": "Channel ID where you want the bot to send chat filter alerts.",
    "suggestions_channel": "Channel ID where you want the bot to log user suggestions.",
    "bugs_channel": "Channel ID where you want the bot to send bug reports.",
    "votebans_channel": "Channel ID where vote bans are created.",
    "votebanslog_channel": "Channel ID where private vote bans logs are stored.",
    "rpctype": 3
}
```

