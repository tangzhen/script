#!/bin/sh

# Rename all folder.
# find . -name "Camera360Plus" -type d -exec rename -v 's/Camera360Plus/Camera360/' {} + 
for i in `find . -name "Camera360Plus" -type d`; do mv $i `echo $i | sed 's/Camera360Plus/Camera360/'`; done

# Replace all string.
grep -rl 'Camera360Plus' --exclude=*.sh ./ | xargs sed -i 's/Camera360Plus/Camera360/g'
