## Materials list
- [x] Door control raspberry pi in chicken coop
- [x] [Linear actuator](https://www.amazon.com/ECO-LLC-Acutator-Electric-Actuator/dp/B08HQRNGYM) for door control
- [x] [12v AC adapter](https://www.amazon.com/Kastar-Adapter-5-52-5mm-Wireless-Security/dp/B003TUMDWG) to power linear actuator
- [x] [H-bridge for motor control](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6)

## Door API
- `POST /open` opens the door
- `POST /close` closes the door
- `POST /time` with times sets the times in cron
- `GET /state` returns whether the door is "open" or "closed" and the current times in JSON, maybe more info like door is opening or closing?

## Wifi troubleshooting
Problem: Wifi does not stay connected in the long term (about a day).
TODO: wait until disconnection, then run `journalctl | grep wlan`

## TODO
- [ ] Flask server with API on door pi
- [ ] [DNS server](https://www.howtogeek.com/devops/how-to-run-your-own-dns-server-on-your-local-network/) on Pi to make connection easier
- [ ] Redo website with responsive functionality and API interaction
- [ ] Access from outer internet- password entry
