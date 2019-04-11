# Instructions for the take home problem

Hello! The goal of this assignment is to take a small task and see how to you think about it, and how you write a little bit of code. Please spend 1-2 hours on this assignment and then send it off. If you're not completely done after 2 hours, just attach a note explaining what you accomplished, what you found out, and what is still missing.

## Ingesting flight data
The task is to read in real time flight data and determine whether to issue a notificartion for each flight update.

See the attached files realtime.txt and notifications.csv. 
`realtime.txt` contains tab-separated data containing updates about the flight status of a bunch of flights. The only columns you'll need for this exercise are `FlightId`, `InGateUtcChange`, and `InGateUtc`, which correspond to a flight ID, whether or not the arrival time has been updated, and the arrival time, respectively. When column `InGateUtcChange` has the value `Y`, this means that the arrival time has changed.

`notifications.txt` contains three columns: `FlightId`, `InGateUtc`, and `SentTimestampUtc` and is a log of past notifications that have been issued for each flight ID. SentTimestamp represents when the notification was issued, and InGateUtc is the arrival time for that notification.

The task is to read realtime.txt, and for each flight update (aka row), if the row represents a new arrival time, and it's been more than 30 minutes since the last notification, issue a new notification by printing "Flight <flight_id> is now scheduled to arrive at <new arrival time>". Submit your code when you're done! (Use a language of your choosing, but Python is preferred).

Pretend that the current time is `2017-04-13 20:28Z` (all times are UTC time).
