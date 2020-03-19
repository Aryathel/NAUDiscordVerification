# NAU Esports Discord Verification
This bot manages the NAU Esports discord server verification. When a user joins, they are DM'ed a survey.
For more information on how the bot works, each file is well commented.
`main.py` is where the core of the bot is contained, with the majority of the commands and functionality residing in the files in the `Cogs` folder.
The majority of the actual intentioned functionality of this bot lies in the `Welcome.py` file in the `Cogs` folder.
These `Cogs` and the `main` file all pull extra resources (enums, the sheets api, extra functions) from the `Resources` folder.

## Author
This bot was originally written by (Heroicos_HM)[https://github.com/HeroicosHM].

# Setup
For Windows:
  1. Download and install (Python)[https://www.python.org/] (the bot was written in version 3.8.1).
  1. Double click the `Setup.bat` file to run it.
  1. Save your Google Sheets API credentials file in the `Data` folder. (you can create one in Step 1 on (this)[https://developers.google.com/sheets/api/quickstart/python] page)
  1. Edit the `Config.yml` and `Permissions.yml` files.
  1. Double click the `Start.bat` file to run the bot.

For *~nix* Systems (Mac, Linux):
  1. Download and install (Python)[https://www.python.org/] (the bot was written in version 3.8.1).
  1. Double click the `Setup.sh` file to run it.
  1. Save your Google Sheets API credentials file in the `Data` folder. (you can create one in Step 1 on (this)[https://developers.google.com/sheets/api/quickstart/python] page)
  1. Edit the `Config.yml` and `Permissions.yml` files.
  1. Double click the `Start.sh` file to run the bot.

# License
MIT License

Copyright (c) [2020] [Heroicos_HM]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
