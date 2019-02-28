D&D 5e random combat encounter generator - 2.0

This is a small project for learning/practicing Python. I realise it could be improved in many ways but perhaps someone will find it useful :-)

I've tried to make it easy to use, though among other things I don't do any input validation (entering numbers which are too high will return an IndexError). 

The program generates a random combat encounter for a specified number and level of heroes and remembers both (so you don't have to keep entering the same adventuring party). You can choose the monsters based on location. Monster information is in an included monster.csv file, I've added a sample file (with a selection of monsters from the 5e Monster Manual). I've added location information purely by feeling. 

The CSV file can also be cut down before use. For example, to run a strictly nature and underground campaign, one could remove all other monsters beforehand, then expand the tags to change 'nature' to 'forest', 'plain', 'hills', 'mountains', etc.

The CSV information should be: name,location,type,xp,MM page.

The program first calculates the XP threshold for the party and difficulty we're trying to achieve. From the possible monsters we remove any which are too weak (so we don't have encounters with twenty villagers) or too strong, from the remaining monsters we add random ones to the encounter, repeating the removal of monsters which would be too strong (as this goes down with each added monster). The program isn't as exact as it could be because of the way encounter XP are calculated in 5e (the difficulty rises non-linearly with the number of enemy creatures). 

The program should work better with a larger set of monsters (as it stands, certain combinations of difficulty/location are not be possible), hopefully I'll get around to adding all of the monsters from the DMG to the CSV file, but the resulting encounters will still need a bit of tweaking (though, honestly, this applies to most encounters in D&D ;-)

Changelog:
1.0 - Initial version
2.0 - Added arguments - you can now specify the party and encounter via arguments when running the program. If arguments are missing, it runs in interactive mode (as before). Removed option to choose creatures by type, only by location.
