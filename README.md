**Note: this project is discontinued, at least for now. The bot is not functional, but I'm leaving it up in case anyone finds it and wants to use it as a base for their own bot!**

# This is work in progress—the bot doesn't currently work yet!

Clockmaster is a Discord bot that acts as an automatic storyteller for the [Blood on the Clocktower](<https://bloodontheclocktower.com/>) social deduction game. It handles everything for either text or voice-based games (the bot's instructions will always be text-based).

Limitations:
* Madness can't be implemented without a human storyteller (or complex language-processing AI), so it won't be a supported mechanic. Roles that are related to madness will either be adapted or not included.
* Storyteller discretion is replaced by randomness, although chances will rarely be 50-50.
* For now messages are sent in Catalan (it's my language). I want to add localization in the future, though.

Config:
* bot_config_template.json: configuration related to the bot. Rename it to bot_config.json and edit manually.
* game_config.json: game settings, including roles, scripts, and more. Not meant to be edited.
* game_state.json: updated automatically as the game runs. Don't edit manually.