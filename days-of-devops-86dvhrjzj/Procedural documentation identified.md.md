### Python3
####  This is how to initiate a python virtual environment once it has been setup 
- cd /home/<username redacted>/myproject-12-29-2024 # 
source myenv/bin/activate
- (myenv) /home/<username redacted>/myproject-12-29-2024 # whoami
<username redacted>
- (myenv) /home/<username redacted>/myproject-12-29-2024 # 


### Docker
- Docker main commands:
-- [To list docker sessions] docker ps 
-- [To start a docker container using example from their hub] docker run -dp 80:80 docker/getting-started 
-- [To stop a docker container] docker stop <id for container using docker ps, step above>
--- Further details via the following simple yet well-written post: https://linuxhandbook.com/docker-stop-container/ 