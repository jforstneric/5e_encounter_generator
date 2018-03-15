D&D 5e random combat encounter generator

This is a small project for learning/practicing Python. I realise it could be improved in many ways but perhaps someone will find it useful :-)

I've tried to make it easy to use, though among other things I don't do any input validation (entering numbers which are too high will return an IndexError). 

The program generates a random combat encounter for a specified number and level of heroes and remembers both (so you don't have to keep entering the same adventuring party). You can choose the monsters either based on location or type. Monster information is in an included monster.csv file, I've added a sample file (with a selection of monsters from the 5e Monster Manual). I've added location information purely by feeling, both the locations and types can be modified and added to, as long as the order of the information for each monster stays the same. Both columns can easily be changed to any other keywords (possibly to adapt this to a specific campaign setting). 

The CSV file can also be cut down before use. For example, to run a strictly nature and underground campaign, one could remove all other monsters beforehand, then expand the tags to change 'nature' to 'forest', 'plain', 'hills', 'mountains', etc.

The CSV information should be: name,location,type,xp,MM page.

The program first calculates the XP threshold for the party and difficulty we're trying to achieve. From the possible monsters we remove any which are too weak (so we don't have encounters with twenty villagers) or too strong, from the remaining monsters we add random ones to the encounter, repeating the removal of monsters which would be too strong (as this goes down with each added monster). The program isn't as exact as it could be because of the way encounter XP are calculated in 5e (the difficulty rises non-linearly with the number of enemy creatures). 

The program should work better with a larger set of monsters (as it stands, certain combinations of difficulty/location/type are not be possible), hopefully I'll get around to adding all of the monsters from the DMG to the CSV file, but the resulting encounters will still need a bit of tweaking (though, honestly, this applies to most encounters in D&D ;-)
