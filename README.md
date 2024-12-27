### Run project 
1. Add file config sdk dowload from firebase setting
2. Change name file <b>sm-home-firebase-sdk.json</b>
3. Run <b>python3 main.py</b>

### Gateway
1. sudo systemctl status sm_home.service
2. sudo journalctl -u sm_home.service -f

### Camera
1. sudo systemctl status sm_home_camera.service
2. sudo journalctl -u sm_home_camera.service -f
