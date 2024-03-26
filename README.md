add below to /etc/systemd/system/myflaskapp.service

[Unit]
Description=Gunicorn instance to serve my flask app
After=network-online.target myflaskapp.service
Wants=network-online.target

[Service]
User=matcris81
Group=matcris81
WorkingDirectory=/home/matcris81/webserver/flask_webserver
Environment="PATH=/home/matcris81/webserver/venv/bin"
ExecStart=/home/matcris81/webserver/venv/bin/python api.py

[Install]
WantedBy=multi-user.target

then reload systemd
sudo systemctl daemon-reload

then reload service
sudo systemctl restart myflaskapp.service

check status for errors
sudo systemctl status myflaskapp.service

