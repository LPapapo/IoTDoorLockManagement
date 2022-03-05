**My project's goal is to employ an IoT management system for a door.**

This will provide access as well as a database for a door. Access to the building will be granted by scanning a QR code, and all access history will be saved in a database that will contain all registered users and will provide them with a unique QR code that will be renewed every day. 00:00

I’ll be using the following hardware:

1.  A raspberry pie 4
2.  A solenoid lock
3.  A relay module
4.  12V 3A power supply
5.  12 V to 5V converter

---

A 3D printing case with an integrated pi camera was created for this project.

![IMG_3567](https://aws1.discourse-cdn.com/balena/optimized/2X/1/140bee934c001faab0cea84362f952cf3fe75b4f_2_281x375.jpeg)

**The steps would be as follows**:

Admin logs in to the local web page and registers a user account.  
 

![Registration_Website](https://aws1.discourse-cdn.com/balena/optimized/2X/d/d9fb4d4bfc2fb6381b09e6fcbee6842612bb80b0_2_517x225.jpeg)

[**Registration\_Website3402×1488 121 KB**](https://aws1.discourse-cdn.com/balena/original/2X/d/d9fb4d4bfc2fb6381b09e6fcbee6842612bb80b0.jpeg)

*   A QR code is sent to the user’s email address.( UUID random generated QR code )  
     

![QRcode](https://aws1.discourse-cdn.com/balena/optimized/2X/f/fcdfa2244e7075cd88e2a5db007439b8c180b8ac_2_383x375.jpeg)

[**QRcode679×664 49.5 KB**](https://aws1.discourse-cdn.com/balena/original/2X/f/fcdfa2244e7075cd88e2a5db007439b8c180b8ac.jpeg)

*   User is registered in a Database.  
     

![UserDB](https://aws1.discourse-cdn.com/balena/optimized/2X/6/6ba8a4a00930a3c493afb22441568c91a6998b28_2_517x277.jpeg)

[**UserDB1920×1031 93.6 KB**](https://aws1.discourse-cdn.com/balena/original/2X/6/6ba8a4a00930a3c493afb22441568c91a6998b28.jpeg)

*   By scanning his QR code, the user unlocks the door.(After 5 seconds, the door locks again.)  
     

![ezgif.com-gif-maker](https://aws1.discourse-cdn.com/balena/original/2X/b/b66f5ea4dcb3a05c2ee759b0430995084aeedfda.gif)

*   The office’s access log is accessible to the administrator.  
     

![AccessDB](https://aws1.discourse-cdn.com/balena/optimized/2X/8/88025e49de7d101b4cadf8a4a8db166f60cc6283_2_517x276.jpeg)

[**AccessDB1920×1028 170 KB**](https://aws1.discourse-cdn.com/balena/original/2X/8/88025e49de7d101b4cadf8a4a8db166f60cc6283.jpeg)

*   A new QR code will be sent to all registered users every day at 00:00.
