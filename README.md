## TODO
- [ ] Flask server with API on door pi
  - Store current door state as JSON so open/close data persists
- [ ] [DNS server](https://www.howtogeek.com/devops/how-to-run-your-own-dns-server-on-your-local-network/) on Pi to make connection easier
- [ ] Redo website with responsive functionality and API interaction
- [ ] Access from outer internet- password entry

## Materials list
- [x] Door control raspberry pi in chicken coop
- [x] [Linear actuator](https://www.amazon.com/ECO-LLC-Acutator-Electric-Actuator/dp/B08HQRNGYM) for door control
- [x] [12v AC adapter](https://www.amazon.com/Kastar-Adapter-5-52-5mm-Wireless-Security/dp/B003TUMDWG) to power linear actuator
- [x] [H-bridge for motor control](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6)

## Door API
- `POST /open` opens the door, returns JSON with:
  - `"success":` true if door is opening, false if door could not be opened
  - `"delay":` time motor will move for or 0 if unsuccessful, integer
- `POST /close` closes the door, same JSON as open
- `POST /times` updates times with JSON `"openTime"` and `"closeTime"` times formatted in 24hr, with 4 digits as string split by a colon.
  Returns `"success":` `false` or `true`.
- `GET /state` returns JSON as follows:
  - `"open":` `null` if unknown state, `true` if open, `false` if closed
  - `"moving":` `true` or `false`
  - `"openTime"` and `"closeTime":` times formatted in 24hr, with 4 digits as string split by a colon

## Wifi troubleshooting
Problem: Wifi does not stay connected in the long term (about a day).
TODO: wait until disconnection, then run `journalctl | grep wlan`
Steps tried:
- [x] WORKED Disable fast roaming on router: https://github.com/raspberrypi/linux/issues/3849
- [ ] Set up cron job to reboot when network unreachable
- [ ] Debug undervolting issues
