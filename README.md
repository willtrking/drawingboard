DrawingBoard - A web UI for aminator
=========================================

DrawingBoard is a simple web UI for Netflix's aminator (https://github.com/Netflix/aminator)

Basic details:

Create 'Amination Templates':
	Allows you to create and version CLI args to be passed to aminator

Create 'AMI Versions':
	Allows you to create and version AMI's. When creating you tie in an 'Amination Template'.
	Allows you to specify regions for your AMI to be placed into

Create and start an 'amination':
	Runs aminator proxied through a bash script which stores output for viewing through the UI. Also copies your AMI
	to regions specifief in your 'AMI Version'

Requires python2.7 and an AWS CLI version with 'ec2 copy-image'

This project was done very quickly and without many regards to style, so there may be some weirdness in the codebase.

More details to follow