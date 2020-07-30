Django + Vue

Backend:
- cd miele-hosting // go to project folder
- pipenv shell // start virtual environment
- python3 manage.py runserver 192.168.1.70:8000 // start local server on selected IP:Port
- python3 manage.py makemigrations // prepare DB structure changes
- python3 manage.py migrate // apply these changes

Frontend:
- cd miele-hosting/client // go to client folder
- yarn serve // start local server on localhost:8080
- yarn build // generate production build
