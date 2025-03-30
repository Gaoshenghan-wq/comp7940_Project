# comp7940_Project

As mainland can not connect to docker hub, I used anzure images resp to manage online images

anzure container update processes: (7940project is images name and comp7940project is anzure appname)
1. docker build -t 7940project .
2. docker tag 7940project 24428078images.azurecr.io/7940project
2. docker push 24428078images.azurecr.io/7940project
3. az login
3. az containerapp update --name comp7940project --resource-group 24428078 --image 24428078images.azurecr.io/7940project:latest
