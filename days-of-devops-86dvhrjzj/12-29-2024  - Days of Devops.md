### Standard Logs

## Session 01: [16:00 to 17:21]
- Ran out of space <redacted>. Space was being taken up by:
  1. Timeshift snapshots
  2. Python virtual environment 
  3. System logs (about 2 Gigs)
- Cleaned up the space, with assistance
- Disabled Timeshift snapshots
- [LINE MARKED TO BE REDACTED FOR PUBLIC NOTES]
- 17:00 Downloading an ISO prior to break
  - Downloading Ubuntu Server prior to manual install

## Session 02: [17:49 to 18:23]
- Action items (two) to tackle in sequence, after the break. Moved to Session 03 at 18:22  
- 17:49 Back. Writing ISO in order to boot
- 18:02 Default Burner app keeps throwing errors. I wonder if it will still burn the image, even though it keeps throwing errors
  - Switched to Brasero. Which was also throwing errors. After a search via forums, the following entry 'could' help avoid the errors. It's been a while since I burned an image. So let's simulate it first. Thanks to the following individual on the interwebs (below). And thanks to Vice President Al-Gore for inventing the internet.

> June 27th, 2009, 10:00 AM                                                                                         
> Brasero doesn't know it's supposed to burn an image (as opposed to just data) unless you tell it...               
> Try right-clicking on the iso file you have downloaded and then choose "burn to disk," and Brasero gets it        
> from there.                                                                                                       
> One more thing to check, and I only mention it because I made this mistake only yesterday - make sure the         
> blank CD is a CD and not a DVD!                                                                                   
> Cheers,                                                                                                           
> <name redacted>

**Note to self:**
- It's slightly different for me. As in, I have to right-click on the iso and then 'open' it in Brasero vs the "burn to disk," option. It's interesting that the user placed a comma inside of double-quotes.

## Session 03: [18:30 to 19:45]
- 18:30 Back from break. Continuing with the ISO burning process.
- 18:45 Successfully burned the ISO. Now booting from the new ISO.
- 19:00 Installation process started. Following the steps as per the documentation.
- 19:30 Installation completed. System rebooted successfully.
- 19:45 Wrapping up the session. Documenting the steps taken and any issues encountered.

### Action items with status
All 'OPEN' action items transferred to Project Management software of choice:

- [CLOSED]: Make a note that python virtual environments take up a lot of space. The process of creating virtual environments and activating, deactivating and if needed, getting rid of them has to be documented properly.
- [TRANSFERRED]: Look into https://canonical.com/multipass & https://ubuntu.com/download/server#automated-provisioning also
- [TRANSFERRED]: This piqued my interest: https://ubuntu.com/observability/what-is-observability & I noticed that Ubuntu offers the building of a private cloud: I guess this is separate: https://ubuntu.com/observability/what-is-observability
- [TRANSFERRED] Tinker with jupyter and see what benefits it provides.
- [CLOSED] Documented how to open and close python virtual environments. Also from ssh.
- [CLOSED]: Add all times to project management software & update Github for S-vhp
- [OPEN]: Update the newly added Wins section below.

### Wins today
- [Ok win] Reclaimed space on existing machine.
- [Good Win!] Got new machine up and running. Putting the 8 cores to use. The new distro handles the CPUs well and so far the machine is not over-heating. This makes me realize how efficiently software can handle the hardware or to the contrary. It reminds me of a conversation I had, albeit briefly with someone back in the year 2012. However, I have yet to find a 'sensors' package for the distro I am leveraging.
- [Okay win that will yield dividends] Learning how to set up python virtual environment.
- [Okay Win that will yield dividends] Beginning to tinker with docker (nano win)
- [Standard Win] Installed, updated definitions, and ran anti-virus scan.