# Backend Build with Flask

### To Run
    cd backend
    pip install -r requirements.txt
    flask --app app run --debug

### Path
    1 - '/' : Default
    2 - '/getall?lat=<latitutde>&long=<longtitude>&std=YYYY-MM-DD&end=YYYY-MM-DD'
        EX: http://172.16.66.233:8080/getall?lat=13.0827&long=80.2707&std=2024-02-01&end=2024-02-15

### Note: Currently configured to API linked to my account, so if you want to work with it follow guide in google earth (Sorry I lost that guide link)
    1 - You have to create new project in google earth, then do as said in guide
    2 - Create API call via google console
    3 - Change project ID with yours [Image](image.png)


### File Structure
- app.py - Contains function that fetch data from ge
- details.py - Contains function to compare data

# Todo
- [x] Write todo here
