	  TITLE DuckyObfuscator
      AUTHOR Chaos.Reigns.All
      DESCRIPTION Python app for "encoding" a string of 0-9, a-z, A-Z characters into an payload.txt for badUSB execution on a flipper as a physical PW manager.

# DuckyObfuscator
I made a quick python app that takes a string of characters up to 128 characters and turns them into a flipper payload.txt written in duckyscript as individual ducky strings and some slightly humorous REM comment phrases to slightly obscure your password to be used on a flipperzero to autotype that string or one based on it directly into a field where you prefer not type it due to legnth/complexity or 

--0-128 bit string Input--  
Accepts any string 0-128 characters includes 0-9, a-z, A-Z, SPACE **See note under ALTCODE
Instead of 'STRING <my password>' being a payload, it is stored as a broken up mess, reconstructed and autotyped by the flipper. Not impossible to read, just a bit more difficult, if done correctly the payload.txt can/should only exist on your flipper

--ALTCODE Substitution--  
I have added a slider that allows you to replace a number of characters (0-128) of the original string with their ALTCODE equivalents instead of a STRING command.  This really only works on Windows boxes, but should help confuse keyloggers. On linux sometimes it just drops the altcodes during transmission.  **Special characters may be possible if the original string is completely rendered in altcodes with no introduced errors (the alt slider is full, the error slider is empty)

--SHA Hashing--  
It also takes the original string, hashes it with sha256 and compares it with the string it thinks the input will make when the ducky script is run (executed on a flipper as bad USB payload).  The SHA hash appears in green if the predicted text matches the original string, if it appears in red there has been a logic error or the next section is at play.

--Error/Jitter/Entrophy--  
I have added another slider that adds error data to the ducky script as it's processed, wip here, very basic errors/jitter/entrophy at the moment, to further obscure the original string.  It's just some Pi segments and arrow commands at present.  *If you would like submit any decoy phrases (funny REMs) and/or short inputs to be used as error data, send them in email to matthew.house.ITPRO@gmail.com*

Using this *always* causes a hash mismatch because the string produced does not match the original string. This allows the injection of semi random non seed data, so two generations with the same seed key would make different payload.txt files and produce different typed passwords.

--payload.txt Creation and Sanitization of payload.txt and Clipboard--
When you generate your payload.txt it will appear in the same directory from which the script was called.  It clears your clipboard, and starts a 30 second timer that auto erases the payload.txt in the script directory.

**You can/should move the payload file with qFlipper quickly; if you drag a copy anywhere else it defeats the purpose of the burn logic.**

--Repeatability--  
The seed key really doesn't matter, what matters is that the flipper types the same password everytime for each payload, and it is 'kinda' hard to read it.
