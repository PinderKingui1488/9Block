# 9Block Project

## Server Setup Instructions

### Prerequisites
- Ubuntu Server (latest LTS version)
- Python 3.12
- PostgreSQL
- Nginx
- Gunicorn

### Installation Steps

1. **Update system and install dependencies**
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3.12 python3.12-venv nginx postgresql postgresql-contrib
```

2. **Install Poetry**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
```

4. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/9block
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

5. **Enable the site and restart Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/9block /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

6. **Configure Gunicorn service**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following configuration:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/.venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    your_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

7. **Start and enable Gunicorn**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## Deployment

The project uses GitHub Actions for continuous integration and deployment. The workflow is configured to:
1. Run tests on every push
2. Deploy to the server if tests pass and the push is to the main branch

### Required GitHub Secrets
- `SECRET_KEY`: Django secret key
- `SSH_KEY`: SSH private key for server access
- `SERVER_IP`: Your server's IP address
- `SSH_USER`: SSH username
- `DEPLOY_DIR`: Deployment directory on the server

### Local Development Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/9block.git
cd 9block
```

2. Install dependencies
```bash
poetry install
```

3. Copy .env.example to .env and configure variables
```bash
cp .env.example .env
```

4. Run migrations
```bash
poetry run python manage.py migrate
```

5. Start development server
```bash
poetry run python manage.py runserver
```

## Security Considerations

1. Configure firewall
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

2. Set up SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

3. Regular security updates
```bash
sudo apt update
sudo apt upgrade
``` 