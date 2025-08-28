# Deployment Guide

This guide covers different deployment options for the Website Reverse Engineer application.

## Local Development Deployment

### Quick Start
1. Ensure you have Python 3.11+ and Node.js 20+ installed
2. Clone or extract the project files
3. Follow the setup instructions in README.md
4. Run the application locally on http://localhost:5000

## Production Deployment Options

### Option 1: Traditional Server Deployment

#### Requirements
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+
- Node.js 20+
- Nginx (recommended for reverse proxy)
- SSL certificate (for HTTPS)

#### Steps

1. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Node.js
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm -y

# Install Nginx
sudo apt install nginx -y
```

2. **Application Setup**
```bash
# Create application directory
sudo mkdir -p /var/www/reverse-engineer-app
sudo chown $USER:$USER /var/www/reverse-engineer-app

# Copy application files
cp -r reverse-engineer-app/* /var/www/reverse-engineer-app/

# Set up backend
cd /var/www/reverse-engineer-app/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install

# Build frontend
cd ../frontend
npm install
npm run build
cp -r dist/* ../backend/src/static/
```

3. **Environment Configuration**
```bash
# Create environment file
cat > /var/www/reverse-engineer-app/backend/.env << EOF
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.manus.im/api/llm-proxy/v1
FLASK_ENV=production
EOF
```

4. **Systemd Service**
```bash
# Create service file
sudo cat > /etc/systemd/system/reverse-engineer.service << EOF
[Unit]
Description=Website Reverse Engineer App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/reverse-engineer-app/backend
Environment=PATH=/var/www/reverse-engineer-app/backend/venv/bin
EnvironmentFile=/var/www/reverse-engineer-app/backend/.env
ExecStart=/var/www/reverse-engineer-app/backend/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable reverse-engineer
sudo systemctl start reverse-engineer
```

5. **Nginx Configuration**
```bash
# Create Nginx site configuration
sudo cat > /etc/nginx/sites-available/reverse-engineer << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/reverse-engineer-app/backend/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/reverse-engineer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Docker Deployment

#### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "src/main.py"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  reverse-engineer-app:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_API_BASE=https://api.manus.im/api/llm-proxy/v1
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - reverse-engineer-app
    restart: unless-stopped
```

### Option 3: Cloud Platform Deployment

#### Heroku
1. Create a Heroku app
2. Add buildpacks for Python and Node.js
3. Set environment variables
4. Deploy using Git

#### DigitalOcean App Platform
1. Connect your repository
2. Configure build and run commands
3. Set environment variables
4. Deploy

#### AWS/GCP/Azure
Use container services or traditional VM deployment following Option 1 steps.

## Environment Variables

Required environment variables:

```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.manus.im/api/llm-proxy/v1
FLASK_ENV=production  # for production deployments
```

## Security Considerations

1. **API Keys**: Store securely using environment variables or secret management
2. **HTTPS**: Always use SSL/TLS in production
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: Validate all user inputs
5. **CORS**: Configure CORS appropriately for your domain
6. **Firewall**: Restrict access to necessary ports only

## Monitoring and Logging

### Application Logs
```bash
# View service logs
sudo journalctl -u reverse-engineer -f

# Application logs location
tail -f /var/www/reverse-engineer-app/backend/app.log
```

### Health Checks
Implement health check endpoints:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Monitoring Tools
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: New Relic, DataDog
- **Log aggregation**: ELK Stack, Splunk

## Backup and Recovery

### Database Backup
```bash
# Backup SQLite database
cp /var/www/reverse-engineer-app/backend/src/database/app.db /backup/location/
```

### Application Backup
```bash
# Full application backup
tar -czf reverse-engineer-backup-$(date +%Y%m%d).tar.gz /var/www/reverse-engineer-app/
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple application instances
- Implement session storage (Redis)

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching (Redis, Memcached)

### Performance Optimization
- Enable gzip compression
- Implement CDN for static assets
- Use database connection pooling
- Implement request caching

## Troubleshooting

### Common Issues

1. **Port already in use**
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

2. **Permission errors**
```bash
sudo chown -R www-data:www-data /var/www/reverse-engineer-app/
sudo chmod -R 755 /var/www/reverse-engineer-app/
```

3. **Playwright browser issues**
```bash
# Reinstall browsers
cd /var/www/reverse-engineer-app/backend
source venv/bin/activate
playwright install --with-deps
```

4. **Memory issues**
```bash
# Check memory usage
free -h
# Increase swap if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test API endpoints manually
4. Check network connectivity
5. Review security group/firewall settings

For additional support, refer to the main README.md or open an issue in the project repository.

