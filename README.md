# Requirements
Docker

# Usage
- Install docker
- Run the following in the terminal: `sudo docker run -d 3mblem/apitest:latest`
- Find your container id with `sudo docker ps` copy the container id
- Find the ip of your container with `sudo docker inspect CONTAINER_ID | grep "IPAddress"` (remember to replace the container id)
- Go to http://IP_ADDRESS/docs#/ (all the documentation, openApi scheme, and an interactive ui to send request can be found there)
- user `johndoe` password `secret`
